import unittest

from python_uax.data_structures import reverse_list, get_elements_between_positions, get_dict_items_by_keys, \
    get_letters_in_first_word_but_not_in_second, get_names_of_adults, get_value_of_key_with_highest_number, \
    get_number_of_times_number_appears_in_both_lists


class DataStructuresTestCase(unittest.TestCase):
    def test_reverse_list(self):
        list_of_ints = [1, 2, 3, 4, 5]
        self.assertEqual([5, 4, 3, 2, 1], reverse_list(list_of_ints))
        self.assertEqual([1, 2, 3, 4, 5], list_of_ints)  # check original list wasn't modified

        list_of_strings = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(['e', 'd', 'c', 'b', 'a'], reverse_list(list_of_strings))
        self.assertEqual(['a', 'b', 'c', 'd', 'e'], list_of_strings)  # check original list wasn't modified

    def test_get_elements_between_positions(self):
        l = ['a', 'b', 'c', 'd', 'e']

        self.assertEqual(
            "Elements between positions 1 and 3 (included): ['b', 'c', 'd']",
            get_elements_between_positions(l, 1, 3))
        self.assertEqual(
            "Elements between positions 1 and 1 (included): ['b']",
            get_elements_between_positions(l, 1))

        self.assertRaises(ValueError, get_elements_between_positions, l, 2, 1)
        self.assertRaises(ValueError, get_elements_between_positions, l, -1, 1)
        self.assertRaises(ValueError, get_elements_between_positions, l, 1, 5)

    def test_get_number_of_times_number_appears_in_both_lists(self):
        l1 = [1, 2, 3, 1, 2, 4]
        l2 = [1, 2, 3, 5]

        self.assertEqual(1, get_number_of_times_number_appears_in_both_lists(l1, l2, 1))
        self.assertEqual(1, get_number_of_times_number_appears_in_both_lists(l1, l2, 2))
        self.assertEqual(1, get_number_of_times_number_appears_in_both_lists(l1, l2, 3))
        self.assertEqual(0, get_number_of_times_number_appears_in_both_lists(l1, l2, 4))
        self.assertEqual(0, get_number_of_times_number_appears_in_both_lists(l1, l2, 5))
        self.assertEqual(0, get_number_of_times_number_appears_in_both_lists(l1, l2, 6))

    def test_get_names_of_adults(self):
        self.assertEqual(['Peter', 'Jane', 'Mark'],get_names_of_adults({'John': 16, 'Mary': 17, 'Peter': 18, 'Jane': 19, 'Mark': 20}))
        self.assertEqual(['Peter', 'Jane'], get_names_of_adults({'John': 16, 'Mary': 17, 'Peter': 18, 'Jane': 19}))
        self.assertEqual(['Peter'], get_names_of_adults({'John': 16, 'Mary': 17, 'Peter': 18}))
        self.assertEqual([], get_names_of_adults({'John': 16, 'Mary': 17}))

    def test_get_dict_items_by_keys(self):
        d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

        self.assertEqual(
            [('a', 1), ('c', 3)],
            get_dict_items_by_keys(d, ['a', 'c']))
        self.assertEqual(
            [('a', 1), ('b', 2), ('c', 3), ('d', 4)],
            get_dict_items_by_keys(d))

    def test_get_value_of_key_with_highest_number(self):
        self.assertEqual('b', get_value_of_key_with_highest_number({2: 'a', 4: 'b', 1: 'c', 3: 'd'}))
        self.assertEqual('e', get_value_of_key_with_highest_number({2: 'a', 4: 'b', 1: 'c', 3: 'd', 5: 'e'}))

    def test_get_letters_in_first_word_but_not_in_second(self):
        self.assertEqual({'h'}, get_letters_in_first_word_but_not_in_second('house', 'mouse'))
        self.assertEqual({'u', 's'}, get_letters_in_first_word_but_not_in_second('house', 'home'))
        self.assertEqual(set(), get_letters_in_first_word_but_not_in_second('house', 'house'))


if __name__ == '__main__':
    unittest.main()
