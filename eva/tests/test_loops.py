from . import eval_str as eval_str

def test_while(eval_str):
	assert eval_str("""
    (var counter 0)
    (var result 0)
    
    (while (< counter 10)
        (begin
            (set result (+ result 1))
            (set counter (+ counter 1))))

    result
	""") == 10

def test_for(eval_str):
	assert eval_str("""
	(var count 0)
	(for (var i 0) (< i 5) (set i (+ i 1))
		(set count (+ count 1))
	)
	count
	""") == 5
