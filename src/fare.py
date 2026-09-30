"""Расчет границ стоимости проезда взрослых и детей."""


def validate_counts(adults: int, children: int) -> None:
    """Проверяет диапазон целых количеств пассажиров.

    При отрицательном значении или превышении 100000 вызывает ValueError.
    """
    if not 0 <= adults <= 100000 or not 0 <= children <= 100000:
        raise ValueError("Количество взрослых и детей должно быть от 0 до 100000.")


def calculate_fare(adults: int, children: int) -> tuple[int, int] | None:
    """Возвращает минимальную и максимальную стоимость в рублях.

    Аргументы — целые количества взрослых и детей от 0 до 100000.
    Если дети едут без взрослых, возвращает None.
    При нарушении диапазона вызывает ValueError.
    """
    validate_counts(adults, children)

    if adults == 0 and children > 0:
        return None

    if children == 0:
        return adults, adults

    minimum = max(adults, children)
    maximum = adults + children - 1
    return minimum, maximum
