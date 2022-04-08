from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""
		(begin
			(var data 10)
			(begin
				(set data 20))
			data)
	""")) == 20

def test_1(new_eva):
	assert new_eva.eval(parse("""
		(begin
			(var data 10)
			(begin
				(begin
					(set data 20)))
			data)
	""")) == 20