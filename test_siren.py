import unittest
from datetime import date
import siren  


class TestCalculateCycleDay(unittest.TestCase):
    def test_today_as_last_period(self):
        today = date(2025, 4, 17)
        self.assertEqual(siren.calculate_cycle_day(today), 1)

    def test_yesterday_as_last_period(self):
        yesterday = date(2025, 4, 16)
        self.assertEqual(siren.calculate_cycle_day(yesterday), 2)

    def test_week_ago_as_last_period(self):
        week_ago = date(2025, 4, 10)
        self.assertEqual(siren.calculate_cycle_day(week_ago), 8)

    def test_long_ago_as_last_period(self):
        long_ago = date(2025, 3, 20)
        self.assertEqual(siren.calculate_cycle_day(long_ago), 29)

    def test_specific_date(self):
        specific_date = date(2025, 4, 1)
        self.assertEqual(siren.calculate_cycle_day(specific_date), 17)


if __name__ == '__main__':
    unittest.main()