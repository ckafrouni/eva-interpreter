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
