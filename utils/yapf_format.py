'''format a file'''
from yapf.yapflib.yapf_api import FormatFile  # reformat a file
FormatFile('common.py', in_place=True)
FormatFile('data_loader.py', in_place=True)
FormatFile('../model/als_model.py', in_place=True)
FormatFile('../model/lightfm_model.py', in_place=True)
FormatFile('../model/baseline_model.py', in_place=True)
FormatFile('../model/nearest_neighbor_model.py', in_place=True)