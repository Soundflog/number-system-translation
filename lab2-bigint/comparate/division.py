import time
import random
import gmpy2
from mpmath import mp
import sys


# 1. Наивное деление (Naive Long Division)
def naive_divide(dividend, divisor):
    quotient = 0
    remainder = 0
    for digit in str(dividend):
        # Перемещаем разряд в остаток
        remainder = remainder * 10 + int(digit)

        # Делим текущий остаток на делитель
        quotient_digit = remainder // divisor
        remainder = remainder % divisor

        # Собираем результат
        quotient = quotient * 10 + quotient_digit

    return quotient, remainder


# 2. Divisor Preconditioning (предобработка делителя)
def divisor_preconditioning(dividend, divisor):
    # Пример простого метода предобработки делителя
    # В реальных случаях это может включать использование числовых преобразований
    # для ускорения деления, например, через сдвиги или приближенные значения делителя.

    # В этой реализации будет простой метод, улучшенный через предобработку
    # Например, быстрый сдвиг делителя для оценки его порядка
    approx_divisor = divisor >> 1  # Пример предобработки (сдвиг делителя)

    quotient = dividend // approx_divisor
    remainder = dividend % approx_divisor
    return quotient, remainder


# 3. Divide and Conquer Division (деление с разделением и властвованием)
def divide_and_conquer(dividend, divisor):
    if divisor == 0:
        raise ValueError("Деление на ноль!")

    # Реализация методом "разделяй и властвуй" для деления
    # Применяется деление чисел через рекурсию (аналогично алгоритму Карацубы)
    n = len(str(dividend))

    if n == 1:  # Базовый случай
        return dividend // divisor, dividend % divisor

    m = n // 2
    high = dividend // 10 ** m
    low = dividend % 10 ** m

    q1, r1 = divide_and_conquer(high, divisor)
    q2, r2 = divide_and_conquer(low, divisor)

    # Собираем результат из частей
    quotient = q1 * 10 ** m + q2
    remainder = r1 * 10 ** m + r2
    return quotient, remainder


# 4. Newton’s Method for Division (Метод Ньютона для деления)
def newtons_method(dividend, divisor, iterations=5):
    # Использование метода Ньютона для вычисления обратного числа
    # Инициализация x0 для обратного числа (принимаем приближение как целое число)
    approx_inv = 1  # Начальное приближение для обратного числа, просто 1 (можно улучшить)

    # Применяем метод Ньютона для приближения обратного числа
    for _ in range(iterations):
        approx_inv = approx_inv * (2 - divisor * approx_inv)  # Итерация метода Ньютона
        # Ограничиваем приближение до целого числа, избегая float
        approx_inv = approx_inv // 1  # Приводим к целому числу

    quotient = dividend * approx_inv  # Умножаем на делимое для получения частного
    return quotient, dividend % divisor


# Генерация случайных чисел
def generate_large_random_number(length):
    sys.set_int_max_str_digits(length)
    return int(''.join([str(random.randint(0, 9)) for _ in range(length)]))


# Тестирование многократных запусков
def test_division_algorithms(repetitions=10, num_length=10**3):
    # Генерация случайных чисел
    dividend = generate_large_random_number(num_length)
    divisor = random.randint(100, 10000)  # Делитель в пределах от 1 до 10,000

    algorithms = [
        ("Naive Division", naive_divide),
        ("Divisor Preconditioning", divisor_preconditioning),
        ("Divide and Conquer", divide_and_conquer),
        ("Newton's Method", newtons_method)
    ]

    for name, algorithm in algorithms:
        times = []
        for _ in range(repetitions):
            start_time = time.time()
            algorithm(dividend, divisor)
            end_time = time.time()
            times.append(end_time - start_time)

        avg_time = sum(times) / len(times)
        print(f"{name} Average Time: {avg_time:.6f} seconds")


if __name__ == "__main__":
    # Запускаем тестирование с 10 повторениями для чисел длиной 1000 цифр
    test_division_algorithms(repetitions=10, num_length=10**4)
