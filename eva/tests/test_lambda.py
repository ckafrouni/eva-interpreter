from . import eval_str as eval_str


def test_0(eval_str):
	assert eval_str("""
	(def onClick (callback)
		(begin 
			(var x 10)
			(var y 20)
			(callback (+ x y))))
	
	(onClick (lambda (data) (* data 10)))
	""") == 300

# Test Immediately-invoked lambda expression - IILE
def test_1(eval_str):
	assert eval_str("""
	((lambda (x y) (+ x y)) 10 20)
	""") == 30


# Save lambda to variable
def test_2(eval_str):
	assert eval_str("""
	(var add (lambda (x y) (+ x y)))
	(add 10 20)
	""") == 30