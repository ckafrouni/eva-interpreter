from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""(var x 10)""") == 10
	assert eval_str("""(var y (* 2 5))""") == 10
