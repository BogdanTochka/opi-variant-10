"""Отдельные сценарии проверки расчета и диапазона пассажиров."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fare import calculate_fare, validate_counts


class FareTests(unittest.TestCase):
    """Каждый метод проверяет один набор исходных данных."""

    def test_first_example(self) -> None:
        self.assertEqual(calculate_fare(1, 2), (2, 2))

    def test_impossible_example(self) -> None:
        self.assertEqual(calculate_fare(0, 5), None)

    def test_third_example(self) -> None:
        self.assertEqual(calculate_fare(2, 2), (2, 3))

    def test_empty_bus(self) -> None:
        self.assertEqual(calculate_fare(0, 0), (0, 0))

    def test_one_adult_only(self) -> None:
        self.assertEqual(calculate_fare(1, 0), (1, 1))

    def test_adults_only(self) -> None:
        self.assertEqual(calculate_fare(5, 0), (5, 5))

    def test_maximum_adults_only(self) -> None:
        self.assertEqual(calculate_fare(100000, 0), (100000, 100000))

    def test_one_child_without_adults(self) -> None:
        self.assertEqual(calculate_fare(0, 1), None)

    def test_maximum_children_without_adults(self) -> None:
        self.assertEqual(calculate_fare(0, 100000), None)

    def test_one_adult_one_child(self) -> None:
        self.assertEqual(calculate_fare(1, 1), (1, 1))

    def test_one_adult_many_children(self) -> None:
        self.assertEqual(calculate_fare(1, 5), (5, 5))

    def test_one_adult_maximum_children(self) -> None:
        self.assertEqual(calculate_fare(1, 100000), (100000, 100000))

    def test_fewer_children(self) -> None:
        self.assertEqual(calculate_fare(5, 2), (5, 6))

    def test_more_children(self) -> None:
        self.assertEqual(calculate_fare(2, 5), (5, 6))

    def test_equal_counts(self) -> None:
        self.assertEqual(calculate_fare(5, 5), (5, 9))

    def test_both_upper_bounds(self) -> None:
        self.assertEqual(calculate_fare(100000, 100000), (100000, 199999))

    def test_maximum_adults_one_child(self) -> None:
        self.assertEqual(calculate_fare(100000, 1), (100000, 100000))

    def test_adjacent_upper_bounds(self) -> None:
        self.assertEqual(calculate_fare(100000, 99999), (100000, 199998))

    def test_negative_adults(self) -> None:
        with self.assertRaises(ValueError):
            calculate_fare(-1, 0)

    def test_negative_children(self) -> None:
        with self.assertRaises(ValueError):
            calculate_fare(0, -1)

    def test_too_many_adults(self) -> None:
        with self.assertRaises(ValueError):
            calculate_fare(100001, 0)

    def test_too_many_children(self) -> None:
        with self.assertRaises(ValueError):
            calculate_fare(0, 100001)


class ValidationTests(unittest.TestCase):
    """Прямые проверки контракта validate_counts."""

    def test_lower_bounds(self) -> None:
        self.assertIsNone(validate_counts(0, 0))

    def test_upper_bounds(self) -> None:
        self.assertIsNone(validate_counts(100000, 100000))

    def test_negative_adults(self) -> None:
        with self.assertRaises(ValueError):
            validate_counts(-1, 0)

    def test_negative_children(self) -> None:
        with self.assertRaises(ValueError):
            validate_counts(0, -1)

    def test_too_many_adults(self) -> None:
        with self.assertRaises(ValueError):
            validate_counts(100001, 0)

    def test_too_many_children(self) -> None:
        with self.assertRaises(ValueError):
            validate_counts(0, 100001)


if __name__ == "__main__":
    unittest.main()
