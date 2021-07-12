import re
from py_expression_eval import Parser
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class Conversion:

    PARANTHESIS = {'(', ')'}

    REPLACE_MAP = {
            '&': 'and',
            '|': 'or',
            '!': 'not'
    }

    def __init__(self, OPERATORS, PRIORITY={}):

        self.OPERATORS = OPERATORS
        self.PRIORITY = PRIORITY
        self.STACK = []

    def infix_2_prefix(self, formula):

        log.debug(" input formula: " + formula)

        elements = self.__getElements(formula)
        log.debug(" elements from formula: " + " ,".join(elements))

        formula = self.__replaceRegular2PythonOperators(formula)
        log.debug(" python formula: " + formula)
        parser = Parser()
        #temp = parser.parse(formula)
        formula = parser.parse(formula).toString()
        log.debug(" paranthesis formula: " + formula)
        formula = self.__replacePython2RegularOperators(formula)
        log.debug(" regular formula: " + formula)

        formula = self.reverse(formula)
        log.debug(" reversed formula: " + formula)
        
        output = ""
        for character in formula:
            #print(character)
            if character.isalnum():
                output += character
            elif character == '(':
                output += '('
                self.STACK.append('(')
            elif character in self.OPERATORS:

                while (len(self.STACK) > 0 and self.PRIORITY[self.STACK[-1]] >= self.PRIORITY[character]):
                    output += self.STACK.pop()
                self.STACK.append(character)
            elif character is ')':
            # if character is ')'
            #   then pop until '('.
                while self.STACK[-1] != '(':
                    output += self.STACK.pop()
                self.STACK.pop()
                output += ')'
        while len(self.STACK) > 0:
            output += self.STACK.pop()
        
        formula = self.reverse(output)
        log.debug(" re-reversed formula: " + formula)
        formula = self.format(formula, elements)
        log.debug(" result formula: " + formula)
        return formula

    def __getElements(self, formula):

        pattern = ""
        #ops = {'(', ')'}
        #ops = ops.union(self.OPERATORS)
        for element in self.OPERATORS:
            pattern = pattern + '\\' + element
        
        pattern = "[^" + pattern + "]+"
        matcher = re.compile(pattern)
        self.parameterPattern = pattern
        elements = matcher.findall(formula)
        
        return elements

    def __replaceRegular2PythonOperators(self, formula):

        for key, value in self.REPLACE_MAP.items():
            formula = formula.replace(key, (' '+value+' '))
        return formula

    def __replacePython2RegularOperators(self, formula):

        for key, value in self.REPLACE_MAP.items():
            formula = formula.replace(value, key)
        return formula
    
    def reverse(self, formula):
        def reverse_paranthesis(c):
            if c == '(' or c == ')':
                if c == '(':
                    return ')'
                else:
                    return '('
            else:
                return c

        formula = reversed(formula)
        formula = list(map(reverse_paranthesis, formula))
        return "".join(formula)
    
    def format(self, formula, elements):

        formula = formula.replace('!(', '(!')
        for operator in self.OPERATORS:
            formula = formula.replace(operator, (operator+ ' '))
        for element in elements:
            formula = formula.replace(element, (element+ ' '))
        return formula

    def formatSugarOps(self, formula):
        formula = formula.replace('&', '&&')
        formula = formula.replace('|', '||')
        #formula = formula.replace('-', '!')
        return formula

