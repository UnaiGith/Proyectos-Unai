import unittest

from python_uax.functions import concat_words_with_prefix, make_multiplier_of


class FunctionsTestCase(unittest.TestCase):
    def test_concat_words_with_prefix(self):
        self.assertEqual(['superhero'], concat_words_with_prefix('super', 'hero'))
        self.assertEqual(['superhero', 'superstar'], concat_words_with_prefix('super', 'hero', 'star'))
        self.assertEqual(['superhero', 'superstar', 'superpower'], concat_words_with_prefix('super', 'hero', 'star', 'power'))
        self.assertEqual(['submarine', 'subway', 'subtitle'], concat_words_with_prefix('sub', 'marine', 'way', 'title'))

    def test_make_multiplier_of(self):
        times_3 = make_multiplier_of(3)
        self.assertEqual(6, times_3(2))
        self.assertEqual(9, times_3(3))

        times_5 = make_multiplier_of(5)
        self.assertEqual(10, times_5(2))
        self.assertEqual(15, times_5(3))


if __name__ == '__main__':
    unittest.main()
