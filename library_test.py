import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    def test_comma_separated_integers(self):
        self.assert_extract('test 123,456 test', library.integers, '123,456')

    def test_incorrect_comma_separated_integers(self):
        self.assert_extract('test 1234,56 test', library.integers, '1234', '56')

    def test_dates_fmt2_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_fmt2, '25 Jan, 2017')

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    def test_dates_with_time(self):
        self.assert_extract('I was born on 2015-07-25 18:22.', library.dates_iso8601, '2015-07-25 18:22')

    def test_dates_with_time_seconds(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33.', library.dates_iso8601, '2015-07-25 18:22:33')

    def test_dates_with_time_seconds_tab_delimited(self):
        self.assert_extract('I was born on 2015-07-25\t18:22:33.', library.dates_iso8601, '2015-07-25\t18:22:33')

    def test_dates_with_time_timezone_3(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33 MDT.', library.dates_iso8601, '2015-07-25 18:22:33 MDT')

    def test_dates_with_time_timezone_UTC(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33 Z.', library.dates_iso8601, '2015-07-25 18:22:33 Z')

    def test_dates_with_time_timezone_positive_offset(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33 +0300.', library.dates_iso8601, '2015-07-25 18:22:33 +0300')

    def test_dates_with_time_timezone_negative_offset(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33 -0300.', library.dates_iso8601, '2015-07-25 18:22:33 -0300')

    def test_dates_with_time_incorrect_hours(self):
        self.assert_extract('I was born on 2015-07-25 24:22:33.', library.dates_iso8601, '2015-07-25')

    def test_dates_with_time_incorrect_minutes(self):
        self.assert_extract('I was born on 2015-07-25 23:61:33.', library.dates_iso8601, '2015-07-25')

    def test_dates_with_time_incorrect_seconds(self):
        self.assert_extract('I was born on 2015-07-25 23:21:61.', library.dates_iso8601, '2015-07-25')

    def test_dates_with_time_milliseconds(self):
        self.assert_extract('I was born on 2015-07-25 18:22:33.133.', library.dates_iso8601, '2015-07-25 18:22:33.133')

    def test_incorrect_dates(self):
        self.assert_extract('I was born on 2015-13-25.', library.dates_iso8601)

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)


if __name__ == '__main__':
    unittest.main()
