import ply.yacc as yacc
import scanner
import ast

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IF_END'),
    ('nonassoc', 'ELSE'),
    ("right", '=', 'PLUSASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'PLUSPLUS', 'MINUSMINUS'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ('left', 'LESSER_THAN', 'GREATER_THAN', 'LESSER_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'EQUAL')
)

error = False


def p_error(p):
    if p:
        print("Syntax error at line {0}: Token({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")
    global error
    error = True


def p_program(p):
    """program : functions"""
    p[0] = p[1]


def p_instructions_1(p):
    """instructions : instructions instruction"""
    p[0] = ast.DoubleInstruction(p[1], p[2])


def p_instructions_2(p):
    """instructions : instruction"""
    p[0] = p[1]


def p_instruction(p):
    """instruction : declaration
                   | assign_instr
                   | if_instr
                   | while_instr
                   | for_instr
                   | break_instr
                   | continue_instr
                   | return_instr
                   | expression
                   | print_instr"""
    p[0] = p[1]


def p_declaration(p):
    """declaration : variable ';'"""
    p[0] = p[1]


def p_declaration_tab(p):
    """declaration : INT ID '[' expression ']' ';'
                    | FLOAT ID '[' expression ']' ';'
                    | BOOL ID '[' expression ']' ';'
                    | CHARTYPE ID '[' expression ']' ';'
                    | STRINGTYPE ID '[' expression ']' ';'"""
    p[0] = ast.TabDeclaration(p[1], ast.ID(p[2], p.lineno(3)), p[4])


def p_instruction_2(p):
    """instruction : '{' instructions '}' """
    p[0] = p[2]


def p_create_assign_instr(p):
    """assign_instr : variable '=' expression ';'"""
    p[0] = ast.AssignCreateInstruction(p[1], p[3], p.lineno(1))


def p_assign(p):
    """assign : ID '=' expression
              | ID PLUSASSIGN expression
              | ID SUBASSIGN expression
              | ID MULASSIGN expression
              | ID DIVASSIGN expression"""
    p[0] = ast.AssignInstruction(ast.ID(p[1], p.lineno(1)), p[2], p[3], p.lineno(2))


def p_assign_2(p):
    """assign : ID PLUSPLUS
              | ID MINUSMINUS"""
    p[0] = ast.AssignInstructionDoubleOp(ast.ID(p[1], p.lineno(1)), p[2], p.lineno(2))


def p_assign_instr_minus(p):
    """assign_instr : variable '=' '-' expression ';'"""
    p[0] = ast.AssignCreateInstructionUnary(p[1], p[4], p.lineno(2))


def p_assign_minus_2(p):
    """assign : ID '=' '-' expression"""
    p[0] = ast.AssignInstructionUnary(ast.ID(p[1], p.lineno(1)), p[4], p.lineno(2))


def p_assign_instr_tab(p):
    """assign_instr : ID '[' index ']' '=' expression ';'
                    | ID '[' index ']' PLUSASSIGN expression ';'
                    | ID '[' index ']' SUBASSIGN expression ';'
                    | ID '[' index ']' MULASSIGN expression ';'
                    | ID '[' index ']' DIVASSIGN expression ';'"""
    p[0] = ast.AssignInstructionTab(ast.ID(p[1], p.lineno(1)), p[3], p[5], p[6], p.lineno(5))


def p_assign_instr_tab_2(p):
    """assign_instr : ID '[' index ']' PLUSPLUS ';'
                    | ID '[' index ']' MINUSMINUS ';'"""
    p[0] = ast.AssignInstructionTabDoubleOp(ast.ID(p[1], p.lineno(1)), p[3], p[5], p.lineno(5))


def p_index(p):
    """index : expression"""
    p[0] = p[1]


def p_assign_instr(p):
    """assign_instr : assign ';' """
    p[0] = p[1]


def p_if_instr(p):
    """if_instr : IF '(' bool_expr ')' instruction %prec IF_END"""
    p[0] = ast.IfInstruction(p[3], p[5])


def p_if_else_instr(p):
    """if_instr : IF '(' bool_expr ')' instruction ELSE instruction"""
    p[0] = ast.IfElseInstruction(p[3], p[5], p[7])


def p_while_instr(p):
    """while_instr : WHILE '(' expression ')' instruction"""
    p[0] = ast.WhileInstruction(p[3], p[5])


def p_for_instr(p):
    """for_instr : FOR '(' assign_instr expression ';' assign ')' instruction"""
    p[0] = ast.ForInstruction(p[3], p[4], p[6], p[8])


def p_break_instr(p):
    """break_instr : BREAK ';'"""
    p[0] = ast.BreakInstruction(p.lineno(1))


def p_continue_instr(p):
    """continue_instr : CONTINUE ';' """
    p[0] = ast.ContinueInstruction(p.lineno(1))


def p_return_instr(p):
    """return_instr : RETURN ';'"""
    p[0] = ast.ReturnInstruction(p.lineno(1))


def p_return_instr_2(p):
    """return_instr : RETURN expression ';'"""
    p[0] = ast.ReturnInstructionExpression(p[2], p.lineno(1))


def p_print_instr(p):
    """print_instr : PRINT '(' STRING ')' ';' """
    p[0] = ast.PrintInstruction(ast.String(p[3]), p.lineno(1))


def p_print_instr_2(p):
    """print_instr : PRINT '(' STRING ',' ids_list ')' ';' """
    p[0] = ast.PrintInstructionArgs(ast.String(p[3]), p[5], p.lineno(1))


def p_ids(p):
    """ids_list : ids_list ',' ID"""
    p[0] = ast.IdsList(p[1], ast.ID(p[3], p.lineno(3)))


def p_ids2(p):
    """ids_list : ID"""
    p[0] = ast.ID(p[1], p.lineno(1))


def p_ids3(p):
    """ids_list : ID '[' index ']'"""
    p[0] = ast.TabID(ast.ID(p[1], p.lineno(2)), p[3], p.lineno(2))


def p_ids4(p):
    """ids_list : ids_list ',' ID '[' index ']'"""
    p[0] = ast.IdsListTab(p[1], ast.TabID(ast.ID(p[3], p.lineno(2)), p[5], p.lineno(2)))


def p_comparison(p):
    """bool_expr : expression LESSER_THAN expression
                  | expression GREATER_THAN expression
                  | expression LESSER_EQUAL expression
                  | expression GREATER_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression EQUAL expression"""
    p[0] = ast.Expression(p[1], p[2], p[3], p.lineno(2))


def p_bool_expression(p):
    """expression : bool_expr"""
    p[0] = p[1]


def p_true_false_comparison(p):
    """bool_expr : TRUE
                 | FALSE"""
    p[0] = ast.Boolean(p[1])


def p_operations(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression"""
    p[0] = ast.Expression(p[1], p[2], p[3], p.lineno(2))


def p_parentheses(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_variable(p):
    """variable : INT ID
                | FLOAT ID
                | BOOL ID
                | CHARTYPE ID
                | STRINGTYPE ID
                | VOID ID"""
    p[0] = ast.Variable(p[1], p[2], p.lineno(1))


def p_expression_int(p):
    """expression : INTNUM """
    p[0] = ast.IntNum(p[1])


def p_expression_float(p):
    """expression : FLOATNUM"""
    p[0] = ast.FloatNum(p[1])


def p_expression_char(p):
    """expression : CHAR"""
    p[0] = ast.Char(p[1])


def p_expression_string(p):
    """expression : STRING """
    p[0] = ast.String(p[1])


def p_expression_id(p):
    """expression : ID"""
    p[0] = ast.ID(p[1], p.lineno(1))


def p_functions_1(p):
    """functions : functions function"""
    p[0] = ast.DoubleFunction(p[1], p[2])


def p_functions_instructions_2(p):
    """functions : function
                 | assign_instr"""
    p[0] = p[1]


def p_function(p):
    """function : variable '(' arguments ')' instruction"""
    p[0] = ast.Function(p[1], p[3], p[5])


def p_empty_function(p):
    """function : variable '(' ')' instruction"""
    p[0] = ast.EmptyFunction(p[1], p[4])


def p_arguments(p):
    """arguments : variables"""
    p[0] = p[1]


def p_variables_1(p):
    """variables : variables ',' variable"""
    p[0] = ast.DoubleVariable(p[1], p[3])


def p_variables_2(p):
    """variables : variable """
    p[0] = p[1]


parser = yacc.yacc()
