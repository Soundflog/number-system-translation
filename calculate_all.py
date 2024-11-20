def binary_add(bin1, bin2):
    """Сложение двоичных чисел."""
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    carry = 0
    result = []

    for i in range(max_len - 1, -1, -1):
        total = int(bin1[i]) + int(bin2[i]) + carry
        result.append(str(total % 2))
        carry = total // 2

    if carry:
        result.append('1')

    return ''.join(reversed(result))


def binary_subtract(bin1, bin2):
    """Вычитание двоичных чисел (без отрицательных результатов)."""
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = []
    borrow = 0

    for i in range(max_len - 1, -1, -1):
        b1 = int(bin1[i])
        b2 = int(bin2[i]) + borrow

        if b1 >= b2:
            result.append(str(b1 - b2))
            borrow = 0
        else:
            result.append(str(b1 + 2 - b2))
            borrow = 1

    # Удаление ведущих нулей
    while len(result) > 1 and result[-1] == '0':
        result.pop()

    return ''.join(reversed(result))


def octal_add(oct1, oct2):
    """Сложение восьмеричных чисел."""
    max_len = max(len(oct1), len(oct2))
    oct1 = oct1.zfill(max_len)
    oct2 = oct2.zfill(max_len)

    carry = 0
    result = []

    for i in range(max_len - 1, -1, -1):
        total = int(oct1[i]) + int(oct2[i]) + carry
        result.append(str(total % 8))
        carry = total // 8

    if carry:
        result.append(str(carry))

    return ''.join(reversed(result))


def octal_subtract(oct1, oct2):
    """Вычитание восьмеричных чисел (без отрицательных результатов)."""
    max_len = max(len(oct1), len(oct2))
    oct1 = oct1.zfill(max_len)
    oct2 = oct2.zfill(max_len)

    result = []
    borrow = 0

    for i in range(max_len - 1, -1, -1):
        o1 = int(oct1[i])
        o2 = int(oct2[i]) + borrow

        if o1 >= o2:
            result.append(str(o1 - o2))
            borrow = 0
        else:
            result.append(str(o1 + 8 - o2))
            borrow = 1

    # Удаление ведущих нулей
    while len(result) > 1 and result[-1] == '0':
        result.pop()

    return ''.join(reversed(result))


def hex_add(hex1, hex2):
    """Сложение шестнадцатеричных чисел."""
    max_len = max(len(hex1), len(hex2))
    hex1 = hex1.zfill(max_len)
    hex2 = hex2.zfill(max_len)

    carry = 0
    result = []
    hex_map = {str(i): i for i in range(10)}
    hex_map.update({chr(i + 55): i for i in range(10, 16)})
    reverse_map = {v: k for k, v in hex_map.items()}

    for i in range(max_len - 1, -1, -1):
        total = hex_map[hex1[i].upper()] + hex_map[hex2[i].upper()] + carry
        result.append(reverse_map[total % 16])
        carry = total // 16

    if carry:
        result.append(reverse_map[carry])

    return ''.join(reversed(result))


def hex_subtract(hex1, hex2):
    """Вычитание шестнадцатеричных чисел (без отрицательных результатов)."""
    max_len = max(len(hex1), len(hex2))
    hex1 = hex1.zfill(max_len)
    hex2 = hex2.zfill(max_len)

    result = []
    borrow = 0
    hex_map = {str(i): i for i in range(10)}
    hex_map.update({chr(i + 55): i for i in range(10, 16)})
    reverse_map = {v: k for k, v in hex_map.items()}

    for i in range(max_len - 1, -1, -1):
        h1 = hex_map[hex1[i].upper()]
        h2 = hex_map[hex2[i].upper()] + borrow

        if h1 >= h2:
            result.append(reverse_map[h1 - h2])
            borrow = 0
        else:
            result.append(reverse_map[h1 + 16 - h2])
            borrow = 1

    # Удаление ведущих нулей
    while len(result) > 1 and result[-1] == '0':
        result.pop()

    return ''.join(reversed(result))

