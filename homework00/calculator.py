# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import typing as tp
from math import cos
from math import log as ln
from math import log10, sin
from math import tan as tg


# проверка, что число целое
def is_int(num: tp.Any) -> bool:
    try:
        if int(num) == num:
            return True
    except ValueError:
        ...
    return False


# проверка, что число вещественное
def is_float(num: tp.Any) -> bool:
    try:
        float(num)
    except ValueError:
        return False
    return True


# получение одного числа
def get_number(text: str) -> float:
    value = input(text)
    if is_float(value):
        return float(value)
    return get_number("Это не число, введите число > ")


# получение двух чисел
def get_numbers(command: str) -> tuple[float, float]:
    if command in "+-*/^#":
        num1 = get_number("Введите число 1 > ")
        num2 = get_number("Введите число 2 > ")
    else:
        num1 = get_number("Введите число > ")
        num2 = 0.0
    return num1, num2


# перевод в другую систему исчисления
def convert(num1: int, num2: int) -> str:
    res = ""
    simbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num1, num2 = int(num1), int(num2)
    if num1 >= 0 and num2 > 0:
        if 0 < num2 <= 9:
            while num1 > 0:
                res = str(num1 % num2) + res
                num1 = num1 // num2
            return res
        if 10 < num2 <= 36:
            while num1 > 0:
                res = simbols[num1 % num2] + res
                num1 = num1 // num2
            return res
        else:
            print("")
    else:
        return f"Числa должны быть положительными"


# калькулятор
def calculate(command: str, num1: float, num2: float = 0.0) -> tp.Union[float, str]:
    match command:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            if num2 != 0:
                return num1 / num2
            return "На ноль делить нельзя"
        case "^":
            return num1**num2
        case "#":
            if not is_int(num1) or not is_int(num2) or num1 < 0 or num2 < 0:
                return "Числа должны быть целыми неотрицательными"
            if not (2 <= num2 <= 36):
                return "Основание CC должно быть в диапазоне от 2 до 36"
            return convert(int(num1), int(num2))
        case "^2":
            return num1**2
        case "sin":
            return sin(num1)
        case "cos":
            return cos(num1)
        case "tg":
            return tg(num1)
        case "ctg":
            return 1 / tg(num1) if tg(num1) != 0 else "Не существует"
        case "log10":
            if num1 > 0:
                return log10(num1)
            return "Число должно быть положительное"
        case "ln":
            if num1 > 0:
                return ln(num1)
            return "Число должно быть положительное"
        case _:
            return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        elif COMMAND != "()":
            NUM1, NUM2 = get_numbers(COMMAND)
            calc = calculate(COMMAND, NUM1, NUM2)
        print(int(calc) if is_int(calc) else calc)
