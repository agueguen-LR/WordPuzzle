# test_puzzleMaker.py mostly generated by Copilot
import unittest
import numpy as np
from puzzleGenerator.puzzleMaker import __word_can_be_placed as word_can_be_placed

class TestWordCanBePlaced(unittest.TestCase):
    def setUp(self):
        self.puzzleDimensions = (13, 6)
        self.occupiedSpaces = np.zeros(self.puzzleDimensions, dtype=int)

    def test_word_can_be_placed_vertically(self):
        word = "TEST"
        intersectionTuple = (5, 2, True, 'E')
        self.occupiedSpaces[5, 2] = 1  # Simulate the intersection word
        self.occupiedSpaces[6, 2] = 1
        self.assertNotEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_out_of_bounds(self):
        word = "LONGWORD"
        intersectionTuple = (5, 5, True, 'O')
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_vertical_with_adjacent_right_word(self):
        word = "TEST"
        intersectionTuple = (5, 0, True, 'E')
        self.occupiedSpaces[6, 2] = 1  # Simulate an adjacent word
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_vertical_with_adjacent_left_word(self):
        word = "TEST"
        intersectionTuple = (7, 0, True, 'E')
        self.occupiedSpaces[6, 2] = 1  # Simulate an adjacent word
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_horizontal_with_adjacent_above_word(self):
        word = "TEST"
        intersectionTuple = (4, 1, False, 'E')
        self.occupiedSpaces[6, 2] = 1  # Simulate an adjacent word
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_horizontal_with_adjacent_below_word(self):
        word = "TEST"
        intersectionTuple = (7, 3, False, 'E')
        self.occupiedSpaces[6, 2] = 1  # Simulate an adjacent word
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_can_be_placed_horizontally(self):
        word = "TEST"
        intersectionTuple = (5, 2, False, 'E')
        self.occupiedSpaces[5, 2] = 1  # Simulate the intersection word
        self.occupiedSpaces[5, 3] = 1
        self.assertNotEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

    def test_word_cannot_be_placed_if_intersection_letter_not_in_word(self):
        word = "TEST"
        intersectionTuple = (5, 2, True, 'X')
        self.assertEqual(word_can_be_placed(word, intersectionTuple, self.occupiedSpaces, self.puzzleDimensions), -1)

if __name__ == '__main__':
    unittest.main()