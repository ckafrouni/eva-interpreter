from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(begin
		(var x 10)
		
		(switch 
			((< x 5) 	1)
			((> x 15)	2)
			(else 		3))
	)
	""") == 3