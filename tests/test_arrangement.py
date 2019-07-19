import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest  # noqa

from sonify.arrangement import Track  # noqa


class TestArrangement(unittest.TestCase):

    def test_type_errors(self):
        with self.assertRaises(TypeError) as error:
            Track('1', 'C', 'major', 5, 'octave')
        self.assertEqual('Number of voices type error, integer expected.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            Track(1, 1, 'major', 5, 'octave')
        self.assertEqual('Key type error, string expected.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            Track(1, 'C', 1, 5, 'octave')
        self.assertEqual('Mode type error, string expected.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            Track(1, 'C', 'major', 'hi', 'octave')
        self.assertEqual('Octave type error, integer expected.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            Track(1, 'C', 'major', 5, 1)
        self.assertEqual('Interval type type error, string expected.', str(error.exception))

    def test_num_voices_validation(self):
        trck = Track(1, 'C', 'major', 5, 'octave')
        trck.num_voices = 3

        with self.assertRaises(ValueError) as error:
            trck.num_voices = 4
        self.assertEqual('Range too high. Reduce the number of voices, lower the starting octave, '
                         'or choose a larger interval type.', str(error.exception))

        with self.assertRaises(ValueError) as error:
            trck.num_voices = 0
        self.assertEqual('Number of voices cannot be 0 or less than 0.', str(error.exception))

        with self.assertRaises(ValueError) as error:
            trck.num_voices = -1
        self.assertEqual('Number of voices cannot be 0 or less than 0.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            trck.num_voices = [1]
        self.assertEqual('Number of voices type error, integer expected.', str(error.exception))

    def test_octave_validation(self):
        trck = Track(1, 'C', 'major', 4, 'octave')

        trck.num_voices = 3
        with self.assertRaises(ValueError) as error:
            trck.octave = 6
        self.assertEqual('Range too high. Reduce the number of voices, lower the starting octave, '
                         'or choose a larger interval type.', str(error.exception))

        trck.num_voices = 1
        trck.octave = 1
        trck.octave = 7
        with self.assertRaises(ValueError) as error:
            trck.octave = 0
        self.assertEqual('Octave out of range. Select octave in between 1 and 7.', str(error.exception))

        with self.assertRaises(ValueError) as error:
            trck.octave = 8
        self.assertEqual('Octave out of range. Select octave in between 1 and 7.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            trck.octave = '1'
        self.assertEqual('Octave type error, integer expected.', str(error.exception))

    def test_interval_type_validation(self):
        trck = Track(1, 'C', 'major', 4, 'octave')
        trck.interval_type = 'triad'
        trck.interval_type = 'fourth'
        trck.interval_type = 'fifth'
        trck.interval_type = 'maj7'
        trck.interval_type = 'all'

        with self.assertRaises(ValueError) as error:
            trck.interval_type = 'interval type'
        self.assertEqual('Invalid interval type.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            trck.interval_type = 1
        self.assertEqual('Interval type type error, string expected.', str(error.exception))

        trck.num_voices = 5
        with self.assertRaises(ValueError) as error:
            trck.interval_type = 'octave'
        self.assertEqual('Range too high. Reduce the number of voices, lower the starting octave, '
                         'or choose a larger interval type.', str(error.exception))

    def test_key_validation(self):
        trck = Track(1, 'C', 'major', 4, 'octave')
        trck.key = 'A'
        trck.key = 'A#'
        trck.key = 'Bb'
        trck.key = 'B'
        trck.key = 'C'
        trck.key = 'C#'
        trck.key = 'Db'
        trck.key = 'E'
        trck.key = 'F'
        trck.key = 'F#'
        trck.key = 'Gb'
        trck.key = 'G'

        with self.assertRaises(ValueError) as error:
            trck.key = 'H'
        self.assertEqual('Key is invalid.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            trck.key = 1
        self.assertEqual('Key type error, string expected.', str(error.exception))

    def test_mode_validation(self):
        trck = Track(1, 'C', 'major', 4, 'octave')
        trck.mode = 'minor'

        with self.assertRaises(ValueError) as error:
            trck.mode = 'harmonic minor'
        self.assertEqual('Invalid mode. Choose between major or minor.', str(error.exception))

        with self.assertRaises(TypeError) as error:
            trck.mode = 123
        self.assertEqual('Mode type error, string expected.', str(error.exception))


if __name__ == "__main__":
    unittest.main()
