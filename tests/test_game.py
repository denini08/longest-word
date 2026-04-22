# tests/test_game.py
from longest_word.game import Game
from unittest.mock import patch, MagicMock
import string

class TestGame:
    def test_game_initialization(self):
        # setup
        fixed_letters = list('ABCDEFGHI')
        with patch('longest_word.game.choice', side_effect=fixed_letters):
            new_game = Game()

        # exercise
        grid = new_game.grid
        # verify
        assert isinstance(grid, list)
        assert len(grid) == 9
        for char in grid:
            assert char in string.ascii_uppercase
        # teardown

    def test_grid_has_exactly_9_letters(self):
        with patch('longest_word.game.choice', return_value='A'):
            new_game = Game()
        assert len(new_game.grid) == 9

    def test_empty_word_is_invalid(self):
        with patch('longest_word.game.choice', return_value='A'):
            new_game = Game()
        assert new_game.is_valid('') is False

    def test_is_valid(self):
        new_game = Game()

        new_game.grid = list('AOYNMLPIYUP')

        assert new_game.is_valid('OLYMPIAN') == True
        assert new_game.grid == list('AOYNMLPIYUP')

    def test_is_invalid(self):
        new_game = Game()

        new_game.grid = list('AOYNLPIYUP')

        assert new_game.is_valid('OLYMPIAN') == False
        assert new_game.grid == list('AOYNLPIYUP')

    def test_unknown_word_is_invalid(self):
        """A word that is not in the English dictionary should not be valid"""
        new_game = Game()
        new_game.grid = list('KWIENFUQW') # Force the grid to a test case:
        assert new_game.is_valid('FEUN') is False

    def test_word_uses_each_letter_only_once(self):
        # Grid has only one 'A' — a word needing two should be invalid
        new_game = Game()
        new_game.grid = list('ABCDEFGHI')
        with patch.object(Game, '_Game__check_dictionary', return_value=True):
            assert new_game.is_valid('AA') is False

    def test_valid_word_does_not_mutate_grid(self):
        new_game = Game()
        new_game.grid = list('AOYNMLPIYUP')
        original = new_game.grid.copy()
        new_game.is_valid('OLYMPIAN')
        assert new_game.grid == original

    def test_dictionary_error_returns_invalid(self):
        new_game = Game()
        new_game.grid = list('HELLOABCD')
        with patch('longest_word.game.get', side_effect=Exception('network error')):
            assert new_game.is_valid('HELLO') is False

    def test_word_not_in_grid_skips_dictionary(self):
        # Letters not in grid — __check_dictionary should never be called
        new_game = Game()
        new_game.grid = list('ABCDEFGHI')
        with patch.object(Game, '_Game__check_dictionary') as mock_dict:
            result = new_game.is_valid('ZZZZZ')
        assert result is False
        mock_dict.assert_not_called()
