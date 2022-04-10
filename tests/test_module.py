from tests import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
    
	(module Math
		(begin
            (def abs (value)
                (if (< value 0)
                    (- value)
                    value))
            
            (def square (x)
                (* x x))
            
            (var MAX 1000)
		)
	)
	
	(module Foo
		(begin
			(def foo () (prop Math MAX))	
		)
	)
    
	((prop Math abs) (- 1000))
	""") == 1000