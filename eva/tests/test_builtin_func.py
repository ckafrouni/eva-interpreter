from . import eval_str as eval_str

def test_math(eval_str):
	assert eval_str("(+ 1 5)") == 6
	assert eval_str("(+ 10 (* 2 5))") == 20

def test_comparison(eval_str):
	assert eval_str("(> 1 5)") == False
	assert eval_str("(< 1 5)") == True

	assert eval_str("(<= 1 5)") == True
	assert eval_str("(<= 5 5)") == True
	assert eval_str("(>= 5 5)") == True
	assert eval_str("(>= 8 5)") == True
	assert eval_str("(= 8 5)") == False
	assert eval_str("(= 8 8)") == True

def test_print(eval_str):
	eval_str('(println "Hello" "World!")')
