import esprima

""" {
    type: "IfStatement",
    test: {
        type: {},
        consequent: {},
        alternate: {} | null
    }
} """


class DecisionParser:

    def __init__(self):
        self.syntax_tree = None
        self.entities = []

    def __build_syntax_tree(self, source):
        self.syntax_tree = esprima.parseScript(source).toDict()['body']

    '''Decisionparser.parse()
        PARAMETERS:
            source (str)
                - c style nested if-else statement.
                - conditions may include [!, &&, ||, (, ), >, <, >=, <=, ==, identifiers]
        RETURNS:
            List of entities [str] | Exception message (str)
    '''

    def parse(self, source):
        try:
            self.entities = []
            self.__build_syntax_tree(source)
            # Single root assumption
            root = self.syntax_tree[0]
            self.__parse(root, prerequisites=[])
            return self.entities

        except Exception as ex:
            return str(ex)

    def get_entities_set(self):
        
        temp_list = []
        
        for entity in self.entities:
            entity_str = ",".join(entity)
            entity_str = entity_str.replace('!!', '')
            temp_list.append(entity_str)
        
        temp_list = list(dict.fromkeys(temp_list))

        entity_list = list()
        for entity in temp_list:
            entity = entity.split(',')
            entity.reverse()
            entity_list.append(entity)
       
        return entity_list

    def __parse(self, block, prerequisites):
        if block['type'] != "IfStatement":
            raise Exception("INVALID-INPUT")

        condition = DecisionParser.build_condition(block['test'])
        neg_condition = '!' + condition

        if_prerequisites = prerequisites + [condition]
        else_prerequisites = prerequisites + [neg_condition]
        self.entities.append(if_prerequisites)
        if_children = block['consequent']['body']

        if 'alternate' in block:
            #self.entities.append(else_prerequisites)
            else_children = block['alternate']['body']
        else:
            else_children = []

        for child in if_children:
            self.__parse(child, prerequisites=if_prerequisites)
        for child in else_children:
            self.__parse(child, prerequisites=else_prerequisites)

    @staticmethod
    def build_condition(test):
        if test['type'] == 'Identifier':
            return test['name']
        elif test['type'] == 'LogicalExpression' or test['type'] == 'BinaryExpression':
            left_operand = DecisionParser.build_condition(test['left'])
            right_operand = DecisionParser.build_condition(test['right'])
            return f"({left_operand} {test['operator']} {right_operand})"
        elif test['type'] == 'UnaryExpression' and test['operator'] == '!':
            return f"!({DecisionParser.build_condition(test['argument'])})"
        else:
            raise Exception("INVALID-INPUT")


if __name__ == "__main__":

    # If entities
    # !o8, (o5 && o3), !o4, (o4 || o2)
    # !o8, (o5 && o3), o4
    # !o8, (o5 && o3)
    # o8

    # Else entites
    # !o8
    # !o8, (o5 & o3), !o4

    program1 = '''
        if ((o8)) {
        } else {
            if ((o5 & o3)) {
                if((o4)){
                }else{
                    if(o4 || o2){
                    }
                }
            }
        }
    '''

    program2 = '''
        if (o84 && o93) {
        }else{}
    '''

    program3 = '''
        if ((o1)) {
            if ((o39)) {
            }
        }
    '''

    program4 = '''
        if ((o84)) {
            if ((o94)) {
            } else {
            }
        }
    '''

    program5 = '''
    if ((o92)) {
        if (o53) {
        }
        if (o37) {
        }
        if (o2 && !(o78)) {
        }
        if (o63) {
        }
        if (o51) {
        }
        if (o53) {
        }
        if (o37) {
        }
        if (o2 && !(o78)) {
        }
        if (o63) {
        }
        if (o51) {
        }
    }s
    '''

    filename = "./src/MCDC-Input-Model-Files/test.java"
    with open(filename, 'r') as file:
        program = file.read()

    decision_parser = DecisionParser()
    decision_parser.parse(source=program)
    entities = decision_parser.get_entities_set()
    for entity in entities:
        print(entity)
