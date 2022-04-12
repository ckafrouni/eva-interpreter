from . import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
		(begin
			(var x 10)
			(var y 20)
			(+ (* x y) 30))
	""") == 230

def test_1(eval_str):
	assert eval_str("""
		(begin
			(var x 10)
			(begin
				(var x 20)
				x)
			x)
	""") == 10
	
	
def test_2(eval_str):
	assert eval_str("""
		(begin 
			(var value 10) 
			(var result (begin 
				(var x (+ value 10))
				x))
			result)
	""") == 20