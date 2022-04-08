from tests import new_eva as new_eva
from parser import parse

def test_0(new_eva):
	assert new_eva.eval(parse("""(+ 2 4)""")) == 6
	# assert new_eva.eval(parse("""(- 2 4)""")) == -2
	assert new_eva.eval(parse("""(* 2 4)""")) == 8
	# assert new_eva.eval(parse("""(/ 4 2)""")) == 2
	
def test_1(new_eva):
	assert new_eva.eval(parse("""(+ 2 (+ 2 2))""")) == 6
	assert new_eva.eval(parse("""(+ (+ 1 1) (+ 2 2))""")) == 6
	assert new_eva.eval(parse("""(+ (* 2 (+ 3 2)) (+ 2 2))""")) == 14