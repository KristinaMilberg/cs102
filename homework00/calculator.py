import math
import typing as tp

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


# перевод в другую систему исчисления
def calculus_system(num1, num2):
    result = ""
    sim = "0123456789ABCDEF"
    num1, num2 = int(num1), int(num2)
    if num1 > 0 and num2 > 0:
        if 0 < num2 <= 9:
            while num1 > 0:
                result = str(num1 % num2) + result
                num1 = num1 // num2
            return result
        if 10 < num2 <= 36:
            while num1 > 0:
                result = sim[num1 % num2] + result
                num1 = num1 // num2
            return result
        else:
            print("")
    else:
        return "Числа должны быть положительными"


# исключение написания лишних символов
def input_check():
    while True:
        num = input("Введите число > ")
        if num.isdigit():
            return int(num)
        else:
            number = num.split(".")
            if len(number) == 2 and number[0].isdigit() and number[1].isdigit():
                return float(num)


def match_case_calc(num1: float, num2: float, command: str) -> tp.Union[float, str]:  # type: ignore
    match command:
        case "/":
            if num2 != 0:
                return num1 + num2
            else:
                return "Error"
        case "-":
            return num1 - num2
        case "+":
            return num1 + num2
        case "*":
            return num1 * num2
        case "**":
            return num1**num2
        case "Перевод в другую сс":
            return calculus_system(num1, num2)
        case "ˆ2":
            return num1**2
        case "sin":
            return math.sin(num1)
        case "cos":
            return math.cos(num1)
        case "tan":
            return math.tan(num1)
        case "logn":
            return math.log(num1)
        case "log(n)":
            return math.log(num1, num2)
        case "log(10)":
            return math.log10(num1)
        case _:
            return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        num1 = input_check()
        num2 = input_check()
        print(match_case_calc(num1, num2, COMMAND))
