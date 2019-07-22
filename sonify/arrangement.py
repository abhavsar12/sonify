"""This module creates voices that can be used by the sound module to sonify."""


class Track:
    """Class that handles a track with various harmonic voices.

    Atributes:
        _num_voices (int): number of voices.
        _voices (list): list of notes corresponding to each voice.
        _key (str): key of the voices.
        _mode (list): major or minor relationship list.
        _octave (int): starting octave for the first voice.
        _interval_type (list): harmonic relationship of voices.

    """

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
        """Validate and instantiate a Track object.

        Args:
            num_voices (int): Number of voices.
            key (str): Key of the voices.
            mode (list): Major or minor relationship list.
            octave (int): Starting octave for the first voice.
            interval_type (list): Harmonic relationship of voices.

        """
        # Validate and assign interval type

        if self._validate_interval_type(interval_type):
            interval_type = interval_type.lower()
            self._interval_type = self._interval_switcher(interval_type)

        # Validate and assign number of voices and octave
        if self._validate_num_voices_and_octave(num_voices, octave, self._interval_type):
            self._octave = octave
            self._num_voices = num_voices
            self._voices = []

        # Validate and assign key
        if self._validate_key(key):
            self._key = key.upper()

        # Validate and assign mode
        if self._validate_mode(mode):
            mode = mode.lower()
            if mode == 'major':
                self._mode = Track.MAJOR
            elif mode == 'minor':
                self._mode = Track.MINOR

        self._create_voices()

        # Print results

    @staticmethod
    def _validate_interval_type(interval_type):
        """Validate interval type.

        Args:
            interval_type (str): Type of interval for track.

        Returns:
            bool: True if valid interval type.

        Raises:
            TypeError: Interval type type error, string expected.
            ValueError: Invalid interval type.

        """
        try:
            if not isinstance(interval_type, str):
                raise TypeError("Interval type type error, string expected.")

            interval_type = interval_type.lower()
            if interval_type == 'triad' or interval_type == 'fourth' \
               or interval_type == 'fifth' or interval_type == 'maj7' \
               or interval_type == 'octave' or interval_type == 'all':
                return True

            else:
                raise ValueError("Invalid interval type.")

        except ValueError:
            raise

    @staticmethod
    def _validate_num_voices_and_octave(num_voices, octave, interval_type):
        """Validate number of voices and octaves so that the voices stay within C1 - C8.

        Arguements:
            num_voices (int): Number of desired voices.
            octave (int): Starting octave.
            interval_type (list): Type of interval for track.

        Returns:
            bool: True if valid number of voices and starting octave.

        Raises:
            TypeError: Number of voices type error, integer expected.
            TypeError: Octave type error, integer expected.
            ValueError: Octave out of range. Select octave inbetween 1 and 7.
            ValueError: Number of voices cannot be 0 or less than 0.
            ValueError: Range too high. Reduce the number of voices, lower the starting octave,
                        or choose a larger interval type.

        """
        try:
            if not isinstance(num_voices, int):
                raise TypeError("Number of voices type error, integer expected.")
            if not isinstance(octave, int):
                raise TypeError("Octave type error, integer expected.")

            if octave < 1 or octave > 7:
                raise ValueError("Octave out of range. Select octave in between 1 and 7.")

            # Validate and assign number of voices and octave
            if num_voices <= 0:
                raise ValueError("Number of voices cannot be 0 or less than 0.")

            num_extra_octaves = int(num_voices / len(interval_type)) + int(num_voices % len(interval_type) > 0)

            if num_extra_octaves + octave - 1 > 7:
                raise ValueError("Range too high. Reduce the number of voices, "
                                 "lower the starting octave, or choose a larger interval type.")

            return True

        except ValueError:
            raise

    @staticmethod
    def _validate_key(key):
        """Validate key of voices.

        Arguements:
            key (str): Desired key of voices.

        Returns:
            bool: True if valid key given.

        Raises:
            TypeError: Key type error, string expected.
            ValueError: Key is invalid.

        """
        try:
            if not isinstance(key, str):
                raise TypeError("Key type error, string expected.")

            if Track._note_to_num(key) is None:
                raise ValueError("Key is invalid.")

            return True

        except ValueError:
            raise

    @staticmethod
    def _validate_mode(mode):
        """Validate mode of voices.

        Arguements:
            mode (str): Desired mode of voices.

        Returns:
            bool: True if valid mode given.

        Raises:
            TypeError: Mode type error, string expected.
            ValueError: Invalid mode. Choose between major or minor.

        """
        try:
            if not isinstance(mode, str):
                raise TypeError("Mode type error, string expected.")

            mode = mode.lower()
            if mode != 'major' and mode != 'minor':
                raise ValueError("Invalid mode. Choose between major or minor.")

            return True

        except ValueError:
            raise

    @staticmethod
    def _interval_switcher(interval_type):
        """Switch between different interval type based on string input.

        Args:
            interval_type (str): interval type as a string

        Return:
            list: List representation of interval steps

        """
        if interval_type == 'triad':
            return Track.TRIAD
        elif interval_type == 'fourth':
            return Track.FOURTH
        elif interval_type == 'fifth':
            return Track.FIFTH
        elif interval_type == 'maj7':
            return Track.MAJ7
        elif interval_type == 'octave':
            return Track.OCTAVE
        elif interval_type == 'all':
            return Track.ALL

    def _create_voices(self):
        """Assign list of notes as numbers to track."""
        voices = []
        voices.append(self._note_to_num(self._key))
        for i in range(1, self._num_voices):
            voice = voices[0]
            j = i % len(self._interval_type)
            octave = int(i / len(self._interval_type))
            voice += sum(self._mode[0:self._interval_type[j]]) + octave * 12
            voices.append(voice)
        self._voices = voices

    @staticmethod
    def _note_to_num(note):
        """Convert note to number.

        Args:
            note (str): Note to be converted to a number.

        Returns:
            key (str): Key if found, none otherwise.

        """
        for key, vals in Track.NOTES.items():
            val = vals.split('/')
            if note in val:
                return key
        return None

    def _num_to_note(self):
        """Convert voices to notes with respect to octave.

        Returns:
            notes (list): List of notes as strings.

        """
        notes = []
        for i in self._voices:
            octave = self._octave + int(i / 12)
            notes.append(Track.NOTES[i % 12] + str(octave))
        return notes

    def _num_to_freq(self):
        """Convert voices to frequencies in Hz.

        Returns:
            freqs (list): List of frequencies corresponding to all voices.

        """
        freqs = []
        for i in self._voices:
            ind = i + 3 + (self._octave - 5) * 12
            freqs.append(round(Track.A4_HZ * 2 ** (ind / 12), 2))
        return freqs

    @property
    def num_voices(self):
        """Voice number property."""
        return self._num_voices

    @num_voices.setter
    def num_voices(self, new_num_voices):
        """Set new number of voices after validation.

        Args:
            new_num_voices (int): new number of voices.

        """
        if self._validate_num_voices_and_octave(new_num_voices, self._octave, self._interval_type):
            self._num_voices = new_num_voices
            self._create_voices()

    @property
    def key(self):
        """Key property."""
        return self._key

    @key.setter
    def key(self, new_key):
        """Set new key after validation.

        Args:
            new_key (str): new key.

        """
        if self._validate_key(new_key):
            self._key = new_key
            self._create_voices()

    @property
    def mode(self):
        """Mode property."""
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        """Set new mode after validation.

        Args:
            new_mode (str): new mode.

        """
        if self._validate_mode(new_mode):
            self._mode = new_mode
            self._create_voices()

    @property
    def octave(self):
        """Octave property."""
        return self._octave

    @octave.setter
    def octave(self, new_octave):
        """Set new octave after validation.

        Args:
            new_octave (int): new octave.

        """
        if self._validate_num_voices_and_octave(self._num_voices, new_octave, self._interval_type):
            self._octave = new_octave
            self._create_voices()

    @property
    def interval_type(self):
        """Interval type property."""
        return self._interval_type

    @interval_type.setter
    def interval_type(self, new_interval_type):
        """Set new interval type after validation.

        Args:
            new_interval_type (str): new interval type.

        """
        if self._validate_interval_type(new_interval_type):
            new_interval_type = self._interval_switcher(new_interval_type)
            if self._validate_num_voices_and_octave(self._num_voices, self._octave, new_interval_type):
                self._interval_type = new_interval_type
                self._create_voices()

    @property
    def voices(self, freq=False):
        """Voices property."""
        return self._num_to_note()

    @property
    def voice_freqs(self):
        """Voices as frequencies property."""
        return self._num_to_freq()
