from japanese_crossword.helpers import find_first_1_index, find_last_1_index


class TestFindLast1Index:
    def test_returns_correct_index_for_complex_input(self):
        assert find_last_1_index([None, 1, 1, None, None, 1, 1, 1, 1, 1, None]) == 9

    def test_returns_correct_index_for_just_one_1(self):
        assert find_last_1_index([1]) == 0

    def test_returns_correct_index_for_several_1(self):
        assert find_last_1_index([1, 1, 1, 1, 1]) == 4

    def test_returns_minus_one(self):
        assert find_last_1_index([None, None]) == -1


class TestFindFirst1Index:
    def test_index_returns_correct_index_for_complex_input(self):
        assert find_first_1_index([None, 1, 1, None, None, 1]) == 1


    def test_returns_correct_index_for_just_one_1(self):
        assert find_first_1_index([1]) == 0


    def test_returns_correct_index_for_several_1(self):
        assert find_first_1_index([1, 1, 1]) == 0


    def test_returns_minus_one(self):
        assert find_first_1_index([None, None]) == -1
