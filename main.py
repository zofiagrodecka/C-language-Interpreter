import scanner
import myparser
from interpreter import Interpreter
from type_checker import TypeChecker
import sys

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Run program with a file name to be interpreted")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        parser = myparser.parser
        text = f.read()
        ast = parser.parse(text, lexer=scanner.lexer)
        # if ast is not None:
        #     ast.printTree()
        if not myparser.error:
            type_checker = TypeChecker()
            type_checker.visit(ast)
            if not type_checker.error:
                ast.accept(Interpreter())
