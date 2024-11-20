def to_decimal(number: str, base: int) -> int:
    """Перевод числа из произвольной системы счисления в десятичную."""
    decimal_value = 0
    for i, digit in enumerate(reversed(number)):
        if '0' <= digit <= '9':
            value = ord(digit) - ord('0')
        elif 'A' <= digit.upper() <= 'Z':
            value = ord(digit.upper()) - ord('A') + 10
        else:
            raise ValueError(f"Недопустимый символ '{digit}' в числе {number}.")

        if value >= base:
            raise ValueError(f"Цифра '{digit}' превышает основание {base}.")

        decimal_value += value * (base ** i)
    return decimal_value


def from_decimal(number: int, base: int) -> str:
    """Перевод числа из десятичной системы счисления в произвольную."""
    if number == 0:
        return "0"

    digits = []
    while number > 0:
        remainder = number % base
        if remainder < 10:
            digits.append(chr(ord('0') + remainder))
        else:
            digits.append(chr(ord('A') + remainder - 10))
        number //= base
    return ''.join(reversed(digits))


def convert_base(number: str, from_base: int, to_base: int) -> str:
    """Перевод числа из одной системы счисления в другую."""
    decimal_number = to_decimal(number, from_base)
    return from_decimal(decimal_number, to_base)


# Сложение и вычитание
def add_numbers(num1: str, num2: str, base: int) -> str:
    """Сложение чисел в указанной системе счисления."""
    decimal_sum = to_decimal(num1, base) + to_decimal(num2, base)
    return from_decimal(decimal_sum, base)


def subtract_numbers(num1: str, num2: str, base: int) -> str:
    """Вычитание чисел в указанной системе счисления."""
    decimal_difference = to_decimal(num1, base) - to_decimal(num2, base)
    if decimal_difference < 0:
        raise ValueError("Результат вычитания отрицательный.")
    return from_decimal(decimal_difference, base)


# Примеры перевода
def perevod_tests():
    print("Из десятичной в двоичную: ", 42, " ----> ", convert_base("42", 10, 2))  # 101010
    print("Из десятичной в восьмеричную: ", 42, " ----> ", convert_base("42", 10, 8))  # 52
    print("Из десятичной в шестнадцатеричную: ", 42, " ----> ", convert_base("42", 10, 16))  # 2A
    print("\n")
    print("Из двоичной в десятичную: ", 101010, " ----> ", convert_base("101010", 2, 10))  # 42
    print("Из двоичной в восьмеричную:", "101010", " ----> ", convert_base("101010", 2, 8))  # 52
    print("Из двоичной в шестнадцатеричную:", "101010", " ----> ", convert_base("101010", 2, 16))  # 2A
    print("\n")
    print("Из восьмеричной в десятичную:", 52, " ----> ", convert_base("52", 8, 10))  # 42
    print("Из восьмеричной в двоичную:", "52", " ----> ", convert_base("52", 8, 2))  # 101010
    print("Из восьмеричной в шестнадцатеричную:", "52", " ----> ", convert_base("52", 8, 16))  # 2A
    print("\n")
    print("Из шестнадцатеричной в десятичную:", "2A", " ----> ", convert_base("2A", 16, 10))  # 42
    print("Из шестнадцатеричной в двоичную:", "2A", " ----> ", convert_base("2A", 16, 2))  # 101010

    print()
    print("Сложение в двоичной системе:", add_numbers("101", "110", 2))  # 1011
    print("Вычитание в двоичной системе:", subtract_numbers("110", "101", 2))  # 1
    print()
    print("Сложение в восьмеричной системе:", add_numbers("7", "10", 8))  # 17
    print("Вычитание в восьмеричной системе:", subtract_numbers("10", "7", 8))  # 1
    print()
    print("Сложение в шестнадцатеричной системе:", add_numbers("A", "B", 16))  # 15
    print("Вычитание в шестнадцатеричной системе:", subtract_numbers("B", "A", 16))  # 1

# print("\n")
# number_from_user = input("Введите число которое хотите перевести: ")
# from_base_user = input("Введите основание числа (система счисления): ")
# to_base_user = input("Введите целевую систему счисления:")
# print("Перевод числа ", number_from_user,
#       " из системы счисления ", from_base_user,
#       " в систему счисления ", to_base_user)
# print(convert_base(number_from_user, int(from_base_user), int(to_base_user)))
