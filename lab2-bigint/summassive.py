import random
import sys
import time
import gmpy2
from sympy import Matrix
import numpy as np
from main import BigInt


# Функция для замера времени выполнения операции
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time


# Генерация большого числа с заданным количеством цифр для BigInt
def generate_bigint_number(digits):
    return BigInt(str(random.randint(10**(digits-1), 10**digits - 1)))


# Генерация обычного числа
def generate_regular_number(digits):
    return random.randint(10**(digits-1), 10**digits - 1)


# Сложение массива чисел (для BigInt)
def sum_large_numbers(numbers):
    total = BigInt("0")
    for number in numbers:
        total = total + number
    return total


# Скалярное произведение (для BigInt)
def scalar_product(A, B):
    result = BigInt("0")
    for i in range(len(A)):
        result = result + (A[i] * B[i])
    return result


# Умножение матриц (для BigInt)
def matrix_multiply(A, B):
    n = len(A)
    m = len(B)
    p = len(B[0])
    C = [[BigInt("0") for _ in range(p)] for _ in range(n)]

    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] = C[i][j] + (A[i][k] * B[k][j])

    return C


# Универсальная функция для всех библиотек
def run_tests(max_nums_random=10**4, max_length_mass=10**3):
    if max_nums_random > 640:
        sys.set_int_max_str_digits(max_nums_random)
    # Генерация чисел произвольной длины (от 1 до 10000 цифр)
    # Для BigInt
    matrix_length = 100
    numbers_bigint = [generate_bigint_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]
    A_bigint = [generate_bigint_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]
    B_bigint = [generate_bigint_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]

    # Для обычных чисел
    numbers_regular = [generate_regular_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]
    A_regular = [generate_regular_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]
    B_regular = [generate_regular_number(random.randint(1, max_nums_random)) for _ in range(max_length_mass)]
    matrix_A_regular = [[generate_regular_number(random.randint(1, max_nums_random)) for _ in range(matrix_length)] for _ in range(matrix_length)]
    matrix_B_regular = [[generate_regular_number(random.randint(1, max_nums_random)) for _ in range(matrix_length)] for _ in range(matrix_length)]

    # Выполнение тестов
    libraries = {
        "BigInt": {
            "sum": sum_large_numbers,
            "scalar": scalar_product,
        },
        "gmpy2": {
            "sum": lambda nums: gmpy2.mpz(sum(nums)),
            "scalar": lambda A, B: sum([A[i] * B[i] for i in range(len(A))]),
            "matrix": lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(matrix_length)) for j in range(matrix_length)] for i in range(matrix_length)]
        },
        "sympy": {
            "sum": lambda nums: sum(nums),
            "scalar": lambda A, B: sum([A[i] * B[i] for i in range(len(A))]),
            "matrix": lambda A, B: Matrix(A) * Matrix(B)
        },
        "numpy": {
            "sum": lambda nums: np.sum(np.array(nums, dtype=object)),
            "scalar": lambda A, B: np.dot(A, B),
            "matrix": lambda A, B: np.dot(A, B)
        }
    }

    # Запуск тестов для всех библиотек
    for lib_name, lib_funcs in libraries.items():
        print(f"\nTesting with {lib_name}:")

        for test_name, func in lib_funcs.items():
            if test_name == "sum":
                # Для BigInt используем BigInt массив, для других библиотек - обычные числа
                numbers = numbers_bigint if lib_name == "BigInt" else numbers_regular
                result, elapsed_time = measure_time(func, numbers)
            elif test_name == "scalar":
                # Для BigInt используем BigInt массивы, для других библиотек - обычные числа
                A = A_bigint if lib_name == "BigInt" else A_regular
                B = B_bigint if lib_name == "BigInt" else B_regular
                result, elapsed_time = measure_time(func, A, B)
            else:  # Для умножения матриц
                #matrix_A = matrix_A_bigint if lib_name == "BigInt" else matrix_A_regular
                matrix_A = matrix_A_regular
                #matrix_B = matrix_B_bigint if lib_name == "BigInt" else matrix_B_regular
                matrix_B = matrix_B_regular
                result, elapsed_time = measure_time(func, matrix_A, matrix_B)

            print(f"{test_name.capitalize()} (time): {elapsed_time:.6f} seconds")


if __name__ == "__main__":
    run_tests(
        max_nums_random=10**3,
        max_length_mass=200,
    )
