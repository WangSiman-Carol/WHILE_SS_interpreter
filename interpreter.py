
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

from collections import OrderedDict
from ast_transformer import *
import sys

sys.setrecursionlimit(100020)
class Interpreter():
    def __init__(self, parser):
        self.parser = parser
        self.state = {}
        self.result = []
        self.while_counter = 0
        self.transformer = Transformer()
        

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
            # ---------------------------------------------------------------------------------------
            # assign: result = skip, state(new!)
            # temp_result = "skip"
            # ---------------------------------------------------------------------------------------
            variable = tree.children[0].children[0]
            value = self.interp(tree.children[1])
            self.state[variable] = value
            temp_result = "skip, " + self.print_States()
            self.result.append(temp_result)
        # comparison
        elif op == "comparison":
            lhs = self.interp(tree.children[0])
            relation = tree.children[1]
            rhs = self.interp(tree.children[2])
            return self.compare(lhs, relation, rhs)
        # while statement
        elif op == "simple_while":
            # a = self.transformer.transform(tree)

            #check while loop times
            if self.while_counter <= 9999/3-1:
                self.while_counter += 1
            else:
                temp_result = self.transformer.transform(tree.children[1]) + "; " + self.transformer.transform(tree) + ", " + self.print_States()
                self.result.append(temp_result)
                return
            cond = self.interp(tree.children[0])

        
            if cond == 1:
                # ---------------------------------------------------------------------------------------
                # while true: result = c ; command, state
                # temp_result = transformer(tree.children[1]) + transformer(tree) + self.print_States()
                # self.result.append(temp_result)
                # ---------------------------------------------------------------------------------------
                #Get currect result
                
                temp_result = self.transformer.transform(tree.children[1]) + "; " + self.transformer.transform(tree) + ", " + self.print_States()
                self.result.append(temp_result)

                #mark before results
                before_result_length = len(self.result)
                
                #Execute command
                self.interp(tree.children[1])

                for i in range(before_result_length,len(self.result)):
                    modify_comm = self.result[i]
                    length_modify = len(modify_comm.split(","))
                    temp_result = modify_comm.split(",")[0] + "; " + self.transformer.transform(tree)
                    for j in range(1,length_modify):
                        temp_result += ',' + modify_comm.split(",")[j]
                    self.result[i] = temp_result

                ###################


                # #Execute command
                # self.interp(tree.children[1])

                # #Get result after command 
                # modify_comm = self.result.pop()

                # length_modify = len(modify_comm.split(","))
                # temp_result = modify_comm.split(",")[0] + "; " + self.transformer.transform(tree)
                # for i in range(1,length_modify):
                #     temp_result += ',' + modify_comm.split(",")[i]
                    
                # self.result.append(temp_result)


                #################

                #Manually make skip;while --> while
                temp_result = self.transformer.transform(tree) + ", " + self.print_States()
                self.result.append(temp_result)


                self.interp(tree)
            elif not cond and tree.children[1].data == "simple_stmt":
                # ---------------------------------------------------------------------------------------
                # while false: result = skip ; following commands, state
                # temp_result = "skip" + transformer(tree.children[1].children[1]) + self.print_States()
                # self.result.append(temp_result)
                # ---------------------------------------------------------------------------------------
                temp_result = "skip; " + self.transformer.transform(tree.children[1].children[1]) + ", " + self.print_States()
                self.result.append(temp_result)

                #Manually make skip;comm --> comm
                temp_result = self.transformer.transform(tree.children[1].children[1]) + ", " + self.print_States()
                self.result.append(temp_result)

                self.interp(tree.children[1].children[1])
            else:
                # temp_result = "skip, " + "next comm from trans, " + self.print_States()
                temp_result = "skip, " + self.print_States() 
                self.result.append(temp_result)
                return
        elif op == "compound_while":

            #check while loop times
            if self.while_counter <= 10000:
                self.while_counter += 1
            else:
                return

            cond = self.interp(tree.children[0])
            if cond == 1:
                #Get currect result
                
                temp_result = self.transformer.transform(tree.children[1]) + "; " + self.transformer.transform(tree) + ", " + self.print_States()
                self.result.append(temp_result)
                
                #mark before results
                before_result_length = len(self.result)
                
                #Execute command
                self.interp(tree.children[1])

                for i in range(before_result_length,len(self.result)):
                    modify_comm = self.result[i]
                    length_modify = len(modify_comm.split(","))
                    temp_result = modify_comm.split(",")[0] + "; " + self.transformer.transform(tree)
                    for j in range(1,length_modify):
                        temp_result += ',' + modify_comm.split(",")[j]
                    self.result[i] = temp_result

                #Manually make skip;while --> while
                temp_result = self.transformer.transform(tree) + ", " + self.print_States()
                self.result.append(temp_result)
                self.interp(tree)
            else:
                temp_result = "skip, " + self.print_States()
                self.result.append(temp_result)
                return




        # if statement
        elif op == "if_stmt":
            children_num = len(tree.children)
            cond = self.interp(tree.children[0])
            if cond:
                
                temp_result = self.transformer.transform(tree.children[1]) + ", " + self.print_States()
                self.result.append(temp_result)
                self.interp(tree.children[1])
            elif not cond and children_num == 3:
                temp_result = self.transformer.transform(tree.children[2]) + ", " + self.print_States()
                self.result.append(temp_result)
                self.interp(tree.children[2])
            return 
        # skip statement
        elif op == "skip_stmt":
            self.result.append(' ,'+self.print_States())
            return 
        # simple statement
        elif op == "simple_stmt":
            # C1; C2
            # Change C1 --> C1; C2
        
            before_result_length = len(self.result)
            self.interp(tree.children[0])
            for i in range(before_result_length,len(self.result)):
                modify_comm = self.result[i]
                length_modify = len(modify_comm.split(","))
                temp_result = modify_comm.split(",")[0] + "; " + self.transformer.transform(tree.children[1])
                for j in range(1,length_modify):
                    temp_result += ',' + modify_comm.split(",")[j]
                self.result[i] = temp_result

            # manually print C2
            temp_result = self.transformer.transform(tree.children[1]) + ", " + self.print_States()
            self.result.append(temp_result)

            self.interp(tree.children[1])
            
            return
        # compound statement, specifically for sequence of assignments
        elif op == "compound_stmt":
            #mark initial results
            before_result_length = len(self.result)

            #execute the command
            self.interp(tree.children[0])

            #modify the reuslts
            for i in range(before_result_length,len(self.result)):
                modify_comm = self.result[i]
                length_modify = len(modify_comm.split(","))
                temp_result = modify_comm.split(",")[0] + "; " + self.transformer.transform(tree.children[1])
                for j in range(1,length_modify):
                    temp_result += ',' + modify_comm.split(",")[j]
                self.result[i] = temp_result

            # manually print C2
            temp_result = self.transformer.transform(tree.children[1]) + ", " + self.print_States()
            self.result.append(temp_result)

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
        # sequence of assignments
        elif op == "sequence":
            children_num = len(tree.children)
            
            #process all the children except the last one
            for i in range(children_num-1):

                #find other comm
                before_result_length = len(self.result)
                other_comm_num = children_num - i - 1
                other_comm_str = ""
                for other_comm in range(other_comm_num):
                    if other_comm == other_comm_num -1:
                        other_comm_str += self.transformer.transform(tree.children[i+other_comm+1])
                    else:
                        other_comm_str += self.transformer.transform(tree.children[i+other_comm+1]) + "; "

                # Execute current
                self.interp(tree.children[i])

                #Add other comm
                for k in range(before_result_length,len(self.result)):
                    modify_comm = self.result[k]
                    length_modify = len(modify_comm.split(","))
                    temp_result = modify_comm.split(",")[0] + "; " + other_comm_str
                    for j in range(1,length_modify):
                        temp_result += ',' + modify_comm.split(",")[j]
                    self.result[k] = temp_result

                # manually print C2
                temp_result = other_comm_str + ", " + self.print_States()
                self.result.append(temp_result)
            
            #process the last child
            self.interp(tree.children[children_num-1])
            


                


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

    def print_States(self):
        od = OrderedDict(sorted(self.state.items()))
        ans = ", ".join(str(var) + " → " + str(value) for var, value in od.items())
        return "{" + ans + "}"

    def print_Results(self):
        for item in self.result:
            if item != " ,{}":
                print("⇒",item)

    def interpret(self, text):
        tree = self.parser.parse(text)
        # print(tree.pretty())
 
        self.interp(tree)
        self.print_Results() 

        
        return self.print_States()

