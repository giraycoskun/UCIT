from unicodedata import decimal
from DecisionParser import DecisionParser
from subprocess import Popen, PIPE
from Masking_MCDC import MaskingMCDCTest

import os
import sys
import logging
import re
import json


logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

## PARSER
MODEL_PATH = "models"
ROOT_PATTERN = '#if[\(\)A-Za-z0-9&!|\{\}\n\t ]*'
TEST_SPACE_DIRECTORY = "src/MCDC-Input-Model-Files/"
OPTION_PATTERN = 'o[0-9]*'
UCIT_OBJECT_DIRECTORY = "src/tool/ucitObject"
TEST_RESULTS_DIRECTORY = "src/TestResults/"
TEST_RESULT_STDOUT_FILE = "src/tool/stdout.txt"
TEST_RESULT_STDERR_FILE = "src/tool/stderr.txt"

for root, dirs, files in os.walk(MODEL_PATH, topdown=False):
    for name in files:
        filename = os.path.join(root, name)
        if filename.endswith(".java"):
            model_name = os.path.basename(root)
            log.info("Model is {}".format(model_name))
            log.info("File is: {}".format(filename))

            with open(filename, 'r') as file_handler:
                file = file_handler.read()

            TEST_SPACE = {
                "decisions":[],
                "options": [],
                "numbers": {}
            }
            
            parser = DecisionParser()
            root_conditions = re.findall(ROOT_PATTERN, file)
            decisions = list()
            for condition in root_conditions:
                condition = condition.replace('#', '').replace('||', '|').replace('&&', '&').replace('!!', '')
                parser.parse(source=condition)
                entities = parser.get_entities_set()
                decisions.extend(entities)
            log.info("Condition Number: {}".format(str(len(root_conditions))))
            
            TEST_SPACE['decisions'] = decisions
            log.info("Number of Decisions are {}".format(str(len(decisions))))

            options = set(re.findall(OPTION_PATTERN, file))
            TEST_SPACE['options'] = list(options)
            log.info("Number of Options are {}".format(str(len(options))))

            log.info("TEST SPACE is Generated for {}".format(model_name))
            output_filename = TEST_SPACE_DIRECTORY + model_name + ".json"
            with open(output_filename, 'w') as output_file:
                json.dump(TEST_SPACE, output_file, indent = 8)

            log.info("TEST ENTITY GENERATION STARTED")
            tester = MaskingMCDCTest(model_name, TEST_SPACE)
            tests = tester.getTestSet()
            tester.dumpTests(tests)
            log.info("Tests Are Generated")
            

            result_dir = TEST_RESULTS_DIRECTORY+model_name
            try:
                os.makedirs(result_dir)
            except OSError as e:
                log.info("Directory {} already exists".format(result_dir))

            try:
                command = ["mv", UCIT_OBJECT_DIRECTORY, result_dir]
                process = Popen(command, stdout=PIPE, stderr=PIPE).wait()

                command = ["mv", TEST_RESULT_STDOUT_FILE, TEST_RESULT_STDERR_FILE, result_dir]
                process = Popen(command, stdout=PIPE, stderr=PIPE).wait()

                log.info("SAVING RESULTS SUCCESSFUL!!")

            except:
                log.info("SAVING RESULTS FAILED!!")