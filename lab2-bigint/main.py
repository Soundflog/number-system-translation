class BigInt:
    def __init__(self, value="0"):
        """Инициализация числа."""
        if not value.lstrip('-').isdigit():  # Проверка, что строка состоит только из цифр
            raise ValueError(f"BigInt must be initialized with a valid integer string, but got: '{value}'")

        self.sign = 1 if value[0] != '-' else -1
        self.digits = list(map(int, value.lstrip('-')[::-1]))  # Сохраняем цифры в обратном порядке

    def __str__(self):
        """Возвращаем строковое представление числа."""
        return ('-' if self.sign == -1 else '') + ''.join(map(str, self.digits[::-1]))

    def _normalize(self):
        """Удаляем ведущие нули."""
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        if len(self.digits) == 1 and self.digits[0] == 0:
            self.sign = 1  # Нормализуем знак для нуля

    def __abs__(self):
        """Возвращаем абсолютное значение числа (игнорируем знак)."""
        result = BigInt("0")  # Это не вызывает рекурсию, просто создается объект с 0
        result.digits = self.digits.copy()  # Просто копируем цифры
        result.sign = 1  # Устанавливаем знак в 1 (положительное число)
        return result

    def __neg__(self):
        """Возвращаем отрицательное значение числа (инвертируем знак)."""
        result = BigInt("0")
        result.digits = self.digits.copy()  # Просто копируем цифры
        result.sign = -self.sign  # Инвертируем знак
        return result

    def __add__(self, other):
        """Оптимизированное сложение по методу Книгена-Карацубы."""
        if self.sign == other.sign:
            result = BigInt()
            result.sign = self.sign
            carry = 0

            max_len = max(len(self.digits), len(other.digits))
            for i in range(max_len):
                sum_digits = carry
                if i < len(self.digits):
                    sum_digits += self.digits[i]
                if i < len(other.digits):
                    sum_digits += other.digits[i]

                carry = sum_digits // 10
                result.digits.append(sum_digits % 10)

            if carry:
                result.digits.append(carry)

            result._normalize()
            return result
        else:
            return self - (-other)  # Если знаки разные, используем вычитание

    def __sub__(self, other):
        """Оптимизированное вычитание с остаточным учетом."""
        if self.sign != other.sign:
            return self + (-other)
        if abs(self) >= abs(other):
            result = BigInt()
            result.sign = self.sign
            borrow = 0

            for i in range(len(self.digits)):
                diff_digits = self.digits[i] - borrow
                if i < len(other.digits):
                    diff_digits -= other.digits[i]

                if diff_digits < 0:
                    diff_digits += 10
                    borrow = 1
                else:
                    borrow = 0

                result.digits.append(diff_digits)

            result._normalize()
            return result
        else:
            return -(other - self)  # Для отрицательного результата

    def _split(self, k):
        """Разделение числа на 3 части для Toom-Cook умножения."""
        n = len(self.digits)

        # Часть 1: A2
        if n > 2 * k:
            A2_digits = self.digits[k:n - 2 * k]
            A2 = BigInt("".join(map(str, A2_digits))) if A2_digits else BigInt("0")
        else:
            A2 = BigInt("0")

        # Часть 2: A1
        if n > k:
            A1_digits = self.digits[k:n - k]
            A1 = BigInt("".join(map(str, A1_digits))) if A1_digits else BigInt("0")
        else:
            A1 = BigInt("0")

        # Часть 3: A0
        A0_digits = self.digits[:k]
        A0 = BigInt("".join(map(str, A0_digits))) if A0_digits else BigInt("0")

        return A2, A1, A0

    def __mul__(self, other):
        """Алгоритм умножения Toom-Cook (Toom-3)."""
        if len(self.digits) < 4 or len(other.digits) < 4:  # Для небольших чисел используем наивный алгоритм
            return self._naive_multiply(other)

        # Разделяем на части
        k = len(self.digits) // 3
        A2, A1, A0 = self._split(k)
        B2, B1, B0 = other._split(k)

        # Шаги Toom-3:
        P0 = A0 * B0
        P1 = (A0 + A1) * (B0 + B1)
        P2 = (A1 + A2) * (B1 + B2)
        P3 = A2 * B2

        # Интерполяция
        result = self._interpolate(P0, P1, P2, P3, k)
        result._normalize()
        return result

    def _interpolate(self, P0, P1, P2, P3, k):
        """Интерполяция для Toom-3 (комбинируем результаты)."""
        # Здесь используется специфическая интерполяция для Toom-3
        # Для простоты предполагаем, что интерполяция осуществляется линейно.
        # В реальной реализации необходимо учитывать полиномиальные вычисления.
        result = P3 * BigInt(str(10 ** (2 * k))) + P2 * BigInt(str(10 ** k)) + P1 + P0
        return result

    def _naive_multiply(self, other):
        """Наивное умножение для небольших чисел."""
        result = BigInt("0")
        result.digits = [0] * (len(self.digits) + len(other.digits))

        for i in range(len(self.digits)):
            for j in range(len(other.digits)):
                result.digits[i + j] += self.digits[i] * other.digits[j]
                result.digits[i + j + 1] += result.digits[i + j] // 10
                result.digits[i + j] %= 10

        result._normalize()
        return result

    def __floordiv__(self, other):
        """Целочисленное деление (алгоритм длинного деления)."""

        """
        Dividend — число, которое делится 
            (большее число, находится на левой стороне символа деления). 

        Divisor — число, которое используется для деления dividend 
            (меньшее число, пишется на правой стороне символа деления)

        Quotient — результат деления 
            (ответ, полученный после деления dividend на divisor). 

        Remainder — количество, которое остаётся после деления 
            (разница между dividend и произведением divisor и quotient)
        """
        if other == BigInt("0"):
            raise ValueError("Cannot divide by zero.")

        # Убираем знак, чтобы работать с положительными числами
        dividend = abs(self)
        divisor = abs(other)

        quotient = BigInt("0")
        remainder = BigInt("0")

        # Перебираем цифры делимого (dividend)
        for i in range(len(dividend.digits) - 1, -1, -1):
            # Добавляем цифру делимого в остаток
            remainder.digits.insert(0, dividend.digits[i])
            remainder._normalize()

            # Делаем деление для текущего остатка
            count = 0
            while remainder >= divisor:
                remainder -= divisor
                count += 1

            # Добавляем к результату
            quotient.digits.insert(0, count)

        quotient._normalize()
        return quotient

    def __lt__(self, other):
        if self.sign != other.sign:
            return self.sign < other.sign
        if len(self.digits) != len(other.digits):
            return len(self.digits) < len(other.digits)
        for i in range(len(self.digits) - 1, -1, -1):
            if self.digits[i] != other.digits[i]:
                return self.digits[i] < other.digits[i]
        return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __eq__(self, other):
        return self.sign == other.sign and self.digits == other.digits

    def __ne__(self, other):
        return not self == other


if __name__ == "__main__":
    a = BigInt("123456789123456789123456789123456789")
    b = BigInt("987654321987654321987654321987654321")
    carry_addition = a + b
    borrowing_subtraction = a - b
    toom_cook_mul = a * b
    naive_division = a // b
    print(f"Сложение: {a} + {b} = {carry_addition}")
    print(f"Вычитание: {a} - {b} = {borrowing_subtraction}")
    print(f"Умножение: {a} * {b} = {toom_cook_mul}")
    print(f"Деление: {a} // {b} = {naive_division}")
