"""Консольная программа расчета стоимости проезда для варианта 10."""

import sys

from fare import calculate_fare


def parse_input(text: str) -> tuple[int, int]:
    """Преобразует текст с двумя целыми числами в количества пассажиров.

    Пробельные символы разделяют значения. При неверном числе значений
    или невозможности преобразования вызывает ValueError.
    Проверку диапазона выполняет модуль fare.
    """
    values = text.split()
    if len(values) != 2:
        raise ValueError("Ожидаются два целых числа: количество взрослых и детей.")

    try:
        adults, children = map(int, values)
    except ValueError as error:
        raise ValueError(
            "Ожидаются два целых числа: количество взрослых и детей."
        ) from error
    return adults, children


def main() -> int:
    """Читает два числа, выводит ответ и возвращает код завершения.

    Результат направляется в stdout. При ошибке ввода сообщение
    направляется в stderr, а код завершения равен 1.
    """

    try:
        adults, children = parse_input(sys.stdin.read())
        result = calculate_fare(adults, children)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if result is None:
        print("Impossible")
    else:
        print(result[0], result[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
