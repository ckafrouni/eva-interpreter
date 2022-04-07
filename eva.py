class Unimplemented(BaseException):
	pass

"""
Exp ::= Number
	| String
	| [+, Exp, Exp]
	;
"""
class Eva: 
	def eval(self, exp):
		# ------------------------------------
		# Self evaluating expressions

		if isNumber(exp):
			return exp
		if isString(exp):
			return exp[1:-1]
		
		# ------------------------------------
		# Math operations:

		if exp[0] == '+':
			return self.eval(exp[1]) + self.eval(exp[2])
		if exp[0] == '*':
			return self.eval(exp[1]) * self.eval(exp[2])

def isNumber(exp):
	return isinstance(exp, int) 

def isString(exp):
	return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

#-------------------------------------------------------------------# 
# Tests

def assert_equals(exp, expected):
	try:
		assert Eva().eval(exp) == expected
	except Unimplemented as e:
		print(e)

def tests():
	assert_equals(1, 1)
	assert_equals('"Hello World"', "Hello World")
	
	# Math:
	assert_equals(['+', 1, 5],			 6)
	assert_equals(['+', ['+', 3, 2], 5], 10)
	assert_equals(['*', ['+', 3, 2], 5], 25)
	
if __name__ == '__main__':
	tests()