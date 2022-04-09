from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
    (var data 10)
    (begin
        (set data 20))
    data
	""") == 20

def test_1(eval_str):
	assert eval_str("""
    (var data 10)
    (begin
        (begin
            (set data 20)))
    data
	""") == 20
