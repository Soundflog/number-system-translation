import time
import numpy as np
from gmpy2 import mpz
from main import BigInt
import random as rnd


# 1. Ваш алгоритм умножения
def my_bigint_algorithm(a, b):
    x = BigInt(str(a))
    y = BigInt(str(b))
    result = x * y
    return result


# 2. Алгоритм Карацубы (с использованием gmpy2)
def karatsuba_algorithm(x, y):
    # Используем gmpy2 для умножения больших чисел
    # Базовый случай для рекурсии: если числа маленькие, используем обычное умножение
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y

    # Вычисляем размер чисел
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    # Разделяем x и y на две половины
    high1, low1 = divmod(x, 10 ** m)
    high2, low2 = divmod(y, 10 ** m)

    # Рекурсивно вычисляем три произведения
    z0 = karatsuba_algorithm(low1, low2)
    z1 = karatsuba_algorithm(low1 + high1, low2 + high2)
    z2 = karatsuba_algorithm(high1, high2)

    # Составляем результат
    return (z2 * 10 ** (2 * m)) + ((z1 - z2 - z0) * 10 ** m) + z0


# 3. Алгоритм FFT
def fft_multiply(a, b):
    # Преобразуем числа в полиномы и применяем FFT
    n = len(a) + len(b) - 1
    m = 2 ** (n.bit_length())  # Следующая степень двойки
    A = np.fft.fft(a, m)
    B = np.fft.fft(b, m)
    result = np.fft.ifft(A * B)

    # Извлекаем результат
    return np.round(result.real).astype(int)


def generate_large_random_number(length):
    return int(''.join([str(rnd.randint(0, 9)) for _ in range(length)]))


# Тестирование многократных запусков
def test_algorithms(repetitions=10, num_length=1000):
    # Генерация случайных чисел
    num1 = generate_large_random_number(num_length)
    num2 = generate_large_random_number(num_length)

    # Тестирование каждого алгоритма
    algorithms = [
        ("Toom Kook Algorithm", my_bigint_algorithm),
        ("Karatsuba", karatsuba_algorithm),
        ("FFT", fft_multiply)
    ]

    for name, algorithm in algorithms:
        times = []
        for _ in range(repetitions):
            start_time = time.time()
            if name == "FFT":
                # Преобразуем числа в массивы для FFT
                a_fft = np.array([int(digit) for digit in str(num1)])
                b_fft = np.array([int(digit) for digit in str(num2)])
                algorithm(a_fft, b_fft)
            else:
                algorithm(num1, num2)
            end_time = time.time()
            times.append(end_time - start_time)

        avg_time = sum(times) / len(times)
        print(f"{name} Average Time: {avg_time:.6f} seconds")


# Основной блок для тестирования
if __name__ == "__main__":
    # Запускаем тестирование с 10 повторениями для чисел длиной 1000 цифр
    test_algorithms(repetitions=10, num_length=1000)
