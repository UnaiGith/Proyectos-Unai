import os
import unittest

from python_uax.files import read_file, append_to_file


class FilesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.remove_file()

    def test_append_and_read_file(self):
        self.assertEqual('File not found!', read_file())

        append_to_file('First line')
        self.assertEqual('First line\n', read_file())

        append_to_file('Second line')
        self.assertEqual('First line\nSecond line\n', read_file())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.remove_file()

    @classmethod
    def remove_file(cls):
        try:
            os.remove('file.txt')  # Remove the file if it exists
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
