# Перевод чисел
from translate import convert_base
# from calculate_all import binary_add, binary_subtract, hex_add, octal_add, hex_subtract, octal_subtract
from calculate_ones import universal_add, universal_subtract


def handler_sum_subtract():
    print("Выберите систему счисления:")
    print("1. Двоичная")
    print("2. Восьмеричная")
    print("3. Шестнадцатеричная")
    choice = int(input("Ваш выбор: "))

    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    operation = int(input("Ваш выбор: "))

    num1 = input("Введите первое число: ")
    num2 = input("Введите второе число: ")

    if choice == 1:
        if operation == 1:
            # binary_add(num1, num2)
            print("Результат:", universal_add(num1, num2, 2))
        elif operation == 2:
            # binary_subtract(num1, num2)
            print("Результат:", universal_subtract(num1, num2, 2))
    elif choice == 2:
        if operation == 1:
            # hex_add(num1, num2)
            print("Результат:", universal_add(num1, num2, 8))
        elif operation == 2:
            # hex_subtract(num1, num2)
            print("Результат:", universal_subtract(num1, num2, 8))
    elif choice == 3:
        if operation == 1:
            # octal_add(num1, num2)
            print("Результат:", universal_add(num1, num2, 16))
        elif operation == 2:
            # octal_subtract(num1, num2)
            print("Результат:", universal_subtract(num1, num2, 16))


def handler_perevod():
    number_from_user = input("Введите число которое хотите перевести: ")
    from_base_user = input("Введите основание числа (система счисления): ")
    to_base_user = input("Введите целевую систему счисления: ")
    print("Перевод числа ", number_from_user,
          " из системы счисления ", from_base_user,
          " в систему счисления ", to_base_user)
    print("Результат: ", convert_base(number_from_user, int(from_base_user), int(to_base_user)))


def main():
    while True:
        print("Выберите действие")
        print("1. Перевод числа")
        print("2. Сложение/Вычитание числа")
        choice = int(input("Ваш выбор: "))

        if choice == 1:
            handler_perevod()
        elif choice == 2:
            handler_sum_subtract()
        print("\n")


if __name__ == "__main__":
    main()
