
from matplotlib.pyplot import imread
from src.gen_extent_triangles import *
pic = imread('./images/processed/ships/7test.png')
import unittest
from src.test_cases import tc

# _s.tc = tc
# extent, extent_t, lds_log, scale_vector = gen_extent(tc['1'], pic, padded=False)  # left_down_log
# tri_base, tris, tri_max_x, tri_max_y, tri_min_x, tri_min_y, mask_x, mask_y = \
# 	gen_triangles(extent_t, extent, tc['1'], pic)

i_state = 0

class Test:

	def __init__(_s):
		_s.tc = tc
		_s.i = 0

	def _run(_s, test_case_num=None):

		for i in range(1, len(_s.tc) + 1):

			if test_case_num == None:
				_s.i_data = i
			else:
				i = test_case_num
				_s.i_data = test_case_num

			index_with_most_ld_x = np.argmax([_s.tc[str(i)]['ld_ss'][0][0], _s.tc[str(i)]['ld_ss'][1][0]])
			_s.tc[str(i)]['max_ri'] = _s.tc[str(i)]['ld_ss'][index_with_most_ld_x][0] + \
			                          pic.shape[1] * _s.tc[str(i)]['scale_ss'][index_with_most_ld_x]

			_s.extent, _s.extent_t, _s.lds_log, _s.scale_vector = gen_extent(_s.tc[str(i)], pic)  # left_down_log
			_s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
				gen_triangles(_s.extent_t, _s.extent, _s.tc[str(i)], pic)

			_s.test_fours()
			_s.test_tris()

			if test_case_num:
				break

	def test_fours(_s):
		""""""
		# TEST 4'S
		for i in range(4):
			assert (abs(_s.tc[str(_s.i_data)]['t']['extent[0]'][i] - _s.extent[0][i]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['extent[-1]'][i] - _s.extent[-1][i]) < 1) #
			assert (abs(_s.tc[str(_s.i_data)]['t']['extent_t[0]'][i] - _s.extent_t[0][i]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['extent_t[-1]'][i] - _s.extent_t[-1][i]) < 1)
		print(str(_s.i_data) + " Test fours passed")

	def test_tris(_s):

		# # TEST TRIs
		for i in range(3):
			assert (abs(_s.tc[str(_s.i_data)]['t']['tri_base'][i][0] - _s.tri_base[i][0]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['tri_base'][i][1] - _s.tri_base[i][1]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['tris[0]'][i][0] - _s.tris[0][i][0]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['tris[0]'][i][1] - _s.tris[0][i][1]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['tris[-1]'][i][0] - _s.tris[-1][i][0]) < 1)
			assert (abs(_s.tc[str(_s.i_data)]['t']['tris[-1]'][i][1] - _s.tris[-1][i][1]) < 1)

		assert (abs(_s.tc[str(_s.i_data)]['t']['mask_ri'] - _s.mask_ri) < 1)
		assert (abs(_s.tc[str(_s.i_data)]['t']['mask_do'] - _s.mask_do) < 1)
		print(str(_s.i_data) + " Test tris passed")



print("number of expected tests: " + str(2))
_t = Test()
_t._run()
