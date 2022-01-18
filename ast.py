class Node:
    def accept(self, visitor):
        return visitor.visit(self)


class DoubleInstruction(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)


class TabDeclaration(Node):
    def __init__(self, type, id, expr):
        self.type = type
        self.id = id
        self.size = expr

    def printTree(self, indent=0):
        print("| " * indent + "TAB")
        print("| " * (indent + 1) + self.id.value)
        self.size.printTree(indent + 1)


class AssignCreateInstruction(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + '=')
        self.left.printTree(indent+1)
        self.right.printTree(indent + 1)


class AssignInstruction(Node):
    def __init__(self, left, op, right, lineno):
        self.id = left
        self.op = op
        self.right = right
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent+1) + self.id.value)
        self.right.printTree(indent + 1)


class AssignInstructionDoubleOp(Node):
    def __init__(self, id, op, lineno):
        self.id = id
        self.op = op
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + self.id.value)


class AssignCreateInstructionUnary(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + '=')
        self.left.printTree(indent+1)
        print("| " * (indent + 1) + '-')
        self.right.printTree(indent + 2)


class AssignInstructionUnary(Node):
    def __init__(self, id, right, lineno):
        self.id = id
        self.right = right
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + '=')
        print("| " * (indent + 1) + self.id.value)
        print("| " * (indent + 1) + '-')
        self.right.printTree(indent + 2)


class AssignInstructionTab(Node):
    def __init__(self, id, index, op, expr, lineno):
        self.id = id
        self.index = index
        self.op = op
        self.expr = expr
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + "TAB")
        print("| " * (indent + 2) + self.id.value)
        self.index.printTree(indent + 2)
        self.expr.printTree(indent + 1)


class AssignInstructionTabDoubleOp(Node):
    def __init__(self, id, index, op, lineno):
        self.id = id
        self.index = index
        self.op = op
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + "TAB")
        print("| " * (indent + 2) + self.id.value)
        self.index.printTree(indent + 2)


class IfInstruction(Node):
    def __init__(self, expr, instr):
        self.expr = expr
        self.instr = instr

    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr.printTree(indent + 1)


class IfElseInstruction(Node):
    def __init__(self, expr, ifinstr, elseinstr):
        self.expr = expr
        self.instr1 = ifinstr
        self.instr2 = elseinstr

    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr1.printTree(indent + 1)
        print("| " * indent + "ELSE")
        self.instr2.printTree(indent + 1)


class WhileInstruction(Node):
    def __init__(self, expr, instr):
        self.expr = expr
        self.instr = instr

    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expr.printTree(indent + 1)
        self.instr.printTree(indent + 1)


class ForInstruction(Node):
    def __init__(self, assign_beg, expr, assign_end, instr):
        self.assign_beg = assign_beg
        self.expr = expr
        self.assign_end = assign_end
        self.instr = instr

    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        print("| " * (indent+1) + "INIT_COND")
        self.assign_beg.printTree(indent+2)
        print("| " * (indent + 1) + "END_COND")
        self.expr.printTree(indent + 2)
        print("| " * (indent+1) + "STEP")
        self.assign_end.printTree(indent+2)
        print("| " * (indent+1) + "INSTR")
        self.instr.printTree(indent+2)


class BreakInstruction(Node):
    def __init__(self, lineno):
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "BREAK")


class ContinueInstruction(Node):
    def __init__(self, lineno):
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "CONTINUE")


class ReturnInstruction(Node):
    def __init__(self, lineno):
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "RETURN")


class ReturnInstructionExpression(Node):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "RETURN")
        self.expr.printTree(indent + 1)


class PrintInstruction(Node):
    def __init__(self, string, lineno):
        self.string = string
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.string.printTree(indent + 1)


class PrintInstructionArgs(Node):
    def __init__(self, string, ids, lineno):
        self.string = string
        self.args = ids
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.string.printTree(indent + 1)
        self.args.printTree(indent + 1)


class IdsList(Node):
    def __init__(self, ids, id):
        self.id = id
        self.args = ids

    def printTree(self, indent=0):
        self.id.printTree(indent)
        self.args.printTree(indent)


class TabID(Node):
    def __init__(self, id, index, line):
        self.id = id
        self.index = index
        self.line = line

    def printTree(self, indent=0):
        print("| " * indent + "TAB")
        print("| " * (indent + 1) + self.id.value)
        self.index.printTree(indent + 1)


class IdsListTab(Node):
    def __init__(self, ids, tab_id):
        self.args = ids
        self.tabID = tab_id

    def printTree(self, indent=0):
        self.tabID.printTree(indent)
        self.args.printTree(indent)


class Expression(Node):
    def __init__(self, expression1, op, expression2, lineno):
        self.left = expression1
        self.op = op
        self.right = expression2
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


class Variable(Node):
    def __init__(self, vartype, name, lineno):
        self.type = vartype
        self.name = name
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.name)
        print("| " * (indent+1) + self.type)


class Boolean(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=0):
        print("| " * indent + self.value)


class IntNum(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=0):
        print("| " * indent + str(self.value))


class FloatNum(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=0):
        print("| " * indent + str(self.value))


class Char(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=0):
        print("| " * indent + self.value)


class String(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=0):
        print("| " * indent + self.value)


class ID(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.line = lineno

    def printTree(self, indent=0):
        print("| " * indent + self.value)


class DoubleFunction(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)


class Function(Node):
    def __init__(self, variable, args, instr):
        self.variable = variable
        self.args = args
        self.instr = instr

    def printTree(self, indent=0):
        self.variable.printTree(indent)
        print("| " * (indent+1) + 'ARGS')
        self.args.printTree(indent+2)
        print("| " * (indent+1) + 'INSTR')
        self.instr.printTree(indent+2)


class EmptyFunction(Node):
    def __init__(self, variable, instr):
        self.variable = variable
        self.instr = instr

    def printTree(self, indent=0):
        self.variable.printTree(indent)
        print("| " * (indent + 1) + 'INSTR')
        self.instr.printTree(indent + 2)


class DoubleVariable(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)


class Error(Node):
    def __init__(self):
        pass

    def printTree(self, indent=0):
        pass
