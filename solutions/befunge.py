class Befunge():
    """Simple befunge interpreter"""

    def __init__(self):
        self.stack = []
        self.code = ''
        self.dir = '>'
        self.strmode = False
        self.skip = False
        self.x = 0
        self.y = 0

        self.output = ''

        self.inst = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '%': self.mod,
            '!': self.lognot,
            '`': self.gt,
            '_': self.mv_hor,
            '|': self.mv_vert,
            '"': self.toggle_strmode,
            ':': self.duplicate_stacktop,
            '\\': self.swap,
            '$': self.discard,
            '.': self.out_int,
            ',': self.out_chr,
            '#': self.trampoline,
            'p': self.put,
            'g': self.get,
            ' ': self.nop,
        }

    def run(self, code):
        self.code = [[c for c in line] for line in code.split('\n')]

        c = self.code[self.y][self.x]
        while c != '@':
            if self.strmode:
                if c == '"':
                    self.toggle_strmode()
                else:
                    self.push(ord(c))
            elif self.skip:
                self.skip = False
            elif c.isnumeric():
                self.push(int(c))
            elif c in '<>v^?':
                self.setdir(c)
            else:
                self.inst[c]()

            self.move()
            c = self.code[self.y][self.x]

    def push(self, n):
        if n is str:
            n = ord(str)
        self.stack.append(n)

    def pop(self):
        return self.stack.pop()

    def move(self):
        if self.dir == '>':
            self.x += 1
        elif self.dir == '<':
            self.x -= 1
        elif self.dir == '^':
            self.y -= 1
        elif self.dir == 'v':
            self.y += 1

    def add(self):
        a, b = self.pop(), self.pop()
        self.push(a + b)

    def sub(self):
        a, b = self.pop(), self.pop()
        self.push(b - a)

    def mul(self):
        a, b = self.pop(), self.pop()
        self.push(a * b)

    def div(self):
        a, b = self.pop(), self.pop()
        self.push(0 if a == 0 else (b // a))

    def mod(self):
        a, b = self.pop(), self.pop()
        self.push(0 if a == 0 else (b % a))

    def lognot(self):
        a = self.pop()
        self.push(1 if a == 0 else 0)

    def gt(self):
        a, b = self.pop(), self.pop()
        self.push(1 if b > a else 0)

    def setdir(self, direction):
        from random import choice
        if direction in '<>^v':
            self.dir = direction
        elif direction == '?':
            self.dir = choice('<>^v')

    def mv_hor(self):
        a = self.pop()
        self.dir = '>' if a == 0 else '<'

    def mv_vert(self):
        a = self.pop()
        self.dir = 'v' if a == 0 else '^'

    def toggle_strmode(self):
        self.strmode = not self.strmode

    def duplicate_stacktop(self):
        if self.stack:
            self.push(self.stack[-1])
        else:
            self.push(0)

    def swap(self):
        lstack = len(self.stack)
        if lstack >= 2:
            a, b = self.pop(), self.pop()
            self.push(a)
            self.push(b)
        else:
            a = self.pop()
            self.push(a)
            self.push(0)

    def discard(self):
        self.pop()

    def out_int(self):
        self.output += str(self.pop())

    def out_chr(self):
        self.output += (chr(self.pop()))

    def trampoline(self):
        self.skip = True

    def put(self):
        y, x, v = self.pop(), self.pop(), self.pop()
        self.code[y][x] = chr(v)

    def get(self):
        y, x = self.pop(), self.pop()
        self.push(ord(self.code[y][x]))

    def nop(self):
        pass


# print('TEST:')
# codes = [('>25*"!dlroW olleH":v \n'
#           '                v:,_@\n'
#           '                >  ^ '),
#          ('2>:3g" "-!v\  g30          <           \n'
#           ' |!`"&":+1_:.:03p>03g+:"&"`|           \n'
#           ' @               ^  p3\\" ":<           \n'
#           '2 2345678901234567890123456789012345678')]
#
# for c in codes:
#     bef = Befunge()
#     bef.run(c)
#     print('--------')
#     print(bef.output)
