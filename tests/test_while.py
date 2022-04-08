from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""
		(begin
			(var counter 0)
			(var result 0)
			
			(while (< counter 10)
				(begin
					(set result (+ result 1))
					(set counter (+ counter 1))))

			result)
	""")) == 10