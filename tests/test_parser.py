from parser.eva_parser import parse


def test_parser():
	r = parse('''
	(begin
		(if (< x 5)
			(x)
			(+ x 1)
		))
	''')
	assert r == ['begin', ['if', ['<', 'x', 5], ['x'], ['+', 'x', 1]]]