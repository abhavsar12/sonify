"""This module creates voices that can be used by the sound module to sonify."""


class Track:
    """Class that handles a track with various harmonic voices."""

    NOTES = {0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F',
             6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'}
    A4_HZ = 440
    MAJOR = [2, 2, 1, 2, 2, 2, 1]
    MINOR = [2, 1, 2, 2, 1, 2, 2]

    TRIAD = [0, 2, 4]
    FOURTH = [0, 3]
    FIFTH = [0, 4]
    MAJ7 = [0, 2, 4, 6]
    OCTAVE = [0]
    ALL = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self, num_voices, key, mode, octave, interval_type):
        """Validates and instantiates a Track object.

        Attributes:
            num_voices (int): number of voices
            voices (list): list of notes corresponding to each voice
            key (str): key of the voices
            mode (list): major or minor relationship list
            octave (int): starting octave for the first voice
            interval_type (list): harmonic relationship of voices

        """
        # Validate and assign interval type
        interval_type = interval_type.lower()
        if self.validate_interval_type(interval_type):
            if interval_type == 'triad':
                self.interval_type = Track.TRIAD
            elif interval_type == 'fourth':
                self.interval_type = Track.FOURTH
            elif interval_type == 'fifth':
                self.interval_type = Track.FIFTH
            elif interval_type == 'maj7':
                self.interval_type = Track.MAJ7
            elif interval_type == 'octave':
                self.interval_type = Track.OCTAVE
            elif interval_type == 'all':
                self.interval_type = Track.ALL

        # Validate and assign number of voices and octave
        if self.validate_num_voices_and_octave(num_voices, octave, self.interval_type):
            self.octave = octave
            self.num_voices = num_voices
            self.voice = []

        # Validate and assign key
        if self.validate_key(key):
            self.key = key.upper()

        # Validate and assign mode
        if self.validate_mode(mode):
            mode = mode.lower()
            if mode == 'major':
                self.mode = Track.MAJOR
            elif mode == 'minor':
                self.mode = Track.MINOR

        # Print results

    @staticmethod
    def validate_interval_type(interval_type):
        try:
            if interval_type == 'triad' or interval_type == 'fourth' \
               or interval_type == 'fifth' or interval_type == 'maj7' \
               or interval_type == 'octave' or interval_type == 'all':
                return True

            else:
                raise ValueError("Invalid interval type")

        except ValueError:
            raise

    @staticmethod
    def validate_num_voices_and_octave(num_voices, octave, interval_type):
        try:
            if octave < 1 or octave > 7:
                raise ValueError("Octave out of range. Select octave inbetween 1 and 7.")

            # Validate and assign number of voices and octave
            if num_voices <= 0:
                raise ValueError("Number of voices cannot be 0 or less than 0.")

            num_extra_octaves = int(num_voices / len(interval_type)) + int(num_voices % len(interval_type) > 0)

            if num_extra_octaves + octave - 1 > 7:
                raise ValueError("Range too high. Reduce the number of voices or lower the starting octave.")

            return True

        except ValueError:
            raise

    @staticmethod
    def validate_key(key):
        try:
            if Track.note_to_num(key.upper()) is None:
                raise ValueError("Key is invalid")

            return True

        except ValueError:
            raise

    @staticmethod
    def validate_mode(mode):
        try:
            mode = mode.lower()
            if mode != 'major' and mode != 'minor':
                raise ValueError("Invalid mode. Choose between major or minor.")

            return True

        except ValueError:
            raise

    def create_voice_notes(self):
        """Assign list of notes as numbers to track."""
        voices = []
        voices.append(self.note_to_num(self.key))
        for i in range(1, self.num_voices):
            voice = voices[0]
            j = i % len(self.interval_type)
            octave = int(i / len(self.interval_type))
            voice += sum(self.mode[0:self.interval_type[j]]) + octave * 12
            voices.append(voice)
        self.voices = voices

    # make normal methods, add list conversions and octave range conversions
    @staticmethod
    def note_to_num(note):
        """Convert note to number.

        Arguments:
            note (str): note to be converted to a number

        Returns:
            key (str): key if found, none otherwise

        """
        for key, vals in Track.NOTES.items():
            val = vals.split('/')
            if note in val:
                return key
        return None

    def num_to_note(self):
        """Convert voices to notes with respect to octave.

        Returns:
            notes (list): list of notes as strings

        """
        notes = []
        for i in self.voices:
            octave = self.octave + int(i / 12)
            notes.append(Track.NOTES[i % 12] + str(octave))
        return notes

    def num_to_freq(self):
        """Convert voices to frequencies in Hz.

        Returns:
            freqs (list): list of frequencies corresponding to all voices

        """
        freqs = []
        for i in self.voices:
            ind = i + 3 + (self.octave - 5) * 12
            freqs.append(round(Track.A4_HZ * 2 ** (ind / 12), 2))
        return freqs
