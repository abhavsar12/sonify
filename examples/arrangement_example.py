import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sonify.arrangement import Track # noqa

a = Track(3, 'B', 'major', 2, 'octave')
a.create_voice_notes()
print(a.num_to_note())
print(a.num_to_freq())
