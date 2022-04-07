# Exp ::= Number
# 	| String
# 	| [+, Exp, Exp] | [*, Exp, Exp]
# 	| ['var', Identifier, Exp]
# 	;

import re

from eva_environment import Environment
from eva_errors import UndefinedVariable, UnimplementedExpression

class Eva: 
	"""
	Eva interpreter
	"""
	
	def __init__(self, _global: Environment = Environment()):
		"""
		Initialises an Eva instance with the global environment
		"""
		self._global = _global

	def eval(self, exp, env: Environment=None):
		"""
		Evaluates an expression in the current environment.
		"""
		if not env:
			env = self._global

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

		# ------------------------------------
		# Variable declaration:
		if exp[0] == 'var':
			[_, name, value] = exp
			return env.define(name, self.eval(value))
		
		# ------------------------------------
		# Variable declaration:
		if isVariableName(exp):
			return env.lookup(exp)

		raise UnimplementedExpression(f"Unimplemented expression: `{exp}`")


def isNumber(exp):
	return isinstance(exp, int) 

def isString(exp):
	return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

def isVariableName(exp):
	return isinstance(exp, str) and re.match(r"^[a-zA-Z]+$", exp) != None



#-------------------------------------------------------------------# 
# Tests

def assert_equals(exp, expected, env=Environment()):
	try:
		if not (res:=Eva(env).eval(exp)) == expected:
			print(f"Evaluation error for `{exp}`:\n\texpected: {expected}\n\tresult: {res}")
		return True
	except UnimplementedExpression as e:
		print(e)
	except UndefinedVariable as e:
		print(e)

def tests(env=None):
	# Self-evaluating:
	assert_equals(1, 1)
	assert_equals('"Hello World"', "Hello World")
	
	# Math:
	assert_equals(['+', 1, 5],			 6)
	assert_equals(['+', ['+', 3, 2], 5], 10)
	assert_equals(['*', ['+', 3, 2], 5], 25)
	
	# Variables:
	assert_equals(['var', 'x', 10], 10)
	assert_equals('x', 10)
	assert_equals(['var', 'y', ['*', 2, 5]], 10)
	assert_equals('y', 10)

	assert_equals('VERSION', '0.1', env)
	
	assert_equals(['var', 'isUser', 'true'], True, env)
	
if __name__ == '__main__':
	env = Environment({
		"nil": None,
		"true": True,
		"false": False,
		"VERSION": "0.1"
	})
	tests(env)