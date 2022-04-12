from eva.parser import parse

def test_0():
	assert parse('(+ 1 5)') == ['+', 1, 5]
	assert parse('(+ (+ 3 2) 5)') == ['+', ['+', 3, 2], 5]
	assert parse('''(* (+ 3 2) 5)''') == ['*', ['+', 3, 2], 5]

def test_1():
	assert parse('(var x 10)') == ['var', 'x', 10]
	assert parse('(var y (* 2 5))') == ['var', 'y', ['*', 2, 5]]

def test_2():
	assert parse('''
	(begin
		(if (< x 5)
			(x)
			(+ x 1)
		))
	''') == ['begin', ['if', ['<', 'x', 5], ['x'], ['+', 'x', 1]]]