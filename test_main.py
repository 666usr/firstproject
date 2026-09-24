"""Простые тесты для main.py.

Это первый опыт написания тестов. Тесты проверяют две ключевые функции:
  * as_number - правильно ли распознаётся число;
  * summarize - правильная ли статистика считается по колонке.

Запуск (из папки проекта):
    python -m unittest -v
    python -m unittest test_main.py
"""

import unittest

from main import as_number, summarize


class TestAsNumber(unittest.TestCase):
    """Проверяем, что строка превращается в число только когда это возможно."""

    def test_whole_number(self):
        self.assertEqual(as_number("42"), 42.0)

    def test_fraction(self):
        self.assertEqual(as_number("3.5"), 3.5)

    def test_text_is_not_number(self):
        self.assertIsNone(as_number("Москва"))

    def test_empty_is_not_number(self):
        self.assertIsNone(as_number(""))


class TestSummarize(unittest.TestCase):
    """Проверяем статистику по колонке."""

    def test_numbers(self):
        info = summarize(["10", "20", "30"])
        self.assertEqual(info["type"], "числовая")
        self.assertEqual(info["min"], 10.0)
        self.assertEqual(info["max"], 30.0)
        self.assertEqual(info["mean"], 20.0)
        self.assertEqual(info["missing"], 0)

    def test_missing_values_are_counted(self):
        info = summarize(["10", "", "30"])
        self.assertEqual(info["type"], "числовая")
        self.assertEqual(info["missing"], 1)
        self.assertEqual(info["mean"], 20.0)

    def test_text_column(self):
        info = summarize(["a", "b", "a"])
        self.assertEqual(info["type"], "текстовая")
        self.assertEqual(info["unique"], 2)
        self.assertEqual(info["top"][0], ("a", 2))


if __name__ == "__main__":
    unittest.main()
