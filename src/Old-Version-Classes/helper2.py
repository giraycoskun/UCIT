import re
from py_expression_eval import Parser

    
    
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

        

    def __getElements(self, formula):

        pattern = ""
        ops = {'(', ')'}
        ops = ops.union(self.OPERATORS)
        for element in ops:
            pattern = pattern + '\\' + element
        
        pattern = "[^" + pattern + "]+"
        matcher = re.compile(pattern)
        self.parameterPattern = pattern
        elements = matcher.findall(formula)
        
        return elements
        
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

    def __replaceRegular2PythonOperators(self, formula):

        for key, value in self.REPLACE_MAP.items():
            formula = formula.replace(key, (' '+value+' '))
        return formula
    
    def __replacePython2RegularOperators(self, formula):

        for key, value in self.REPLACE_MAP.items():
            #print(key, value)
            formula = formula.replace(value, key)
            #print(formula)
        return formula
                
    def infix_2_prefix(self, formula):

        print("INPUT:", formula)

        elements = self.__getElements(formula)
        print("ELEMENTS:", elements)

        formula = self.__replaceRegular2PythonOperators(formula)
        print("1", formula)
        parser = Parser()
        #temp = parser.parse(formula)
        formula = parser.parse(formula).toString()
        print("2", formula)
        formula = self.__replacePython2RegularOperators(formula)
        print("3", formula)

        formula = self.reverse(formula)
        print("4", formula)
        
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
        print("5:", formula)
        formula = self.format(formula, elements)
        print("OUTPUT: ", formula)
        return formula
    
    def format(self, formula, elements):

        formula = formula.replace('!(', '(!')
        for operator in self.OPERATORS:
            formula = formula.replace(operator, (operator+ ' '))
        for element in elements:
            formula = formula.replace(element, (element+ ' '))
        return formula
    
    def getMatcher(self, elements):
        element_pattern = ""
        for item in elements:
            element_pattern = element_pattern + item + '|'
        element_pattern = '(' + element_pattern[:-1] + ')'
        print(element_pattern)
        op_pattern = ""
        for op in self.OPERATORS:
            op_pattern = op_pattern + '\\' + op
        op_pattern = '[' + op_pattern + ']'
        pattern = op_pattern + element_pattern + element_pattern
        print(pattern)
        matcher = re.compile(pattern)
        #print(matcher.search("+a+b+cd"))
        return matcher
    
    def formatSugarOps(self, formula):
        formula = formula.replace('&', '&&')
        formula = formula.replace('|', '||')
        #formula = formula.replace('-', '!')
        return formula
    

def isValidString(str):
    cnt = 0
    for i in range(len(str)):
        if (str[i] == '('):
            cnt += 1
        elif (str[i] == ')'):
            cnt -= 1
        if (cnt < 0):
            return False
    return (cnt == 0)

def isParenthesis(c):
    return ((c == '(') or (c == ')'))
      
# method to remove invalid parenthesis 
def removeInvalidParenthesis(str):
    if (len(str) == 0):
        return
          
    # visit set to ignore already visited 
    visit = set()
      
    # queue to maintain BFS
    q = []
    temp = 0
    level = 0
      
    # pushing given as starting node into queu
    q.append(str)
    visit.add(str)
    while(len(q)):
        str = q[0]
        q.pop()
        if (isValidString(str)):
            #print(str)
              
            # If answer is found, make level true 
            # so that valid of only that level 
            # are processed. 
            level = True
        if (level):
            continue
        for i in range(len(str)):
            if (not isParenthesis(str[i])):
                continue
                  
            # Removing parenthesis from str and 
            # pushing into queue,if not visited already 
            temp = str[0:i] + str[i + 1:] 
            if temp not in visit:
                q.append(temp)
                visit.add(temp)
    return str

#REFRENCES
#https://www.geeksforgeeks.org/remove-invalid-parentheses/


if __name__ == '__main__':

    OPERATORS = {'&', '|', '!'}
    PRIORITY = {
        '!':2,
        '&':1,
        '|':1,
        '(':0,
        ')':0
    }

    formula = "a|(b&c)"
    formula2 = "a|(b&-c)"
    formula3 = "-a|(b&c)"
    formula4 = "a|-(b&c)"

    C = Conversion(OPERATORS, PRIORITY)
    C.infix_2_prefix(formula2)