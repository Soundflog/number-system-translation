def universal_add(num1, num2, base, symbols="0123456789ABCDEF"):
    """
    Универсальная функция сложения чисел в любой системе счисления.
    :param num1: Первое число (в виде строки).
    :param num2: Второе число (в виде строки).
    :param base: Основание системы счисления.
    :param symbols: Символы, используемые в системе счисления.
    :return: Результат сложения (в виде строки).
    """
    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)

    carry = 0
    result = []
    symbol_to_value = {symbol: i for i, symbol in enumerate(symbols)}
    value_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}

    for i in range(max_len - 1, -1, -1):
        val1 = symbol_to_value[num1[i].upper()]
        val2 = symbol_to_value[num2[i].upper()]
        total = val1 + val2 + carry

        result.append(value_to_symbol[total % base])  # Остаток
        carry = total // base  # Перенос

    if carry:
        result.append(value_to_symbol[carry])

    return ''.join(reversed(result))


def universal_subtract(num1, num2, base, symbols="0123456789ABCDEF"):
    """
    Универсальная функция вычитания чисел в любой системе счисления.
    :param num1: Уменьшаемое (в виде строки).
    :param num2: Вычитаемое (в виде строки).
    :param base: Основание системы счисления.
    :param symbols: Символы, используемые в системе счисления.
    :return: Результат вычитания (в виде строки).
    """
    if num2 < num1:
        print("Ошибка: Невозможно вычесть из меньшего большее")
        return

    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)

    result = []
    borrow = 0
    symbol_to_value = {symbol: i for i, symbol in enumerate(symbols)}
    value_to_symbol = {i: symbol for i, symbol in enumerate(symbols)}

    for i in range(max_len - 1, -1, -1):
        val1 = symbol_to_value[num1[i].upper()]
        val2 = symbol_to_value[num2[i].upper()] + borrow

        if val1 >= val2:
            result.append(value_to_symbol[val1 - val2])  # Без заимствования
            borrow = 0
        else:
            result.append(value_to_symbol[val1 + base - val2])  # Заимствование
            borrow = 1  # Устанавливаем заимствование

    # Удаление ведущих нулей
    while len(result) > 1 and result[-1] == '0':
        result.pop()

    return ''.join(reversed(result))
