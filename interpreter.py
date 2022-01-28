from termcolor import colored
import ast
import sys

from exceptions import BreakException, ContinueException, ReturnException, ReturnValueException
from memory import Memory, MemoryStack
from visit import on, when

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory("Global"))

    @on('node')
    def visit(self, node):
        pass

    @when(ast.DoubleInstruction)
    def visit(self, node):
        node.left.accept(self)
        node.right.accept(self)

    @when(ast.TabDeclaration)
    def visit(self, node):
        name = node.id.value
        size = node.size.accept(self)
        if node.type == 'int':
            self.memory_stack.insert(name, [0 for _ in range(size)])
        elif node.type == 'float':
            self.memory_stack.insert(name, [0.0 for _ in range(size)])
        elif node.type == 'char' or node.type == 'string':
            self.memory_stack.insert(name, ['' for _ in range(size)])
        elif node.type == 'bool':
            self.memory_stack.insert(name, [False for _ in range(size)])
        return name

    @when(ast.AssignCreateInstruction)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        if node.left.type == 'string':
            right = right.replace('"', '')
        self.memory_stack.set(left, right)
        self.debug_message(left + ' = ' + str(right))
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)

    @when(ast.AssignInstruction)
    def visit(self, node):
        left = node.id.value
        left_value = node.id.accept(self)
        right = node.right.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        if type(node.id) == 'string':
            right = right.replace(right, '"', '')
        if node.op == '=':
            self.memory_stack.set(left, right)
        elif node.op == '+=':
            self.memory_stack.set(left, left_value + right)
        elif node.op == '-=':
            self.memory_stack.set(left, left_value - right)
        elif node.op == '*=':
            self.memory_stack.set(left, left_value * right)
        elif node.op == '/=':
            self.memory_stack.set(left, left_value / right)
        self.debug_message(left + node.op + str(right))
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)

    @when(ast.AssignInstructionDoubleOp)
    def visit(self, node):
        left = node.id.value
        left_value = node.id.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        if node.op == '++':
            self.memory_stack.set(left, left_value + 1)
        elif node.op == '--':
            self.memory_stack.set(left, left_value - 1)
        self.debug_message(left + node.op)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)

    @when(ast.AssignCreateInstructionUnary)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        self.memory_stack.set(left, -right)
        self.debug_message(left + ' = ' + str(-right))
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)

    @when(ast.AssignInstructionUnary)
    def visit(self, node):
        left = node.id.value
        right = node.right.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        self.memory_stack.set(left, -right)
        self.debug_message(left + ' = ' + str(-right))
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)

    @when(ast.AssignInstructionTab)
    def visit(self, node):
        left = node.id.value
        index = node.index.accept(self)
        left_value = node.id.accept(self)
        right = node.expr.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        if type(node.id) == 'string':
            right = right.replace(right, '"', '')
        if node.op == '=':
            self.memory_stack.set(left, right, index=index)
        elif node.op == '+=':
            self.memory_stack.set(left, left_value + right, index=index)
        elif node.op == '-=':
            self.memory_stack.set(left, left_value - right, index=index)
        elif node.op == '*=':
            self.memory_stack.set(left, left_value * right, index=index)
        elif node.op == '/=':
            self.memory_stack.set(left, left_value / right, index=index)
        self.debug_message(left + node.op + str(right))

    @when(ast.AssignInstructionTabDoubleOp)
    def visit(self, node):
        left = node.id.value
        index = node.index.accept(self)
        left_value = node.id.accept(self)
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        if node.op == '++':
            self.memory_stack.set(left, left_value + 1, index=index)
        elif node.op == '--':
            self.memory_stack.set(left, left_value - 1, index=index)
        self.debug_message(left + node.op)

    @when(ast.IfInstruction)
    def visit(self, node):
        if node.expr.accept(self):
            node.instr.accept(self)

    @when(ast.IfElseInstruction)
    def visit(self, node):
        if node.expr.accept(self):
            node.instr1.accept(self)
        else:
            node.instr2.accept(self)

    @when(ast.WhileInstruction)
    def visit(self, node):
        res = None
        while_mem = Memory("while")
        self.memory_stack.push(while_mem)
        while node.expr.accept(self):
            try:
                res = node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        return res

    @when(ast.ForInstruction)
    def visit(self, node):
        res = None
        for_mem = Memory('for')
        self.memory_stack.push(for_mem)
        node.assign_beg.accept(self)
        while node.expr.accept(self):
            try:
                res = node.instr.accept(self)
                node.assign_end.accept(self)
            except BreakException:
                break
            except ContinueException:
                node.assign_end.accept(self)
                continue
        self.memory_stack.pop()
        # for i in range(self.memory_stack.elements):
        #     mem = self.memory_stack.content[i]
        #     print(mem.name)
        #     for item in mem.variables.items():
        #         print(item)
        return res

    @when(ast.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(ast.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(ast.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(None)

    @when(ast.ReturnInstructionExpression)
    def visit(self, node):
        raise ReturnValueException(node.expr.accept(self))

    @when(ast.PrintInstruction)
    def visit(self, node):
        text = node.string.accept(self)
        for i in range(1, len(text) - 1):
            if text[i] == '\\' and text[i+1] == 'n':
                print()
            elif text[i] != '\\' and text[i-1] != '\\':
                print(text[i], end='')

    @when(ast.PrintInstructionArgs)
    def visit(self, node):
        text = node.string.accept(self)

        tmp = node.args
        args = []
        while isinstance(tmp, ast.IdsList) or isinstance(tmp, ast.IdsListTab):
            args = [tmp.id.accept(self)] + args
            tmp = tmp.args
        args = [tmp.accept(self)] + args
        args_counter = 0
        for i in range(1, len(text) - 1):
            c = text[i]
            if i > 0 and text[i-1] != '%':  # pomijam znak po %
                if c != '%':
                    if text[i] == '\\' and text[i + 1] == 'n':
                        print()
                    elif text[i] != '\\' and text[i - 1] != '\\':
                        print(c, end='')
                else:
                    print(args[args_counter], end='')
                    args_counter += 1

    @when(ast.IdsList)
    def visit(self, node):
        node.id.accept(self)
        node.args.accept(self)

    @when(ast.TabID)
    def visit(self, node):
        name = node.id.value
        index = node.index.accept(self)
        value = self.memory_stack.get(name, index)
        return value

    @when(ast.IdsListTab)
    def visit(self, node):
        node.args.accept(self)
        node.tabID.accept(self)

    @when(ast.Expression)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if type(left) == 'float':
                return left / right
            else:
                return left // right
        elif node.op == '%':
            return left % right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == '!=':
            return left != right
        elif node.op == '==':
            return left == right
        self.debug_message(left + node.op + right)

    @when(ast.Variable)
    def visit(self, node):
        var_name = node.name
        if node.type == 'int' or node.type == 'float':
            self.memory_stack.insert(var_name, 0)
        elif node.type == 'char' or node.type == 'string':
            self.memory_stack.insert(var_name, '')
        elif node.type == 'bool':
            self.memory_stack.insert(var_name, False)
        return node.name

    @when(ast.Boolean)
    def visit(self, node):
        if node.value == 'true':
            return True
        return False

    @when(ast.IntNum)
    def visit(self, node):
        return node.value

    @when(ast.FloatNum)
    def visit(self, node):
        return node.value

    @when(ast.Char)
    def visit(self, node):
        return node.value

    @when(ast.String)
    def visit(self, node):
        return node.value

    @when(ast.ID)
    def visit(self, node):
        name = node.value
        value = self.memory_stack.get(name)
        return value

    @when(ast.DoubleFunction)
    def visit(self, node):
        node.left.accept(self)
        if node.right.variable.name == "main":  # Wykonaj tylko main, a reszte funkcji przy ich wywołaniu
            node.right.accept(self)

    @when(ast.Function)
    def visit(self, node):
        name = node.variable.accept(self)
        fun_mem = Memory(name)
        self.memory_stack.push(fun_mem)
        tmp = node.args
        while isinstance(tmp, ast.DoubleVariable):
            tmp.right.accept(self)  # od razu doda do pamięci zmienną i da jej wartosc None
            tmp = tmp.left
        node.instr.accept(self)
        self.memory_stack.pop()

    @when(ast.EmptyFunction)
    def visit(self, node):
        name = node.variable.accept(self)
        fun_mem = Memory(name)
        self.memory_stack.push(fun_mem)
        try:
            node.instr.accept(self)
        except ReturnValueException:
            return
        self.memory_stack.pop()

    @when(ast.DoubleVariable)
    def visit(self, node):
        node.left.accept(self)
        node.right.accept(self)

    @staticmethod
    def debug_message(message):
        # print(colored(message, 'blue'))
        pass
