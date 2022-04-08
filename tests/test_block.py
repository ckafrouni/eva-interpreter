from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""
		(begin
			(var x 10)
			(var y 20)
			(+ (* x y) 30))
	""")) == 230

def test_1(new_eva):
	assert new_eva.eval(parse("""
		(begin
			(var x 10)
			(begin
				(var x 20)
				x)
			x)
	""")) == 10
	
	
def test_2(new_eva):
	assert new_eva.eval(parse("""
		(begin 
			(var value 10) 
			(var result (begin 
				(var x (+ value 10))
				x))
			result)
	""")) == 20