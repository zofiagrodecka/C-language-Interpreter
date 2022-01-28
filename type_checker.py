from collections import defaultdict

import ast
from symbol_table import SymbolTable
from termcolor import colored


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.error = False
        self.symbols = SymbolTable(None, 'SYMBOL_TABLE')
        self.depth = 0
        self.fun_type = None
        self.arrays_sizes = {}
        self.ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

        self.ttype['+']['int']['int'] = 'int'
        self.ttype['+']['float']['float'] = 'float'

        self.ttype['-']['int']['int'] = 'int'
        self.ttype['-']['float']['float'] = 'float'

        self.ttype['*']['int']['int'] = 'int'
        self.ttype['*']['float']['float'] = 'float'

        self.ttype['/']['int']['int'] = 'int'
        self.ttype['/']['float']['float'] = 'float'

        self.ttype['%']['int']['int'] = 'int'
        self.ttype['%']['float']['float'] = 'float'

        self.ttype['==']['int']['int'] = 'int'
        self.ttype['==']['float']['float'] = 'float'
        self.ttype['==']['bool']['bool'] = 'bool'

        self.ttype['!=']['int']['int'] = 'int'
        self.ttype['!=']['float']['float'] = 'float'
        self.ttype['!=']['bool']['bool'] = 'bool'

        self.ttype['>']['int']['int'] = 'int'
        self.ttype['>']['float']['float'] = 'float'
        self.ttype['>']['bool']['bool'] = 'bool'

        self.ttype['<']['int']['int'] = 'int'
        self.ttype['<']['float']['float'] = 'float'
        self.ttype['<']['bool']['bool'] = 'bool'

        self.ttype['<=']['int']['int'] = 'int'
        self.ttype['<=']['float']['float'] = 'float'
        self.ttype['<=']['bool']['bool'] = 'bool'

        self.ttype['>=']['int']['int'] = 'int'
        self.ttype['>=']['float']['float'] = 'float'
        self.ttype['>=']['bool']['bool'] = 'bool'

    def visit_DoubleInstruction(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_TabDeclaration(self, node):
        type = node.type
        name = node.id.value
        size = node.size
        self.arrays_sizes[name] = size
        self.symbols.put(name, type)
        return type

    def visit_AssignCreateInstruction(self, node):
        left_type = self.visit(node.left)  # variable
        left_name = node.left.name
        right_type = self.visit(node.right)
        if left_type is not None and left_type != right_type:
            self.print_error(node.line, "Incorect types: " + left_type + " and " + right_type)
        else:
            self.symbols.put(left_name, left_type)

    def visit_AssignInstruction(self, node):
        left_type = self.visit(node.id)
        left_name = node.id.value
        right_type = self.visit(node.right)
        if left_type is None:
            self.print_error(node.line, "Undeclared variable: " + left_name)
        elif left_type != right_type:
            self.print_error(node.line, "Incorect types: " + left_type + " and " + right_type)

    def visit_AssignInstructionDoubleOp(self, node):
        left_type = self.visit(node.id)
        left_name = node.id.value
        if left_type is None:
            self.print_error(node.line, "Undeclared variable: " + left_name)

    def visit_AssignCreateInstructionUnary(self, node):
        left_type = self.visit(node.left)
        left_name = node.left.name
        right_type = self.visit(node.right)
        if left_type is not None and left_type != right_type:
            self.print_error(node.line, "Incorect types: " + left_type + " and " + right_type)
        else:
            self.symbols.put(left_name, left_type)

    def visit_AssignInstructionUnary(self, node):
        left_type = self.visit(node.id)
        left_name = node.id.value
        right_type = self.visit(node.right)
        if left_type is None:
            self.print_error(node.line, "Undeclared variable: " + left_name)
        elif left_type != right_type:
            self.print_error(node.line, "Incorect types: " + left_type + " and " + right_type)

    def visit_AssignInstructionTab(self, node):
        left_type = self.visit(node.id)
        tab_name = node.id.value
        right_type = self.visit(node.expr)
        index_type = self.visit(node.index)
        if index_type != 'int':
            self.print_error(node.line, "Incorrect type: " + index_type)
        elif self.symbols.get(tab_name) is None:
            self.print_error(node.line, "Undeclared variable: " + tab_name)
        elif left_type != right_type:
            self.print_error(node.line, "Incorect types: " + left_type + " and " + right_type)

    def visit_AssignInstructionTabDoubleOp(self, node):
        tab_name = node.id.value
        index_type = self.visit(node.index)
        if index_type != 'int':
            self.print_error(node.line, "Incorrect type: " + index_type)
        elif self.symbols.get(tab_name) is None:
            self.print_error(node.line, "Undeclared variable: " + tab_name)

    def visit_IfInstruction(self, node):
        self.visit(node.expr)
        self.symbols = self.symbols.pushScope('if')
        self.visit(node.instr)
        self.symbols = self.symbols.popScope()

    def visit_IfElseInstruction(self, node):
        self.visit(node.expr)
        self.symbols = self.symbols.pushScope("if")
        self.visit(node.instr1)
        self.symbols = self.symbols.popScope()
        self.symbols = self.symbols.pushScope("else")
        self.visit(node.instr2)
        self.symbols = self.symbols.popScope()

    def visit_WhileInstruction(self, node):
        self.depth += 1
        self.symbols = self.symbols.pushScope("while")
        self.visit(node.expr)
        self.visit(node.instr)
        self.symbols = self.symbols.popScope()
        self.depth -= 1

    def visit_ForInstruction(self, node):
        self.depth += 1
        self.symbols = self.symbols.pushScope("for")
        self.visit(node.assign_beg)
        self.visit(node.expr)
        self.visit(node.assign_end)
        self.visit(node.instr)
        self.symbols = self.symbols.popScope()
        self.depth -= 1

    def visit_BreakInstruction(self, node):
        if self.depth <= 1:
            self.print_error(node.line, "break outside loop")

    def visit_ContinueInstruction(self, node):
        if self.depth <= 1:
            self.print_error(node.line, "continue outside loop")

    def visit_ReturnInstruction(self, node):
        if self.depth <= 0:
            self.print_error(node.line, "return outside function")
        elif self.fun_type != 'void':
            self.print_error(node.line, "Incorrect return type")

    def visit_ReturnInstructionExpression(self, node):
        return_type = self.visit(node.expr)
        if self.depth <= 0:
            self.print_error(node.line, "return outside function")
        elif self.fun_type != return_type:
            self.print_error(node.line, "Incorrect return type")

    def visit_PrintInstruction(self, node):
        t = self.visit(node.string)
        if t != 'string':
            self.print_error(node.line, "Incorrect type: " + t)

    def visit_PrintInstructionArgs(self, node):
        t = self.visit(node.string)
        str_val = node.string.value
        expected_n_args = str_val.count('%')
        if t != 'string':
            self.print_error(node.line, "Incorrect type: " + t)

        expected_types = []
        for i in range(len(str_val)):
            c = str_val[i]
            if c == '%':
                expected = str_val[i+1]
                if str_val[i+1] == 'c':
                    expected = 'char'
                elif str_val[i+1] == 's':
                    expected = 'string'
                elif str_val[i+1] == 'd':
                    expected = 'int'
                elif str_val[i+1] == 'f':
                    expected = 'float'
                else:
                    self.print_error(node.line, "Nonexistent printf type: " + expected)
                expected_types.append(expected)

        tmp = node.args
        size = 1
        argtypes = []
        while isinstance(tmp, ast.IdsList) or isinstance(tmp, ast.IdsListTab):
            size += 1
            argtypes = [self.visit(tmp.id)] + argtypes
            tmp = tmp.args
        if isinstance(tmp, ast.TabID):
            argtypes = [self.visit(tmp.id)] + argtypes
        else:
            argtypes = [self.visit(tmp)] + argtypes
        if size != expected_n_args:
            self.print_error(node.line, "Wrong number of parameters in printf function: " + str(size))
        else:
            for i in range(len(argtypes)):
                if argtypes[i] != expected_types[i]:
                    self.print_error(node.line, "Incorrect type: " + argtypes[i])

    def visit_IdsList(self, node):
        self.visit(node.id)
        self.visit(node.args)

    def visit_TabID(self, node):
        index = self.symbols.get(node.index.value)
        tab_name = node.id.value
        index_type = self.visit(node.index)
        if index_type != 'int':
            self.print_error(node.line, "Incorrect type: " + index_type)
        return self.symbols.get(tab_name)

    def visit_IdsListTab(self, node):
        self.visit(node.id)
        self.visit(node.index)
        self.visit(node.args)

    def visit_Expression(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op
        t = self.ttype[op][left_type][right_type]
        if t is None:
            self.print_error(node.line, "Incorrect types: " + left_type + " and " + right_type)
            return None
        return t

    def visit_Variable(self, node):
        var_type = node.type
        var_name = node.name
        if self.symbols.get(var_name):
            self.print_error(node.line, "Redeclared: " + var_name)
            return None
        self.symbols.put(var_name, var_type)
        return var_type

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_Boolean(self, node):
        return 'bool'

    def visit_Char(self, node):
        return 'char'

    def visit_String(self, node):
        return 'string'

    def visit_ID(self, node):
        return self.symbols.get(node.value)

    def visit_DoubleFunction(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Function(self, node):
        fun_type = self.visit(node.variable)
        self.fun_type = fun_type
        self.depth += 1
        self.symbols = self.symbols.pushScope("function")
        self.visit(node.instr)
        self.symbols = self.symbols.popScope()
        self.depth -= 1

    def visit_EmptyFunction(self, node):
        fun_type = self.visit(node.variable)
        self.fun_type = fun_type
        self.depth += 1
        self.symbols = self.symbols.pushScope("function")
        self.visit(node.instr)
        self.symbols = self.symbols.popScope()
        self.depth -= 1

    def visit_DoubleVariable(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def print_error(self, line, text):
        print(colored(text + ' in line: ' + str(line), 'red'))
        self.error = True
