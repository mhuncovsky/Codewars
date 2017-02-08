#! python3

# SQURED STRINGS
##
# >>> rot90clock==rot90counter[::-1]
# True
# >>> d1sym==d2sym[::-1]
# True


# Moves in squared strings (I)
s = "abcd\nefgh\nijkl\nmnop"
vm = "dcba\nhgfe\nlkji\nponm"
hm = "mnop\nijkl\nefgh\nabcd"


def vert_mirror(s):
    return "\n".join(line[::-1] for line in s.split("\n"))


def hor_mirror(s):
    return "\n".join(s.split("\n")[::-1])


def oper(fct, s):
    return fct(s)


# Moves in squared strings (II)
r = "ponm\nlkji\nhgfe\ndcba"
sar = "abcd....\nefgh....\nijkl....\nmnop....\n....ponm\n....lkji\n....hgfe\n....dcba"


def rot(s):
    return "\n".join(line[::-1] for line in s.split("\n")[::-1])


def selfie_and_rot(s):
    return "\n".join([line + '.' * len(line) for line in s.split()]
                     + ['.' * len(line) + line for line in rot(s).split()])


# Moves in squared strings (III)
d1sym = "aeim\nbfjn\ncgko\ndhlp"
rot90clock = "miea\nnjfb\nokgc\nplhd"
sad1 = "abcd|aeim\nefgh|bfjn\nijkl|cgko\nmnop|dhlp"


def diag_1_sym(s):
    lines = s.split("\n")
    ret = ""
    for i in range(len(lines)):
        for j in range(len(lines)):
            ret += lines[j][i]
        ret += "\n"
    return ret[:-1]


def rot_90_clock(s):
    return "\n".join(line[::-1] for line in diag_1_sym(s).split("\n"))


def selfie_and_diag1(s):
    d = diag_1_sym(s).split("\n")
    s = s.split("\n")
    return "\n".join("{}|{}".format(s[i], d[i]) for i in range(len(s)))


"""
def rot_90_clock(strng):
    return '\n'.join(''.join(x) for x in zip(*strng.split('\n')[::-1]))      
def diag_1_sym(strng):
    return '\n'.join(''.join(x) for x in zip(*strng.split('\n'))) 
def selfie_and_diag1(strng):
    return '\n'.join('|'.join(x) for x in zip(strng.split('\n'), diag_1_sym(strng).split('\n')))
"""

# Moves in squared strings (IV)
d2sym = "plhd\nokgc\nnjfb\nmiea"
rot90counter = "dhlp\ncgko\nbfjn\naeim"
sad2cc = "abcd|plhd|dhlp\nefgh|okgc|cgko\nijkl|njfb|bfjn\nmnop|miea|aeim"


def diag_2_sym(s):
    return "\n".join("".join(x) for x in zip(*s[::-1].split("\n")))


def rot_90_counter(s):
    return "\n".join(line[::-1] for line in diag_2_sym(s).split("\n"))


def selfie_diag2_counterclock(s):
    return "\n".join("|".join(x) for x in zip(s.split(), diag_2_sym(s).split(),
                                              rot_90_counter(s).split()))


# Coding with Squared Strings
from math import sqrt, ceil


def code(s):
    n = ceil(sqrt(len(s)))
    s += '\x0b' * (n ** 2 - len(s))
    s = ''.join(s[i] if (i + 1) % n != 0 else s[i] + '\n'
                for i in range(n ** 2))[:-1]
    return '\n'.join(''.join(x) for x in zip(*s.split('\n')[::-1]))


def decode(s):
    return '\n'.join(''.join(x) for x in
                     zip(*s.split('\n')[::-1]))[::-1].replace('\n', '').replace('\x0b', '')
