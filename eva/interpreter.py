# Exp 
# 	: NUMBER
# 	| STRING
# 	| ['begin', Exp...]
# 	| ['var', NAME, Exp]
# 	| ['set', NAME, Exp]
# 	| ['if', Exp, Exp, Exp]
# 	| ['while', Exp, Exp]
# 	| NAME
# 	| [NAME, Exp...] # Function call
# 	;

import os
from posixpath import dirname
import re
from typing import Callable, List

from eva.environment import GLOBAL_ENVIRONMENT, Environment
from eva.errors import UnimplementedExpression
from eva.syntactic_sugar.transformer import Transformer
from parser import parse

class Eva: 
	"""
	Eva interpreter
	"""
	
	def __init__(self, _global: Environment=GLOBAL_ENVIRONMENT):
		"""
		Initialises an Eva instance with the global environment
		"""
		self._global = _global
		self.__transformer = Transformer


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
			[_, ref, value] = exp
			
			# Assign to a property
			if ref[0] == 'prop':
				[_, instance, prop_name] = ref
				instance_env = self.eval(instance, env)
				return instance_env.define(
					prop_name,
					self.eval(value, env)
				)

			# Simple assignment
			return env.assign(ref, self.eval(value, env))
		
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
		# Switch-expression: (switch (cond1 block1) (cond2 block2) ...)
		#
		# Syntactic suggar for if-expressions
		if exp[0] == 'switch':
			if_exp = self.__transformer.switch_to_if(exp)
			return self.eval(if_exp, env)
			
		# ------------------------------------
		# for-expression: (for init cond modifier body)
		#
		# Syntactic suggar for while-expressions
		if exp[0] == 'for':
			while_exp = self.__transformer.for_to_while(exp)
			return self.eval(while_exp, env)

		# ------------------------------------
		# Increment: 
		# (++ foo) | (+= foo inc)
		# SS
		if exp[0] == '++':
			print("In ")
			return self.eval(self.__transformer.inc_to_set(exp), env)

		if exp[0] == '+=':
			return self.eval(self.__transformer.inc_to_set(exp), env)

		# ------------------------------------
		# Increment: 
		# (-- foo) | (-- foo dec)
		# SS
		if exp[0] == '--':
			return self.eval(self.__transformer.dec_to_set(exp), env)
		if exp[0] == '-=':
			return self.eval(self.__transformer.dec_to_set(exp), env)

		# ------------------------------------
		# Mul-assign: 
		# (*= foo dec)
		# SS
		if exp[0] == '*=':
			return self.eval(self.__transformer.mul_to_set(exp), env)

		# ------------------------------------
		# Pow-assign: 
		# (**= foo dec)
		# SS
		if exp[0] == '**=':
			return self.eval(self.__transformer.pow_to_set(exp), env)

		# ------------------------------------
		# function declaration: (def square (x) (* x x))
		#
		# Syntactic suggar for: (var square (lambda (x) (* x x)))
		if exp[0] == 'def':
			# JIT-transpile to a variable declaration
			var_exp = self.__transformer.def_to_var_lambda(exp)

			return self.eval(var_exp, env)

		# ------------------------------------
		# Lambda functions: (lambda (x) (* x x))
		if exp[0] == 'lambda':
			[_, params, body] = exp

			return {
				'params': params,
				'body': body,
				'env': env # Closure !!
			}

		# ------------------------------------
		# Class declaration: (class <Name> <Parent> <Body>)
		if exp[0] == 'class':
			[_, name, parent, body] = exp
			# a class is an environment -- storage of methods
			# and properties

			parent_env = self.eval(parent, env) or env
			class_env = Environment({}, parent_env)
			
			# Body is evaluated in the class environment
			self.__eval_body(body, class_env)
			
			# class is accessible by name
			return env.define(name, class_env)

		# ------------------------------------
		# Super expresson: (super <ClassName>)
		if exp[0] == 'super':
			[_, class_name] = exp
			return self.eval(class_name, env).parent

		# ------------------------------------
		# Class instanciation: (new <Class> <Arguments> ...)
		if exp[0] == 'new':
			[_, class_name, *args] = exp
			class_env = self.eval(class_name, env)

			# create an instance of the class
			instance = Environment({}, class_env)
			
			evaluated_args = list(map(
				lambda arg: self.eval(arg, env),
				args
			))

			self.__call_user_defined_function(
				class_env.lookup('constructor'),
				[instance, *evaluated_args]
			)
			
			return instance
			
		# ------------------------------------
		# Property access: (prop <instance> <name>)
		if exp[0] == 'prop':
			[_, instance, name] = exp
			
			instance_env = self.eval(instance, env)
			
			return instance_env.lookup(name)

		# ------------------------------------
		# Module declaration: (module <Name> <body>)
		if exp[0] == 'module':
			[_, name, body] = exp
			
			module_env = Environment({}, env)
			
			self.__eval_body(body, module_env)
			
			return env.define(name, module_env)

		# ------------------------------------
		# Module import: (import <Name>) | (import <Name> (<props>))
		if exp[0] == 'import':
			[_, name, *vars] = exp
			# TODO: implement caching if importing same file
			# TODO: handle user generated code in other directories
			
			module_src = ""
			if os.path.exists(f"{os.getcwd()}/eva/std/{name}.eva"):
				with open(f"{os.getcwd()}/eva/std/{name}.eva", 'r') as module_file:
					module_src = module_file.read()
			else:
				with open(f"{os.getcwd()}/{name}.eva", "r") as module_file:
					module_src = module_file.read()

			body = parse(f'(begin {module_src})')
			
			module_exp = ['module', name, body]
			
			if not vars:
				return self.eval(module_exp, self._global)
			
			res = None
			for v in vars[0]:
				res = self.eval(['var', v, ['prop', module_exp, v]], self._global)
			
			return res

		# ------------------------------------
		# function call:
		# (println "Hello World!")
		# (+ x 5)
		# (> foo bar)
		# (square 5)
		if isinstance(exp, List):
			fn = self.eval(exp[0], env)
			
			args = list(map(
				lambda arg: self.eval(arg, env),
				exp[1:]
			))
			
			# 1. Native functions:
			if isinstance(fn, Callable):
				return fn(*args)

			# 2. User-defined functions:
			return self.__call_user_defined_function(fn, args)

		raise UnimplementedExpression(f"Unimplemented expression: `{exp}`")
	
	def __eval_body(self, body, env: Environment):
		if body[0] == 'begin':
			return self.__eval_block(body, env)
		return self.eval(body, env)

	def __eval_block(self, block, env: Environment):
		[_, *expression] = block
		result = None
		for exp in expression:
			result = self.eval(exp, env)
		return result
	
	def __call_user_defined_function(self, fn, args):
		# fn['params'] = ['x', 'y']
		# args = [5, 9]
		activation_record = {}
		for index, value in enumerate(fn['params']):
			activation_record[value] = args[index]
		
		# the activation_environment's parent is the functions's env
		# If we had set it to the current environment, we would have
		# a dynamic scope
		activation_env = Environment(
			activation_record,
			fn['env'] # static scope!
		)
		return self.__eval_body(fn['body'], activation_env)

	#----------------------------------------------------------------
	#----------------------------------------------------------------
	@staticmethod
	def __is_number(exp):
		return isinstance(exp, int) 

	@staticmethod
	def __is_string(exp):
		return isinstance(exp, str) and exp[0] == '"' and exp[-1] == '"'

	@staticmethod
	def __is_var_name(exp):
		return isinstance(exp, str) and re.match(r"^[+\-*/<>=a-zA-Z_]+$", exp) != None