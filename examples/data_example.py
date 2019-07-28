import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sonify import dataproccess as dp # noqa

folder = '../data/'
data_file = 'sample_line.json'
json_file = open(folder + data_file)
data = json.load(json_file)

data = dp.norm_and_quantize_data(data, 16)
print(data[1])
data = dp.gen_sonification_mat(data, 16, 0.1, 0.5)
print(data)
