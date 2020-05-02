###############################################################################
#                                                                             #
#  TRANSFORMER                                                                #
#  Transform AST tree to pretty-print string                                  #
###############################################################################

from lark import tree, Lark

class Transformer(object):
    def __init__(self):
        self.mapping = {"add": "+", "mul":"*", "sub": "-", "div": "/", "power": "**", 
                        "and_test": "∧", "or_test": "∨"}
        

    def transform(self, tree):
        op = tree.data

        if op in {"add", "mul", "sub", "div", "power", "and_test", "or_test"}:
            lhs = self.transform(tree.children[0])
            rhs = self.transform(tree.children[1])
            return "(" + lhs + self.mapping[op] + rhs + ")"
        elif op == "number":
            return str(int(tree.children[0]))
        elif op == "var":
            return tree.children[0]
        elif op == "not":
            return "¬" + self.transform(tree.children[0])
        elif op == "const_true":
            return "true"
        elif op == "const_false":
            return "false"
        elif op == "assign":
            variable = tree.children[0].children[0]
            value = self.transform(tree.children[1])
            return variable + " := " + value
        elif op == "sequence":
            children_num = len(tree.children)
            tmp = ""
            for i in range(children_num):
                if i != children_num - 1:
                    tmp += self.transform(tree.children[i]) + "; "
                else:
                    tmp += self.transform(tree.children[i])
            return tmp
        elif op == "comparison":
            lhs = self.transform(tree.children[0])
            relation = tree.children[1]
            rhs = self.transform(tree.children[2])
            return "(" + lhs + relation + rhs + ")"
        elif op in {"compound_while", "simple_while"}:
            cond = self.transform(tree.children[0])
            command = self.transform(tree.children[1])
            return "while " + cond + " do { " + command + " }"
        elif op == "if_stmt":
            children_num = len(tree.children)
            cond = self.transform(tree.children[0])
            command_1 = self.transform(tree.children[1])
            command_2 = self.transform(tree.children[2])
            return "if " + cond + " then { " + command_1 + " } else { " + command_2 + " }"
        elif op == "simple_stmt":
            command_1 = self.transform(tree.children[0])
            command_2 = self.transform(tree.children[1])
            return command_1 + "; " + command_2
# following codes only for debuggine
# text = "{ a := 1 ; b := 2 }\n"
# while_parser = Lark.open('WHILE.lark', parser='lalr')
# tree = while_parser.parse(text)
# trans = Transformer()
# print(trans.transform(tree))
