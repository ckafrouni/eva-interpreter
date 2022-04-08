from eva import interpreter, environment


#-------------------------------------------------------------------# 
# Tests

def test_selfEvaluating():
	ev = interpreter.Eva()
	assert ev.eval(1) == 1
	assert ev.eval('"Hello World"') == "Hello World"

def test_basicMath():
	ev = interpreter.Eva()
	assert ev.eval(['+', 1, 5]) == 6
	assert ev.eval(['+', ['+', 3, 2], 5], 10)
	assert ev.eval(['*', ['+', 3, 2], 5]) == 25

def test_variables():
	ev = interpreter.Eva()
	assert ev.eval(['var', 'x', 10]) == 10
	assert ev.eval(['var', 'y', ['*', 2, 5]]) == 10

def test_env_variables():
	env = environment.Environment({
		"true": True,
		"VERSION": "0.1"
	})
	ev = interpreter.Eva(env)
	assert ev.eval('VERSION') == '0.1'
	assert ev.eval(['var', 'isUser', 'true']) == True
	env.parent = environment.Environment({'X': 123})
	assert ev.eval('X') == 123

def test_block():
	ev = interpreter.Eva()
	assert ev.eval(
		['begin', 
			['var', 'x', 10],
			['var', 'y', 20],
			['+', ['*', 'x', 'y'], 30]
		]) == 230

def test_nestedBlock():
	ev = interpreter.Eva()
	assert ev.eval(
		['begin', 
			['var', 'x', 10],
			['begin',
				['var', 'x', 20],
				'x'
			],
			'x'
		]) == 10

def test_nestedBlock_2():
	ev = interpreter.Eva()
	assert ev.eval(
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
	ev = interpreter.Eva()
	assert ev.eval(
		['begin', 
			['var', 'data', 10],
			['begin',
				['set', 'data', 20],
			],
			'data'
		]) == 20

def test_set_keyword_2():
	ev = interpreter.Eva()
	assert ev.eval(
		['begin', 
			['var', 'data', 10],
			['begin',
				['begin', 
					['set', 'data', 20],
				]
			],
			'data'
		]) == 20
	
def test_if():
	ev = interpreter.Eva()
	assert ev.eval(
		['begin',
			['var', 'x', 10],
			['var', 'y', 0],
			
			['if', ['>=', 'x', 10],
				['set', 'y', 20],
				['set', 'y', 30]
			],
			
			'y'
		]

	) == 20

def test_while():
	ev = interpreter.Eva()
	assert ev.eval(
		['begin',
			['var', 'counter', 0],
			['var', 'result', 0],
			
			['while', ['<', 'counter', 10],
				# TODO: implement ['++', <Exp>]
				['begin',
					['set', 'result', ['+', 'result', 1]],
					['set', 'counter', ['+', 'counter', 1]]
				],
			],
			
			'result'
		]

	) == 10