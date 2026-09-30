"""Тесты черного ящика с запуском консольной программы."""

import subprocess
import sys
import unittest
from pathlib import Path

PROGRAM = Path(__file__).resolve().parents[1] / "src" / "main.py"


def run_program(data: str) -> subprocess.CompletedProcess[str]:
    """Запускает программу и получает оба потока вывода и код завершения."""
    return subprocess.run(
        [sys.executable, str(PROGRAM)],
        input=data,
        text=True,
        capture_output=True,
        timeout=5,
        check=False,
    )


class ConsoleTests(unittest.TestCase):
    """Каждый метод проверяет один запуск программы."""

    def test_first_example(self) -> None:
        result = run_program('1 2\n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '2 2\n', ''),
        )

    def test_impossible_example(self) -> None:
        result = run_program('0 5\n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, 'Impossible\n', ''),
        )

    def test_third_example(self) -> None:
        result = run_program('2 2\n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '2 3\n', ''),
        )

    def test_empty_bus(self) -> None:
        result = run_program('0 0')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '0 0\n', ''),
        )

    def test_adults_only(self) -> None:
        result = run_program('5 0')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '5 5\n', ''),
        )

    def test_fewer_children(self) -> None:
        result = run_program('5 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '5 6\n', ''),
        )

    def test_more_children(self) -> None:
        result = run_program('2 5')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '5 6\n', ''),
        )

    def test_both_upper_bounds(self) -> None:
        result = run_program('100000 100000')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '100000 199999\n', ''),
        )

    def test_maximum_children_without_adults(self) -> None:
        result = run_program('0 100000')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, 'Impossible\n', ''),
        )

    def test_multiple_spaces(self) -> None:
        result = run_program('  2   2  \n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '2 3\n', ''),
        )

    def test_newlines(self) -> None:
        result = run_program('2\n2\n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '2 3\n', ''),
        )

    def test_tabs(self) -> None:
        result = run_program('\t2\t2\r\n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (0, '2 3\n', ''),
        )

    def test_empty_input(self) -> None:
        result = run_program('')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_whitespace_only(self) -> None:
        result = run_program(' \n')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_missing_value(self) -> None:
        result = run_program('2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_extra_value(self) -> None:
        result = run_program('2 2 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_non_integer_adults(self) -> None:
        result = run_program('два 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_non_integer_children(self) -> None:
        result = run_program('2 два')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_fractional_adults(self) -> None:
        result = run_program('1.5 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_fractional_children(self) -> None:
        result = run_program('2 1.5')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Ожидаются два целых числа: количество взрослых и детей.\n'),
        )

    def test_negative_adults(self) -> None:
        result = run_program('-1 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Количество взрослых и детей должно быть от 0 до 100000.\n'),
        )

    def test_negative_children(self) -> None:
        result = run_program('2 -1')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Количество взрослых и детей должно быть от 0 до 100000.\n'),
        )

    def test_too_many_adults(self) -> None:
        result = run_program('100001 2')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Количество взрослых и детей должно быть от 0 до 100000.\n'),
        )

    def test_too_many_children(self) -> None:
        result = run_program('2 100001')
        self.assertEqual(
            (result.returncode, result.stdout, result.stderr),
            (1, '', 'Количество взрослых и детей должно быть от 0 до 100000.\n'),
        )


if __name__ == "__main__":
    unittest.main()
