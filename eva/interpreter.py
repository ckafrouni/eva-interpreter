# Exp 
# 	: NUMBER
# 	| STRING
# 	| ['begin', Exp...]
# 	| ['var', NAME, Exp]
# 	| ['set', NAME, Exp]
# 	| ['if', NAME, Exp]
# 	| ['while', NAME, Exp]
# 	| NAME
# 	| [NAME, Exp...] # Function call
# 	;

import re
from typing import Callable, List

from eva.environment import GLOBAL_ENVIRONMENT, Environment
from eva.errors import UnimplementedExpression

class Eva: 
	"""
	Eva interpreter
	"""
	
	def __init__(self, _global: Environment=GLOBAL_ENVIRONMENT):
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
		if self.__is_number(exp):
			return exp

		if self.__is_string(exp):
			return exp[1:-1]
		
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
		# if-expression:
		if exp[0] == 'if':
			[_, condition, consequent, alternate] = exp
			if self.eval(condition, env):
				return self.eval(consequent, env)
			return self.eval(alternate, env)

		# ------------------------------------
		# while-expression:
		if exp[0] == 'while':
			[_, condition, body] = exp
			result = None
			while self.eval(condition, env):
				result = self.eval(body, env)
			return result

		# ------------------------------------
		# Variable access: foo
		if self.__is_var_name(exp):
			return env.lookup(exp)

		# ------------------------------------
		# function call:
		# (println "Hello World!")
		# (+ x 5)
		# (> foo bar)
		if isinstance(exp, List):
			fn = self.eval(exp[0])
			
			args = map(
				lambda arg: self.eval(arg, env),
				exp[1:]
			)
			
			# 1. Native functions:
			if isinstance(fn, Callable):
				return fn(*args)

			# 2. User-defined functions:
			# TODO

		raise UnimplementedExpression(f"Unimplemented expression: `{exp}`")

	def __eval_block(self, block, env):
		[_, *expression] = block
		result = None
		for exp in expression:
			result = self.eval(exp, env)
		return result


	@staticmethod
	def __is_number(exp):
		return isinstance(exp, int) 

	@staticmethod
	def __is_string(exp):
		return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

	@staticmethod
	def __is_var_name(exp):
		return isinstance(exp, str) and re.match(r"^[+\-*/<>=a-zA-Z_]+$", exp) != None