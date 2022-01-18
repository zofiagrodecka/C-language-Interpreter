from __future__ import print_function
import ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(ast.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(ast.DoubleInstruction)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(ast.AssignCreateInstruction)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent+1)
        self.right.printTree(indent + 1)

    @addToClass(ast.AssignInstructionDoubleOp)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + self.id.value)

    @addToClass(ast.AssignCreateInstructionUnary)
    def printTree(self, indent=0):
        print("| " * indent + '=')
        self.left.printTree(indent+1)
        print("| " * (indent + 1) + '-')
        self.right.printTree(indent + 2)

    @addToClass(ast.AssignInstructionTab)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + "TAB")
        print("| " * (indent + 2) + self.id.value)
        self.index.printTree(indent + 2)
        self.expr.printTree(indent + 1)

    @addToClass(ast.AssignInstructionTabDoubleOp)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + "TAB")
        print("| " * (indent + 2) + self.id.value)
        self.index.printTree(indent + 2)

    @addToClass(ast.IfInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr.printTree(indent + 1)

    @addToClass(ast.IfElseInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr1.printTree(indent + 1)
        print("| " * indent + "ELSE")
        self.instr2.printTree(indent + 1)

    @addToClass(ast.WhileInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expr.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(ast.ForInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        print("| " * (indent+1) + "INIT_COND")
        self.assign_beg.printTree(indent+2)
        print("| " * (indent+1) + "END_COND")
        self.assign_end.printTree(indent+2)
        print("| " * (indent+1) + "STEP")
        self.expr.printTree(indent+2)
        print("| " * (indent+1) + "INSTR")
        self.instr.printTree(indent+2)

    @addToClass(ast.BreakInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "BREAK")

    @addToClass(ast.ContinueInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "CONTINUE")

    @addToClass(ast.ReturnInstruction)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")

    @addToClass(ast.ReturnInstructionExpression)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")
        self.expr.printTree(indent + 1)

    @addToClass(ast.Expression)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(ast.Variable)
    def printTree(self, indent=0):
        print("| " * indent + self.type)
        print("| " * indent + self.name)

    @addToClass(ast.Boolean)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(ast.IntNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(ast.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(ast.String)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(ast.ID)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(ast.DoubleFunction)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(ast.Function)
    def printTree(self, indent=0):
        print("| " * indent + 'FUNCTION')
        self.variable.printTree(indent+1)
        print("| " * (indent+1) + 'ARGS')
        self.args.printTree(indent+2)
        print("| " * (indent+1) + 'INSTR')
        self.instr.printTree(indent+2)

    @addToClass(ast.EmptyFunction)
    def printTree(self, indent=0):
        print("| " * indent + 'FUNCTION')
        self.variable.printTree(indent + 1)
        print("| " * (indent + 1) + 'INSTR')
        self.instr.printTree(indent + 2)

    @addToClass(ast.DoubleVariable)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(ast.Error)
    def printTree(self, indent=0):
        pass
