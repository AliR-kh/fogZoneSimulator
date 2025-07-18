from env import Env
import torch

import torch.nn as nn
import torch.nn.functional as F
import numpy as np


tasks=[{'id': 'ID00000', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.45', 'device_id': 0, 'sizein': 4222384, 'sizeout': 8299550, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00000', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.45', 'device_id': 1, 'sizein': 4222384, 'sizeout': 8299550, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00000', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.45', 'device_id': 2, 'sizein': 4222384, 'sizeout': 8299550, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00001', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.86', 'device_id': 0, 'sizein': 4222384, 'sizeout': 8348380, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00001', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.86', 'device_id': 1, 'sizein': 4222384, 'sizeout': 8348380, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00001', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.86', 'device_id': 2, 'sizein': 4222384, 'sizeout': 8348380, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00002', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.50', 'device_id': 0, 'sizein': 4222384, 'sizeout': 8289590, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00002', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.50', 'device_id': 1, 'sizein': 4222384, 'sizeout': 8289590, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00002', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.50', 'device_id': 2, 'sizein': 4222384, 'sizeout': 8289590, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00003', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.46', 'device_id': 0, 'sizein': 4222384, 'sizeout': 8293698, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00003', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.46', 'device_id': 1, 'sizein': 4222384, 'sizeout': 8293698, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00003', 'namespace': 'Montage', 'name': 'mProjectPP', 'version': '1.0', 'runtime': '13.46', 'device_id': 2, 'sizein': 4222384, 'sizeout': 8293698, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': []},
 {'id': 'ID00004', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.80', 'device_id': 0, 'sizein': 8299854, 'sizeout': 214929, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00000']},
 {'id': 'ID00004', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.80', 'device_id': 1, 'sizein': 8299854, 'sizeout': 214929, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00000']},
 {'id': 'ID00004', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.80', 'device_id': 2, 'sizein': 8299854, 'sizeout': 214929, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00000']},
 {'id': 'ID00005', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.57', 'device_id': 0, 'sizein': 16650024, 'sizeout': 286771, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00000']},
 {'id': 'ID00005', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.57', 'device_id': 1, 'sizein': 16650024, 'sizeout': 286771, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00000']},
 {'id': 'ID00005', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.57', 'device_id': 2, 'sizein': 16650024, 'sizeout': 286771, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00000']},
 {'id': 'ID00006', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.49', 'device_id': 0, 'sizein': 16584640, 'sizeout': 371182, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00000']},
 {'id': 'ID00006', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.49', 'device_id': 1, 'sizein': 16584640, 'sizeout': 371182, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00000']},
 {'id': 'ID00006', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.49', 'device_id': 2, 'sizein': 16584640, 'sizeout': 371182, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00000']},
 {'id': 'ID00007', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.52', 'device_id': 0, 'sizein': 16634516, 'sizeout': 279275, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00001']},
 {'id': 'ID00007', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.52', 'device_id': 1, 'sizein': 16634516, 'sizeout': 279275, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00001']},
 {'id': 'ID00007', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.52', 'device_id': 2, 'sizein': 16634516, 'sizeout': 279275, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00001']},
 {'id': 'ID00008', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.59', 'device_id': 0, 'sizein': 8289894, 'sizeout': 190341, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002']},
 {'id': 'ID00008', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.59', 'device_id': 1, 'sizein': 8289894, 'sizeout': 190341, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002']},
 {'id': 'ID00008', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.59', 'device_id': 2, 'sizein': 8289894, 'sizeout': 190341, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002']},
 {'id': 'ID00009', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.54', 'device_id': 0, 'sizein': 16667736, 'sizeout': 353586, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00002']},
 {'id': 'ID00009', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.54', 'device_id': 1, 'sizein': 16667736, 'sizeout': 353586, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00002']},
 {'id': 'ID00009', 'namespace': 'Montage', 'name': 'mDiffFit', 'version': '1.0', 'runtime': '10.54', 'device_id': 2, 'sizein': 16667736, 'sizeout': 353586, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00002']},
 {'id': 'ID00010', 'namespace': 'Montage', 'name': 'mConcatFit', 'version': '1.0', 'runtime': '0.48', 'device_id': 0, 'sizein': 1696247, 'sizeout': 1259, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00006', 'ID00005', 'ID00004', 'ID00009', 'ID00008', 'ID00007']},
 {'id': 'ID00010', 'namespace': 'Montage', 'name': 'mConcatFit', 'version': '1.0', 'runtime': '0.48', 'device_id': 1, 'sizein': 1696247, 'sizeout': 1259, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00006', 'ID00005', 'ID00004', 'ID00009', 'ID00008', 'ID00007']},
 {'id': 'ID00010', 'namespace': 'Montage', 'name': 'mConcatFit', 'version': '1.0', 'runtime': '0.48', 'device_id': 2, 'sizein': 1696247, 'sizeout': 1259, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00006', 'ID00005', 'ID00004', 'ID00009', 'ID00008', 'ID00007']},
 {'id': 'ID00011', 'namespace': 'Montage', 'name': 'mBgModel', 'version': '1.0', 'runtime': '0.77', 'device_id': 0, 'sizein': 1929, 'sizeout': 212, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00010']},
 {'id': 'ID00011', 'namespace': 'Montage', 'name': 'mBgModel', 'version': '1.0', 'runtime': '0.77', 'device_id': 1, 'sizein': 1929, 'sizeout': 212, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00010']},
 {'id': 'ID00011', 'namespace': 'Montage', 'name': 'mBgModel', 'version': '1.0', 'runtime': '0.77', 'device_id': 2, 'sizein': 1929, 'sizeout': 212, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00010']},
 {'id': 'ID00012', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.81', 'device_id': 0, 'sizein': 8292552, 'sizeout': 8292340, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00011', 'ID00000']},
 {'id': 'ID00012', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.81', 'device_id': 1, 'sizein': 8292552, 'sizeout': 8292340, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00011', 'ID00000']},
 {'id': 'ID00012', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.81', 'device_id': 2, 'sizein': 8292552, 'sizeout': 8292340, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00011', 'ID00000']},
 {'id': 'ID00013', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.55', 'device_id': 0, 'sizein': 8316168, 'sizeout': 8315956, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00011']},
 {'id': 'ID00013', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.55', 'device_id': 1, 'sizein': 8316168, 'sizeout': 8315956, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00011']},
 {'id': 'ID00013', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.55', 'device_id': 2, 'sizein': 8316168, 'sizeout': 8315956, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00001', 'ID00011']},
 {'id': 'ID00014', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.68', 'device_id': 0, 'sizein': 8292710, 'sizeout': 8292498, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002', 'ID00011']},
 {'id': 'ID00014', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.68', 'device_id': 1, 'sizein': 8292710, 'sizeout': 8292498, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002', 'ID00011']},
 {'id': 'ID00014', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.68', 'device_id': 2, 'sizein': 8292710, 'sizeout': 8292498, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00002', 'ID00011']},
 {'id': 'ID00015', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.89', 'device_id': 0, 'sizein': 8334098, 'sizeout': 8333886, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00011']},
 {'id': 'ID00015', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.89', 'device_id': 1, 'sizein': 8334098, 'sizeout': 8333886, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00011']},
 {'id': 'ID00015', 'namespace': 'Montage', 'name': 'mBackground', 'version': '1.0', 'runtime': '10.89', 'device_id': 2, 'sizein': 8334098, 'sizeout': 8333886, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00003', 'ID00011']},
 {'id': 'ID00016', 'namespace': 'Montage', 'name': 'mImgTbl', 'version': '1.0', 'runtime': '1.48', 'device_id': 0, 'sizein': 33235350, 'sizeout': 1516, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00015', 'ID00014', 'ID00013', 'ID00012']},
 {'id': 'ID00016', 'namespace': 'Montage', 'name': 'mImgTbl', 'version': '1.0', 'runtime': '1.48', 'device_id': 1, 'sizein': 33235350, 'sizeout': 1516, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00015', 'ID00014', 'ID00013', 'ID00012']},
 {'id': 'ID00016', 'namespace': 'Montage', 'name': 'mImgTbl', 'version': '1.0', 'runtime': '1.48', 'device_id': 2, 'sizein': 33235350, 'sizeout': 1516, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00015', 'ID00014', 'ID00013', 'ID00012']},
 {'id': 'ID00017', 'namespace': 'Montage', 'name': 'mAdd', 'version': '1.0', 'runtime': '2.40', 'device_id': 0, 'sizein': 1820, 'sizeout': 98073828, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00016']},
 {'id': 'ID00017', 'namespace': 'Montage', 'name': 'mAdd', 'version': '1.0', 'runtime': '2.40', 'device_id': 1, 'sizein': 1820, 'sizeout': 98073828, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00016']},
 {'id': 'ID00017', 'namespace': 'Montage', 'name': 'mAdd', 'version': '1.0', 'runtime': '2.40', 'device_id': 2, 'sizein': 1820, 'sizeout': 98073828, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00016']},
 {'id': 'ID00018', 'namespace': 'Montage', 'name': 'mShrink', 'version': '1.0', 'runtime': '3.45', 'device_id': 0, 'sizein': 98073828, 'sizeout': 1962261, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00017']},
 {'id': 'ID00018', 'namespace': 'Montage', 'name': 'mShrink', 'version': '1.0', 'runtime': '3.45', 'device_id': 1, 'sizein': 98073828, 'sizeout': 1962261, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00017']},
 {'id': 'ID00018', 'namespace': 'Montage', 'name': 'mShrink', 'version': '1.0', 'runtime': '3.45', 'device_id': 2, 'sizein': 98073828, 'sizeout': 1962261, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00017']},
 {'id': 'ID00019', 'namespace': 'Montage', 'name': 'mJPEG', 'version': '1.0', 'runtime': '0.35', 'device_id': 0, 'sizein': 1962261, 'sizeout': 181372, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00018']},
 {'id': 'ID00019', 'namespace': 'Montage', 'name': 'mJPEG', 'version': '1.0', 'runtime': '0.35', 'device_id': 1, 'sizein': 1962261, 'sizeout': 181372, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00018']},
 {'id': 'ID00019', 'namespace': 'Montage', 'name': 'mJPEG', 'version': '1.0', 'runtime': '0.35', 'device_id': 2, 'sizein': 1962261, 'sizeout': 181372, 'start_time': 0, 'time': 0, 'makespan': 0, 'time_queue': 0, 'id_resource': 0, 'energy': 0, 'cost': 0, 'transfer_time_input': 0, 'transfer_time_output': 0, 'execution': 0, 'type_resource': 0, 'parentid': ['ID00018']}]


resources=[{'id': 0, 'type': 'Fog', 'mips': 1500, 'ratepermipscost': 0.48, 'parentid': 0, 'con_pow_active': 500, 'con_pow_idle': 200, 'down_bw': 1000, 'down_cost': 0.04, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.04, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'inter_time': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 1, 'type': 'Fog', 'mips': 1500, 'ratepermipscost': 0.48, 'parentid': 0, 'con_pow_active': 500, 'con_pow_idle': 200, 'down_bw': 1000, 'down_cost': 0.04, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.04, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'inter_time': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 2, 'type': 'Fog', 'mips': 1500, 'ratepermipscost': 0.48, 'parentid': 0, 'con_pow_active': 500, 'con_pow_idle': 200, 'down_bw': 1000, 'down_cost': 0.04, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.04, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'inter_time': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 3, 'type': 'Fog', 'mips': 1500, 'ratepermipscost': 0.48, 'parentid': 0, 'con_pow_active': 500, 'con_pow_idle': 200, 'down_bw': 1000, 'down_cost': 0.04, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.04, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'inter_time': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 4, 'type': 'Fog', 'mips': 1500, 'ratepermipscost': 0.48, 'parentid': 0, 'con_pow_active': 500, 'con_pow_idle': 200, 'down_bw': 1000, 'down_cost': 0.04, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.04, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'inter_time': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 0, 'type': 'Cloud', 'ratepermipscost': 0.96, 'mips': 2000, 'con_pow_active': 700, 'con_pow_idle': 400, 'down_bw': 1000, 'down_cost': 0.02, 'up_bw': 1000, 'down_energy': 50, 'up_cost': 0.02, 'up_energy': 50, 'exec_cost': 0.96, 'memory_cost_unit': 0, 'exist_flag': 0, 'memory_size': 0, 'inter_time': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 1, 'type': 'Cloud', 'ratepermipscost': 0.96, 'mips': 2000, 'con_pow_active': 700, 'con_pow_idle': 400, 'down_bw': 1000, 'down_cost': 0.02, 'up_bw': 1000, 'down_energy': 50, 'up_cost': 0.02, 'up_energy': 50, 'exec_cost': 0.96, 'memory_cost_unit': 0, 'exist_flag': 0, 'memory_size': 0, 'inter_time': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 2, 'type': 'Cloud', 'ratepermipscost': 0.96, 'mips': 2000, 'con_pow_active': 700, 'con_pow_idle': 400, 'down_bw': 1000, 'down_cost': 0.02, 'up_bw': 1000, 'down_energy': 50, 'up_cost': 0.02, 'up_energy': 50, 'exec_cost': 0.96, 'memory_cost_unit': 0, 'exist_flag': 0, 'memory_size': 0, 'inter_time': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 0, 'type': 'Edge', 'mips': 1000, 'ratepermipscost': 0, 'con_pow_active': 200, 'con_pow_idle': 50, 'down_bw': 1000, 'down_cost': 0.08, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.08, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 1, 'type': 'Edge', 'mips': 1000, 'ratepermipscost': 0, 'con_pow_active': 200, 'con_pow_idle': 50, 'down_bw': 1000, 'down_cost': 0.08, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.08, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0},
 {'id': 2, 'type': 'Edge', 'mips': 1000, 'ratepermipscost': 0, 'con_pow_active': 200, 'con_pow_idle': 50, 'down_bw': 1000, 'down_cost': 0.08, 'down_energy': 50, 'up_bw': 1000, 'up_cost': 0.08, 'up_energy': 50, 'memory_cost_unit': 0, 'exist_flag': 0, 'exec_cost': 0, 'memory_size': 0, 'time': 0, 'idle_energy': 0, 'active_energy': 0, 'total_energy': 0, 'cost_process': 0, 'cost_transfer': 0, 'cost_memory': 0, 'total_cost': 0, 'assigned_mips': 0}]



class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, seed=42):
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, action_size)
        self.dropout = nn.Dropout(p=0.1)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = self.dropout(F.relu(self.fc2(x)))
        x = F.relu(self.fc3(x))
        return self.fc4(x)



def _modif_action(action):
    if action==0:
        return {"id":action, "resource":{"type":"edge"}}
    elif action==1:
        return {"id":action, "resource":{"type":"cloud"}}
    elif action==2:
        return {"id":action, "resource":{"type":"fog"}}


# ==============================================================================
# ۱. تعریف مجدد ساختار شبکه و محیط
# ==============================================================================

# تعریف مجدد کلاس شبکه عصبی (باید دقیقا مشابه زمان آموزش باشد)
# پارامترهای مدل
STATE_SIZE = 3
ACTION_SIZE = 3
MODEL_PATH = 'dqn_scheduler_model_modified5.pth' # مسیر فایل ذخیره شده

# ساخت یک نمونه از شبکه
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)

# بارگذاری وزن‌های آموزش‌دیده
try:
    model.load_state_dict(torch.load(MODEL_PATH))
    print(f"مدل با موفقیت از مسیر '{MODEL_PATH}' بارگذاری شد.")
except FileNotFoundError:
    print(f"خطا: فایل مدل در مسیر '{MODEL_PATH}' پیدا نشد. لطفاً ابتدا مدل را آموزش و ذخیره کنید.")
    exit()


# قرار دادن مدل در حالت ارزیابی (بسیار مهم)
# این کار لایه‌هایی مثل Dropout یا BatchNorm را غیرفعال می‌کند
model.eval()

# ==============================================================================
# ۳. اجرای مدل روی تسک‌های جدید و نمایش خروجی
# ==============================================================================

def schedule_tasks_with_model(trained_model):
    """
    از مدل آموزش‌دیده برای تخصیص مجموعه‌ای از تسک‌ها استفاده می‌کند.
    
    Args:
        trained_model: مدل QNetwork که وزن‌های آن بارگذاری شده.
        env_instance: یک نمونه از کلاس محیط شما.
        num_tasks: تعداد تسک‌هایی که باید زمان‌بندی شوند.
        
    Returns:
        یک آرایه NumPy شامل دنباله‌ای از اقدامات (شماره منابع) انتخاب‌شده.
    """
    # print(f"\nشروع زمان‌بندی برای {} تسک جدید...")
    
    # ریست کردن محیط
    env_instance=Env(resources=resources,tasks=tasks)
    env_instance.reset()
    action_sequence = []
    
    # این حلقه باید با torch.no_grad() اجرا شود تا محاسبات گرادیان انجام نشود
    with torch.no_grad():
        for task_index in range(len(env_instance.tasks)):
            # گرفتن وضعیت فعلی از محیط
            env_instance._temporary_state(task_index)
            normalized_state =env_instance.temp_state
            state_tensor = torch.tensor([normalized_state], device=device, dtype=torch.float32)

            # استفاده از مدل برای پیش‌بینی بهترین اقدام (بدون اپسیلون)
            # .max(1)[1] مقدار بیشینه و اندیس آن را برمی‌گرداند. ما به اندیس نیاز داریم.
            action = trained_model(state_tensor).max(1)[1].item()
            modif_act=_modif_action(action)
            # ذخیره اقدام انتخاب‌شده
            action_sequence.append(action)
            
            # به‌روزرسانی محیط با اقدام انجام‌شده
            _, _, _, done = env_instance.step(task_index, modif_act)
            
            if done:
                print("همه تسک‌ها زمان‌بندی شدند.")
                break
                
    return np.array(action_sequence)

# --- اجرای نمونه ---
# یک نمونه از محیط خود بسازید
# تعداد تسک‌های مورد نظر برای تست را مشخص کنید
NUM_TEST_TASKS = 100

# اجرای تابع زمان‌بندی
final_schedule = schedule_tasks_with_model(model)

# نمایش آرایه نهایی انتخاب‌ها
print("\n" + "="*40)
print("final result")
# print(f"دنباله تخصیص تسک‌ها به منابع (منبع 0 تا {ACTION_SIZE-1}):")
print(f"{final_schedule}")
print("="*40)
