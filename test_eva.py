from typing import Callable, List
from eva import Eva
from eva_environment import Environment
from eva_errors import *


class CaughtException(Exception):
	pass

#-------------------------------------------------------------------# 
# Tests

def test_selfEvaluating():
	eva = Eva()
	assert eva.eval(1) == 1
	assert eva.eval('"Hello World"') == "Hello World"

def test_basicMath():
	eva = Eva()
	assert eva.eval(['+', 1, 5]) == 6
	assert eva.eval(['+', ['+', 3, 2], 5], 10)
	assert eva.eval(['*', ['+', 3, 2], 5]) == 25

def test_variables():
	eva = Eva()
	assert eva.eval(['var', 'x', 10]) == 10
	assert eva.eval(['var', 'y', ['*', 2, 5]]) == 10

def test_env_variables():
	env = Environment({
		"true": True,
		"VERSION": "0.1"
	})
	eva = Eva(env)
	assert eva.eval('VERSION') == '0.1'
	assert eva.eval(['var', 'isUser', 'true']) == True
	env.parent = Environment({'X': 123})
	assert eva.eval('X') == 123

def test_block():
	eva = Eva()
	assert eva.eval(
		['begin', 
			['var', 'x', 10],
			['var', 'y', 20],
			['+', ['*', 'x', 'y'], 30]
		]) == 230

def test_nestedBlock():
	eva = Eva()
	assert eva.eval(
		['begin', 
			['var', 'x', 10],
			['begin',
				['var', 'x', 20],
				'x'
			],
			'x'
		]) == 10


def run_tests(tests: List[Callable]):	
	success = 0
	for t in tests:
		try:
			if t():
				success += 1
			else:
				print(f'Unsuccessfull test: {t.__name__}')
		except CaughtException as e:
			print(e)
	return success, len(tests)