import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sonify.arrangement import Track # noqa

a = Track(3, 'F', 'major', 5, 'octave')
print(a.num_to_note())
print(a.num_to_freq())
a.octave = 4
