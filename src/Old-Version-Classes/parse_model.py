from os import device_encoding
import re

def parse(filename):
    with open(filename, 'r') as file:
        input = file.read()

    result = {
        "decisions":[
            
        ],

        "options": set(),
        "numbers": {}
    }

    pattern = re.compile('\/\/[A-Za-z0-9; ]*')
    elements = re.split(pattern, input)
    elements = [item.strip() for item in elements]
    elements = list(filter(lambda item: item != '', elements))

    first_if_pattern = re.compile('#if[\(\)A-Za-z0-9&!| ]*')
    condition_pattern = re.compile('\([\(\)A-Za-z0-9&!| ]*\)')
    option_pattern = re.compile('o[0-9]*')
    inside_if_pattern = re.compile('\{[A-Za-z0-9&!| ]*\}')
    else_pattern = re.compile('else[ ]*\{[\{\}\(\)A-Za-z0-9!&| ]*\}')
    if_pattern = re.compile('if *\{[\{\}\(\)A-Za-z0-9!&| ]*\}')


    for item in elements:

        item = item.replace('\n', '')
        item = item.replace('\t', '')

        item = item.replace('&&', '&')
        item = item.replace('||', '|')

        matchedObject = first_if_pattern.match(item)
        if_condition = matchedObject.group().strip()
        condition = condition_pattern.findall(if_condition)[0][1:-1]
        
        result["decisions"].append(condition)

        options = option_pattern.findall(if_condition)
        result["options"].update(options)

        item = item[len(matchedObject.group()):]

        inside_if_part = inside_if_pattern.match(item).group()
        num_if = len(re.findall('if', inside_if_part))
        pre_conditions = []
        for k in range(num_if):
            pre_conditions.append(condition)
            condition = if_pattern.search(inside_if_part).group()
            pass

        else_part = else_pattern.findall(item)
        if(else_part is not None):
            else_part = else_part[0]
            num_else = len(re.findall('else', else_part))
        pre_conditions = []
        for k in range(num_else):
            pre_conditions.append(condition)
            condition = else_pattern.search(else_part).group()
            pass

        


    result['options'] = list(result['options'])

    return

def if_func(item):

    pass

def else_func(item):
    pass

    

if __name__ == '__main__':
    file_directory = "./src/MaskingMCDC-Input-Model-Files/"
    filename = file_directory + "dia.java"
    parse(filename)