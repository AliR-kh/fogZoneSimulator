
from env import Env
import random


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

env=Env(tasks,resources)



print(f" max_load_edge {env.max_load_Edge} \n max_load_fog {env.max_load_fog} \n max_load_cloud {env.max_load_cloud}")


def action():
    action=2 #random.randint(2,2)
    if action==0:
        return {"id":action, "resource":{"type":"edge"}}
    elif action==1:
        return {"id":action, "resource":{"type":"cloud"}}
    elif action==2:
        return {"id":action, "resource":{"type":"fog"}}

# for i in range(len(env.tasks)):
#     print(f"****************************** task_id : {env.tasks[i]["id"]} ********************************")
#     print(f"****************************** device_id : {env.tasks[i]["device_id"]} ********************************")
    
    
#     print("\n++++++++++++++++++++++++++++++++ befor action ++++++++++++++++++++++++++++++++++")
#     print(f"\n assigend_edge : {env.assigned_to_edges}")
#     print(f"\n assigend_fogs : {env.assigned_to_fogs}")
#     print(f"\n assigend_cloud : {env.assigned_to_clouds}")
#     print(f"\n state is : {env.state}")
#     print(f"\n temporary state is : {env._temporary_state(i)}")
#     print("\n ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ after action ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#     act=action()
#     _,_,reward,done=env.step(i,act)
#     env._temporary_state(i)
#     print(f"\n action is : {act}")
#     print(f"\n assigend_edge : {env.assigned_to_edges}")
#     print(f"\n assigend_fogs : {env.assigned_to_fogs}")
#     print(f"\n assigend_cloud : {env.assigned_to_clouds}")
#     print(f"\n state is : {env.state}")
#     print(f"\n temporary state is : {env.temp_state}")
#     print(f"\n rewarrrd is : {reward}")

#     if i==10:
#         break
    
    
    
    
    
    
    
    
    
    
# from Env.engine import Engine
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import math
from collections import namedtuple, deque
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# یک ساختمان داده برای ذخیره تجربیات
Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'done'))

class ReplayBuffer:
    """بافر برای ذخیره و بازیابی تجربیات جهت آموزش"""
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """یک تجربه را ذخیره می‌کند"""
        self.memory.append(Experience(*args))

    def sample(self, batch_size):
        """یک دسته تصادفی از تجربیات را برمی‌گرداند"""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

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

# ==============================================================================
# ۱. هایپرپارامترها و تنظیمات اولیه
# ==============================================================================

# فرض می‌کنیم شما کلاس خود را در فایلی به نام a_star_env import کرده‌اید
# from your_env_file import YourEnvClass  # <--- نام فایل و کلاس خود را اینجا قرار دهید

# یک نمونه از محیط خود بسازید
# env = YourEnvClass() # <--- نمونه‌سازی کلاس شما

# *** برای اجرای این کد به تنهایی، از کلاس شبیه‌ساز زیر استفاده می‌کنیم ***
# *** شما باید این بخش را کامنت کرده و خطوط بالا را فعال کنید ***
class MockEnv:
    def __init__(self, num_resources=5, num_tasks=50):
        self.num_resources = num_resources
        self.num_tasks = num_tasks
        self.resources = np.zeros(num_resources)
    def reset(self): self.resources = np.zeros(self.num_resources); return self.resources
    def temporary_state(self, task_index): return self.resources
    def normalize_state(self, state): return state / (np.sum(state) + 1e-8)
    def step(self, task_index, action):
        old_state = self.resources.copy()
        self.resources[action] += np.random.uniform(0.5, 1.5) # افزودن بار تسک
        reward = -self.resources[action] # پاداش منفی برای تشویق به انتخاب منابع با بار کمتر
        done = (task_index == self.num_tasks - 1)
        return old_state, self.resources.copy(), reward, done
# *** پایان بخش شبیه‌ساز ***


# هایپرپارامترهای DQN
BATCH_SIZE = 128            # بزرگ‌تر از حالت قبلی برای نمونه‌گیری پایدارتر
GAMMA = 0.95                # تنزیل ملایم برای توجه به آینده ولی با تمرکز بر حال
EPS_START = 1.0             # اکتشاف کامل در ابتدا (100٪ اکشن تصادفی)
EPS_END = 0.05              # در پایان 5٪ رفتار تصادفی حفظ میشه
EPS_DECAY = 5000            # آهسته‌تر شدن روند کاهش اکتشاف برای کاهش bias
TARGET_UPDATE = 500         # به‌روزرسانی مکررتر شبکه هدف برای سازگاری بهتر
LR = 1e-5                   # نرخ یادگیری معقول برای شبکه کوچک تا متوسط
NUM_EPISODES = 500         # اپیزودهای بیشتر برای پوشش بیشتر وضعیت‌ها
NUM_TASKS = 60              # بسته به اندازه مسئله‌ات خوبه
STATE_SIZE = 3              # فرض بر اینکه 5 ویژگی مهم در state داری
ACTION_SIZE = 3


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ساختن شبکه‌ها، بهینه‌ساز و بافر
policy_net = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)
target_net = QNetwork(STATE_SIZE, ACTION_SIZE).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
memory = ReplayBuffer(10000)

steps_done = 0

# ==============================================================================
# ۲. توابع کمکی برای انتخاب اقدام و بهینه‌سازی
# ==============================================================================

def select_action(state):
    """انتخاب اقدام بر اساس سیاست اپسیلون-حریصانه"""
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # از شبکه اصلی برای انتخاب بهترین اقدام استفاده کن
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        # یک اقدام تصادفی انتخاب کن
        return torch.tensor([[random.randrange(ACTION_SIZE)]], device=device, dtype=torch.long)

def optimize_model():
    """یک بچ از تجربیات را از بافر گرفته و شبکه را یک مرحله آموزش می‌دهد"""
    if len(memory) < BATCH_SIZE:
        return None # تا زمانی که به اندازه کافی تجربه جمع نشده، آموزش نده
    
    experiences = memory.sample(BATCH_SIZE)
    batch = Experience(*zip(*experiences))

    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    
    # برای next_stateها، آن‌هایی که پایانی (None) نیستند را جدا می‌کنیم
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

    # Q(s_t, a)
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # V(s_{t+1})
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()
    
    # محاسبه مقدار Q هدف (Expected Q values)
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # محاسبه خطا (Smooth L1 Loss)
    loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))
    
    # بهینه‌سازی
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100) # جلوگیری از انفجار گرادیان
    optimizer.step()
    
    return loss.item()

# ==============================================================================
# ۳. حلقه اصلی آموزش
# ==============================================================================

episode_scores = []
episode_losses = []

def _modif_action(action):
    if action==0:
        return {"id":action, "resource":{"type":"edge"}}
    elif action==1:
        return {"id":action, "resource":{"type":"cloud"}}
    elif action==2:
        return {"id":action, "resource":{"type":"fog"}}


print("شروع آموزش DQN برای زمان‌بندی تسک‌ها...")
for i_episode in tqdm(range(NUM_EPISODES)):
    env.reset() # ریست کردن وضعیت منابع در ابتدای هر اپیزود
    total_reward = 0
    total_loss = 0
    num_optim_steps = 0
    
    # حلقه روی تمام تسک‌های ورودی
    for task_index in range(len(env.tasks)):
        # ۱. گرفتن وضعیت فعلی از محیط شما 
        env._temporary_state(task_index)
        # print(current_raw_state)
        normalized_state =env.temp_state
        state = torch.from_numpy(normalized_state.astype(np.float32)).unsqueeze(0).to(device)


        # ۲. انتخاب یک اقدام (منبع پردازشی)
        action = select_action(state)
        modif_act=_modif_action(action.item())

        # ۳. اجرای اقدام در محیط و گرفتن نتایج
        _, next_raw_state, reward, done = env.step(task_index, modif_act)
        
        # نرمال‌سازی وضعیت بعدی
        normalized_next_state =next_raw_state
        
        total_reward += reward
        reward_tensor = torch.tensor([reward], device=device)
        
        if done:
            next_state = None
        else:
            next_state = torch.from_numpy(normalized_next_state.astype(np.float32)).unsqueeze(0).to(device)


        # ۴. ذخیره تجربه در بافر
        memory.push(state, action, reward_tensor, next_state, done)
        
        # ۵. بهینه‌سازی مدل
        loss = optimize_model()
        if loss is not None:
            total_loss += loss
            num_optim_steps += 1
            
        if done:
            break
            
    # ذخیره نتایج اپیزود
    episode_scores.append(total_reward)
    avg_loss = total_loss / num_optim_steps if num_optim_steps > 0 else 0
    episode_losses.append(avg_loss)
    
    # print(f"Episode {i_episode+1}/{NUM_EPISODES} | Score: {total_reward:.2f} | Avg Loss: {avg_loss:.4f}")

    # به‌روزرسانی شبکه هدف به صورت دوره‌ای
    if i_episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

print("\nآموزش به پایان رسید!")

# ==============================================================================
# ۴. نمایش نتایج و تست نهایی
# ==============================================================================

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(episode_scores)
plt.title('Reward per Episode')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(episode_losses)
plt.title('Average Loss per Episode')
plt.xlabel('Episode')
plt.ylabel('Loss')
plt.grid(True)

plt.tight_layout()
plt.show()

# تست مدل نهایی
print("\nشروع تست مدل آموزش‌دیده...")
env.reset()
test_total_reward = 0
for task_index in range(len(env.tasks)): 
    env._temporary_state(task_index)
    norm_state = env.temp_state
    state_tensor = torch.tensor([norm_state], device=device, dtype=torch.float32)
    with torch.no_grad():
        # انتخاب بهترین اقدام بر اساس سیاست یادگرفته‌شده
        action = policy_net(state_tensor).max(1)[1].view(1, 1)
        modif_act=_modif_action(action.item())
    
    _, _, reward, done = env.step(task_index, modif_act)
    test_total_reward += reward
    if done:
        break

print(f"امتیاز نهایی در فاز تست: {test_total_reward:.2f}")

# ذخیره مدل نهایی (اختیاری)
torch.save(policy_net.state_dict(), 'dqn_scheduler_model_modified5.pth')

# rtx=Engine()


# print(rtx.max_S_element_val_for_norm)

# for i in range(rtx.tasks.number_of_task):
#     action=random.randint(0, 4)
#     print(f"number of task: {i}")
#     print(f"state before action is {rtx.get_current_status()}")
#     print(f"state with normalize is {rtx.normalize_state(rtx.state)}")
#     rtx.step(i,action)
#     print(f"state after action is {rtx.get_current_status()}")
#     print("**************************************************")
    
# # rtx.temporary_state(3)
# # rtx.step(3,2)

# # print(rtx.step(19,3))
# # print(f"\n\n state is: \n\n {rtx.state}  \n\n\n temp_state is: \n\n f{rtx.temp_state}")

# rtx.reset()

# print(f"\n\n after reset state is: \n\n {rtx.state}  \n\n\n temp_state is: \n\n f{rtx.temp_state}")



import torch
import torch.nn as nn
import numpy as np

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
            raw_state = env_instance._temporary_state(task_index)
            normalized_state =raw_state
            state_tensor = torch.tensor([normalized_state], device=device, dtype=torch.float32)

            # استفاده از مدل برای پیش‌بینی بهترین اقدام (بدون اپسیلون)
            # .max(1)[1] مقدار بیشینه و اندیس آن را برمی‌گرداند. ما به اندیس نیاز داریم.
            action = trained_model(state_tensor).max(1)[1].item()
            modif_act=_modif_action(action.item(modif_act))
            # ذخیره اقدام انتخاب‌شده
            action_sequence.append(action)
            
            # به‌روزرسانی محیط با اقدام انجام‌شده
            _, _, _, done = env_instance.step(task_index, action)
            
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
