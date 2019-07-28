import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sonify.arrangement import Track # noqa
import sonify.dataproccess as dp # noqa
import sonify.soundgen as sg # noqa

voices = 16

folder = '../data/'
data_file = 'sample_sine.json'
json_file = open(folder + data_file)
data = json.load(json_file)

data = dp.norm_and_quantize_data(data, voices)
data = dp.gen_sonification_mat(data, voices, 0.1, 0.5)

a = Track(voices, 'F', 'minor', 2, 'triad')
trck = sg.arrange_harmonies(a.voice_freqs, 5)
print(trck.shape)
trck = sg.sonify_data(trck, data)
print(trck.shape)
trck = sg.render_track(trck)
print(trck.shape)

sg.play_track(trck)
