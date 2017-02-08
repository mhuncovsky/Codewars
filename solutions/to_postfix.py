def to_postfix(expr):
    precedence = {
        '**': 4,
        '^': 4,
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1,
    }
    opstack = []
    postfix = []
    tokenlist = [c for c in expr]

    for token in tokenlist:
        if token.isalnum():
            postfix.append(token)
        elif token == '(':
            opstack.append(token)
        elif token == ')':
            top = opstack.pop()
            while top != '(':
                postfix.append(top)
                top = opstack.pop()
        else:
            while opstack and precedence[opstack[-1]] >= precedence[token]:
                postfix.append(opstack.pop())
            opstack.append(token)
    while opstack:
        postfix.append(opstack.pop())

    return ''.join(postfix)
