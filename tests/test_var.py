from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""(var x 10)""")) == 10
	assert new_eva.eval(parse("""(var y (* 2 5))""")) == 10