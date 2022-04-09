from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""(+ 2 4)""") == 6
	# assert eval_str("""(- 2 4)""") == -2
	assert eval_str("""(* 2 4)""") == 8
	# assert eval_str("""(/ 4 2)""") == 2
	
def test_1(eval_str):
	assert eval_str("""(+ 2 (+ 2 2))""") == 6
	assert eval_str("""(+ (+ 1 1) (+ 2 2))""") == 6
	assert eval_str("""(+ (* 2 (+ 3 2)) (+ 2 2))""") == 14

def test_2(eval_str):
	assert eval_str("""
	(begin
		(var x 0)
		(++ x)
		(++ x)
		(++ x)
		(-- x)
	)
	""") == 2

def test_3(eval_str):
	assert eval_str("""
	(begin
		(var x 0)
		(+= x 15)
		(*= x 2)
		(-= x 5)
		x
	)
	""") == 25

def test_4(eval_str):
	assert eval_str("""
	(begin
		(var x 2)
		(**= x 3)
		x
	)
	""") == 8