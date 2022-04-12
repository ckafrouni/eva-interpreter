from . import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(var x 10)
	(var y 10)
	(if (>= x 10)
		(set y 20)
		(set y 30))
	""") == 20