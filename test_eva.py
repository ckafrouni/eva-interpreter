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

def test_nestedBlock_2():
	eva = Eva()
	assert eva.eval(
		['begin', 
			['var', 'value', 10],
			['var', 'result', 
				['begin',
					['var', 'x', ['+', 'value', 10]],
					'x'
				]],
			'result'
		]) == 20

def test_set_keyword():
	eva = Eva()
	assert eva.eval(
		['begin', 
			['var', 'data', 10],
			['begin',
				['set', 'data', 20],
			],
			'data'
		]) == 20

def test_set_keyword_2():
	eva = Eva()
	assert eva.eval(
		['begin', 
			['var', 'data', 10],
			['begin',
				['begin', 
					['set', 'data', 20],
				]
			],
			'data'
		]) == 20