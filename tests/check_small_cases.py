"""Дополнительная проверка формул полным перебором малых распределений."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fare import calculate_fare


def enumerate_costs(adults: int, children: int) -> list[int]:
    """Получает стоимости распределений непосредственно по условию задачи."""
    if adults == 1:
        return [1 + max(0, children - 1)]
    return [
        1 + max(0, assigned - 1) + remaining_cost
        for assigned in range(children + 1)
        for remaining_cost in enumerate_costs(adults - 1, children - assigned)
    ]


def main() -> int:
    """Сравнивает расчет с перебором для 54 пар; возвращает 0 при совпадении."""
    checked = 0
    for adults in range(1, 7):
        for children in range(9):
            costs = enumerate_costs(adults, children)
            expected = min(costs), max(costs)
            actual = calculate_fare(adults, children)
            if actual != expected:
                print(
                    f"Несовпадение для n={adults}, m={children}: "
                    f"получено {actual}, ожидается {expected}.",
                    file=sys.stderr,
                )
                return 1
            checked += 1
    print(f"Проверены {checked} пары: результат совпадает с перебором.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
