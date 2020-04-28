
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

from collections import OrderedDict

class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.state = {}

    def interp(self, tree):
        op = tree.data

        # Binary operations
        if op in {"add", "mul", "sub", "div", "power"}:
            lhs = self.interp(tree.children[0])
            rhs = self.interp(tree.children[1])
            if op == 'add':
                return lhs + rhs
            elif op == 'sub':
                return lhs - rhs
            elif op == 'mul':
                return lhs * rhs
            elif op == 'div':
                return lhs / rhs
            elif op == "power":
                return lhs ** rhs
        # visit number
        elif op == "number":
            return int(tree.children[0])
        # visit variable
        elif op == "var":
            return self.lookup(tree.children[0])
        # var or array assignment
        elif op == "assign":
            variable = tree.children[0].children[0]
            value = self.interp(tree.children[1])
            self.state[variable] = value
        # comparison
        elif op == "comparison":
            lhs = self.interp(tree.children[0])
            relation = tree.children[1]
            rhs = self.interp(tree.children[2])
            return self.compare(lhs, relation, rhs)
        # while statement
        elif op == "simple_while":
            cond = self.interp(tree.children[0])
            if cond == 1:
                self.interp(tree.children[1])
                self.interp(tree)
            elif not cond and tree.children[1].data == "simple_stmt":
                self.interp(tree.children[1].children[1])
            else:
                return
        elif op == "compound_while":
            cond = self.interp(tree.children[0])
            if cond == 1:
                self.interp(tree.children[1])
                self.interp(tree)
            else:
                return
        # if statement
        elif op == "if_stmt":
            children_num = len(tree.children)
            cond = self.interp(tree.children[0])
            if cond:
                self.interp(tree.children[1])
            elif not cond and children_num == 3:
                self.interp(tree.children[2])
            return 
        # skip statement
        elif op == "skip_stmt":
            return 
        # simple statement
        elif op == "simple_stmt":
            self.interp(tree.children[0])
            self.interp(tree.children[1])
            return
        # not
        elif op == "not":
            return 1 if not self.interp(tree.children[0]) else 0
        # const_false
        elif op == "const_false":
            return 0
        elif op == "const_true":
            return 1
        # or, and
        elif op == "or_test":
            lhs = self.interp(tree.children[0])
            rhs = self.interp(tree.children[1])
            return lhs or rhs
        elif op == "and_test":
            lhs = self.interp(tree.children[0])
            rhs = self.interp(tree.children[1])
            return lhs and rhs
        elif op == "ternary_assign":
            variable = tree.children[0].children[0]
            cond = self.interp(tree.children[1])
            if cond:
                self.state[variable] = self.interp(tree.children[2])
            else:
                self.state[variable] = self.interp(tree.children[3])
            return
        # array
        elif op == "array":
            array = self.interp(tree.children[0])
            return array
        elif op == "testlist_comp":
            children_num = len(tree.children)
            elems = []
            for i in range(children_num):
                elems.append(self.interp(tree.children[i]))
            return elems
        # accept arguments
        elif op == 'arguments':
            children_num = len(tree.children)
            args = []
            for i in range(children_num):
                args.append(self.interp(tree.children[i]))
            return args
        # get items in array
        elif op == "getitem":
            variable = tree.children[0].children[0]
            subscripts = self.interp(tree.children[1])
            return self.state[variable][subscripts[0]]
        elif op == "subscriptlist":
            children_num = len(tree.children)
            _subscripts = []
            for i in range(children_num):
                _subscripts.append(self.interp(tree.children[i]))
            return _subscripts
        elif op == "subscript":
            return self.interp(tree.children[0])


    def compare(self, left, relation, right):
        if relation == "=":
            return left == right
        elif relation == "<":
            return left < right
        elif relation == ">":
            return left > right

    def lookup(self, v):
        if v in self.state:
            return self.state[v]
        else:
            return 0
    
    def print_Result(self):
        od = OrderedDict(sorted(self.state.items()))
        ans = ", ".join(str(var) + " → " + str(value) for var, value in od.items())
        return "{" + ans + "}"

    def interpret(self, text):
        tree = self.parser.parse(text)
        self.interp(tree)
        return self.print_Result()


