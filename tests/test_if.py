from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""
	(begin
		(var x 10)
		(var y 10)
		(if (>= x 10)
			(set y 20)
			(set y 30)))
	""")) == 20