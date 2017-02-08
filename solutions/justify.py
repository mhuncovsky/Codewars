def justify(string, width):
    words = string.split()[::-1]
    justified = ''

    line = []
    chars = 0
    while words:
        if chars + len(words[-1]) > width - len(line):
            spaces = width - len(''.join(line))
            gaps = len(line) - 1
            pergap = spaces // gaps if gaps > 0 else 0
            more = spaces % gaps if gaps > 0 else 0

            justified += (' ' * (pergap + 1)).join(line[:more + 1])
            justified += (' ' * pergap) + (' ' * pergap).join(line[more + 1:])
            justified += '\n'

            chars = 0
            line = []

        word = words.pop()
        line.append(word)
        chars += len(word)

    justified += ' '.join(line)

    return justified