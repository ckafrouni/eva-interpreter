from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(import math)

	(var square (prop math square))
	
	(square 10)
	""") == 100