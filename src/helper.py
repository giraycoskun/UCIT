import re

class Conversion:
    PARANTHESIS = {'(', ')'}

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
        elements = matcher.findall(formula)
        print(elements)
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

        for character in formula:
            #print(character)
            if character.isalnum():
                output += character
            elif character in self.OPERATORS or character == '(':
                #if(character == '('):
                 #       output += '('
                while (len(self.STACK) > 0 and self.STACK[-1] != "(" and self.PRIORITY[self.STACK[-1]] >= self.PRIORITY[character]):
                    output += self.STACK.pop()
                self.STACK.append(character)
            elif character is ")":
            # if character is ')'
            #   then pop until '('.
                while self.STACK[-1] != "(":
                    output += self.STACK.pop()
                self.STACK.pop()
                #output += ')'
        while len(self.STACK) > 0:
            output += self.STACK.pop()
        
        print(output)
        formula = self.reverse(output)
        print(formula)
        self.format(formula, elements)
        return formula
    
    def format(self, formula, elements):
        

        pass
                
            


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

    formula = "(1+2)*(3+4)"
    C.infix_2_prefix(formula)

#REF
#https://www.codesdope.com/blog/article/expression-parsing/