from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
		(begin
			(var counter 0)
			(var result 0)
			
			(while (< counter 10)
				(begin
					(set result (+ result 1))
					(set counter (+ counter 1))))

			result)
	""") == 10
