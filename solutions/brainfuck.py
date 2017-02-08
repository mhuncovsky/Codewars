#! python3.5


class Brainfuck():
    """Simple brainfuck interpreter"""

    def __init__(self):
        self.data = [0]
        self.input = None
        self.output = ''
        self.data_pointer = 0
        self.instr_pointer = 0
        self.code = None

    def run(self, code, input_str):
        self.code = code
        self.input = list(input_str[::-1])
        while True:
            try:
                instr = self.code[self.instr_pointer]
            except IndexError:
                break

            if instr == '>':
                self._inc_data_pointer()
            elif instr == '<':
                self._dec_data_pointer()
            elif instr == '+':
                self._increment()
            elif instr == '-':
                self._decrement()
            elif instr == '.':
                self._out()
            elif instr == ',':
                self._inp()
            elif instr == '[':
                self._jump_forward()
            elif instr == ']':
                self._jump_backward()

            self.instr_pointer += 1

        return self.output

    def _inc_data_pointer(self):
        self.data_pointer += 1
        if len(self.data) <= self.data_pointer:
            self.data.append(0)

    def _dec_data_pointer(self):
        self.data_pointer -= 1
        if self.data_pointer < 0:
            self.data.insert(0, 0)
            self.data_pointer = 0

    def _increment(self):
        self.data[self.data_pointer] += 1
        if self.data[self.data_pointer] > 255:
            self.data[self.data_pointer] = 0

    def _decrement(self):
        self.data[self.data_pointer] -= 1
        if self.data[self.data_pointer] < 0:
            self.data[self.data_pointer] = 255

    def _out(self):
        self.output += chr(self.data[self.data_pointer])

    def _inp(self):
        self.data[self.data_pointer] = ord(self.input.pop())

    def _jump_forward(self):
        if not self.data[self.data_pointer]:
            self.instr_pointer += 1
            counter = 1
            while counter > 0:
                self.instr_pointer += 1
                if self.code[self.instr_pointer] == ']':
                    counter -= 1
                elif self.code[self.instr_pointer] == '[':
                    counter += 1

    def _jump_backward(self):
        if self.data[self.data_pointer]:
            self.instr_pointer -= 1
            counter = 1
            while counter > 0:
                self.instr_pointer -= 1
                if self.code[self.instr_pointer] == '[':
                    counter -= 1
                elif self.code[self.instr_pointer] == ']':
                    counter += 1


if __name__ == '__main__':
    codes = [',[.[-],]', ',+[-.,+]', ',>,<[>[->+>+<<]>>[-<<+>>]<<<-]>>.']
    inputs = ['Codewars' + chr(0), 'Codewars' + chr(255), chr(8) + chr(9)]
    for i, c in enumerate(codes):
        bf = Brainfuck()
        bf.run(c, inputs[i])
        print(c, inputs[i], ' --> ', bf.output)
