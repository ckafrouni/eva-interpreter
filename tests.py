from typing import Callable, List
from eva import Eva
from eva_environment import Environment
from eva_errors import *

class CaughtException(Exception):
	pass

#-------------------------------------------------------------------# 
# Tests

def assert_equals(exp, expected, env: Environment=None):
	eva = Eva(env)
	if not (res := eva.eval(exp)) == expected:
		print(eva._global.record)
		print(f"\nBad eval: for `{exp}`:\n\texpected: {expected}\n\tresult: {res}")
		return False
	return True


def test_selfEvaluating():
	# Self-evaluating:
	return assert_equals(1, 1) and \
	assert_equals('"Hello World"', "Hello World")

def test_basicMath():
	# Math:
	return assert_equals(['+', 1, 5],6) and \
	assert_equals(['+', ['+', 3, 2], 5], 10) and \
	assert_equals(['*', ['+', 3, 2], 5], 25)

def test_variables():
	# Variables:
	return assert_equals(['var', 'x', 10], 10) and \
	assert_equals(['var', 'y', ['*', 2, 5]], 10)

def test_env_variables():
	env = Environment({
		"true": True,
		"VERSION": "0.1"
	})
	env.parent = Environment({'X': 123})
	return assert_equals('VERSION', '0.1', env) and \
	assert_equals(['var', 'isUser', 'true'], True, env) and \
	assert_equals('X', 123, env)

def test_block():
	return assert_equals(
		['begin', 
			['var', 'x', 10],
			['var', 'y', 20],
			['+', ['*', 'x', 'y'], 30]
		], 230)

def test_nestedBlock():
	return assert_equals(
		['begin', 
			['var', 'x', 10],
			['begin',
				['var', 'x', 20],
				'x'
			],
			'x'
		], 10)


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
	
if __name__ == '__main__':
	success, total = run_tests([
		test_selfEvaluating,
		test_basicMath,
		test_variables,
		test_env_variables,
		test_block,
		test_nestedBlock
	])
	print(f'\nTest done:\n\t{success}/{total}')