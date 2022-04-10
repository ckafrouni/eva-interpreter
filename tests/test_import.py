from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(import math)

	((prop math square) 10)
	""") == 100

def test_1(eval_str):
	assert eval_str("""
	(import math (square))

	(print (square 10))

	(square 10)
	""") == 100