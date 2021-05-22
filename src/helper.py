import re

class Conversion:
    PARANTHESIS = {'(', ')'}
    parameterPattern = None
    operatorPattern = None

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

    def infix_2_prefix(self, formula):
        elements = self.__getElements(formula)
        print(formula)
        formula = self.reverse(formula)
        
        output = ""
        NUMBER_PARA = 0
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
        print(formula)
        print(elements)
        formula = self.format(formula, elements)
        print(formula)
        return formula
    
    def format(self, formula, elements):

        matcher = self.getMatcher()
        
        check = True
        while(check):
            matched = matcher.search(formula)

        for operator in self.OPERATORS:
            formula = formula.replace(operator, (operator+ ' '))
        for element in elements:
            formula = formula.replace(element, (element+ ' '))
        return formula
    
    def getMatcher(self):
        print(self.parameterPattern)
        pattern = "["
        for op in self.OPERATORS:
            pattern += op
        pattern += "]"
        pattern += self.parameterPattern
        matcher = re.compile(pattern)
        return matcher

                
            


if __name__ == '__main__':
    
    OPERATORS = {'+', '-', "*", "/"}
    PRIORITY = {
        '(':0,
        ')':0,
        '+':1,
        '-':1,
        '*':2,
        '/':2
    }

    C = Conversion(OPERATORS, PRIORITY)

    formula = "a+b+c+d"
    C.infix_2_prefix(formula)

#REF
#https://www.codesdope.com/blog/article/expression-parsing/