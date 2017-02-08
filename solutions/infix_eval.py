def infix_eval(expr):
    from operator import pow, mul, truediv, add, sub
    oper = {
        '**': pow,
        '^': pow,
        '*': mul,
        '/': truediv,
        '+': add,
        '-': sub,
    }
    prec = {
        '**': 4,
        '^': 4,
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1,
    }
    operator_stack = []
    operand_stack = []

    for token in expr.split():
        if isnum(token):
            operand_stack.append(float(token))
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            top = operator_stack.pop()
            while top != '(':
                temp = operand_stack.pop()
                operand_stack.append(oper[top](operand_stack.pop(), temp))
                top = operator_stack.pop()
        else:
            while operator_stack and prec[operator_stack[-1]] >= prec[token]:
                temp = operand_stack.pop()
                operand_stack.append(
                    oper[operator_stack.pop()](operand_stack.pop(), temp))
            operator_stack.append(token)

    while operator_stack:
        temp = operand_stack.pop()
        operand_stack.append(
            oper[operator_stack.pop()](operand_stack.pop(), temp))

    return operand_stack.pop()
