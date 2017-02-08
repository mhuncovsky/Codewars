#! python 3.5


MORSE_CODE = {
    '.-...': '&', '--..--': ',', '....-': '4', '.....': '5',
    '...---...': 'SOS', '-...': 'B', '-..-': 'X', '.-.': 'R',
    '.--': 'W', '..---': '2', '.-': 'A', '..': 'I', '..-.': 'F',
    '.': 'E', '.-..': 'L', '...': 'S', '..-': 'U', '..--..': '?',
    '.----': '1', '-.-': 'K', '-..': 'D', '-....': '6',
    '-...-': '=', '---': 'O', '.--.': 'P', '.-.-.-': '.',
    '--': 'M', '-.': 'N', '....': 'H', '.----.': "'",
    '...-': 'V', '--...': '7', '-.-.-.': ';', '-....-': '-',
    '..--.-': '_', '-.--.-': ')', '-.-.--': '!', '--.': 'G',
    '--.-': 'Q', '--..': 'Z', '-..-.': '/', '.-.-.': '+',
    '-.-.': 'C', '---...': ':', '-.--': 'Y', '-': 'T',
    '.--.-.': '@', '...-..-': '$', '.---': 'J', '-----': '0',
    '----.': '9', '.-..-.': '"', '-.--.': '(', '---..': '8',
    '...--': '3'
}


# pause between dots/dashes 0, chars 000, words 0000000

def decode_morse(morse_code):
    words = [word.split() for word in morse_code.split('   ')]
    return ' '.join(''.join(MORSE_CODE[c] for c in word if c)
                    for word in words if word)


def decode_bits(bits):
    bits = bits.strip('0')
    rate = set(len(x) for x in bits.split('0') if x).union(
        set(len(x) for x in bits.split('1') if x))
    if len(rate) > 1:
        rate = min(rate)
    else:
        rate = rate.pop()

    print(rate, bits)
    bits = bits.replace('0' * rate, '0').replace('1' * rate, '1')
    bits = bits.replace('0' * 7, '   ')
    bits = bits.replace('0' * 3, ' ')
    bits = bits.replace('1' * 3, '-').replace('1', '.')
    bits = bits.replace('0', '')
    return bits


def decode_bits_advanced(bits):
    tol1 = 1.2
    tol2 = 1.5
    bits = bits.strip('0')
    ones = [len(x) for x in bits.split('0') if x][::-1]
    zeros = [len(x) for x in bits.split('1') if x][::-1]
    rate = [x for x in ones if x < sum(ones) / len(ones)]
    rate = sum(rate) / len(rate)

    ret = ''
    while ones:
        c = ones.pop()
        if abs(c / rate - 3) < tol1:
            ret += '-'
        else:
            ret += '.'
        c = zeros.pop() if zeros else 0
        if abs(c / rate - 7) < tol2:
            ret += '   '
        elif abs(c / rate - 3) < tol1:
            ret += ' '

    return ret
