from unittest import TestCase

from helpers import get_duplicates


class GetDuplicatesTestCase(TestCase):
    def test_empty_list(self):
        assert get_duplicates([]) == []

    def test_no_duplicates(self):
        assert get_duplicates([1, 2, 3, 4]) == []

    def test_one_duplicate_of_one_value(self):
        assert get_duplicates([1, 1, 2, 3, 4]) == [1]

    def test_multiple_duplicates_of_one_value(self):
        assert get_duplicates([1, 2, 3, 4, 4, 4, 4]) == [4, 4, 4]

    def test_one_duplicate_of_two_values(self):
        assert get_duplicates([1, 2, 2, 3, 3, 4]) == [2, 3]

    def test_multiple_duplicate_of_two_values(self):
        assert get_duplicates([1, 1, 1, 2, 2, 2, 2, 3, 4]) == [1, 1, 2, 2, 2]
