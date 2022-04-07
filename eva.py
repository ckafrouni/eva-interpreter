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
	
	def __init__(self, _global: Environment=None):
		"""
		Initialises an Eva instance with the global environment
		"""
		if not _global:
			_global = Environment()
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
			return self.eval(exp[1], env) + self.eval(exp[2], env)
		if exp[0] == '*':
			return self.eval(exp[1], env) * self.eval(exp[2], env)

		# ------------------------------------
		# Block: (sequence of expressions)
		if exp[0] == 'begin':
			block_env = Environment(parent=env)
			return self.__eval_block(exp, block_env)

		# ------------------------------------
		# Variable declaration: (var foo 10)
		if exp[0] == 'var':
			[_, name, value] = exp
			return env.define(name, self.eval(value, env))

		# ------------------------------------
		# Variable update: (set foo 10)
		if exp[0] == 'set':
			[_, name, value] = exp
			return env.assign(name, self.eval(value, env))
		
		# ------------------------------------
		# Variable access:
		if isVariableName(exp):
			return env.lookup(exp)

		raise UnimplementedExpression(f"Unimplemented expression: `{exp}`")

	def __eval_block(self, block, env):
		[_, *expression] = block
		result = None
		for exp in expression:
			result = self.eval(exp, env)
		return result


def isNumber(exp):
	return isinstance(exp, int) 

def isString(exp):
	return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

def isVariableName(exp):
	return isinstance(exp, str) and re.match(r"^[a-zA-Z]+$", exp) != None