from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(import math (square))

	(square 4)
	""") == 16