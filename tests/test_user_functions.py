from tests import eval_str as eval_str


def test_0(eval_str):
	assert eval_str("""
	(begin

		(def square (x)
			(* x x)
		)

		(square 5)
	)
	""") == 25

def test_1(eval_str):
	assert eval_str("""
	(begin
	
		(def calc (x y)
			(begin
				(var z 30)
				(+ (* x y) z)
			))

		(calc 10 20)
	)
	""") == 230

# Closures:

def test_2(eval_str):
	assert eval_str("""
	(begin

		(var z 30)
	
		(def calc (x y)
			(begin
				(+ (* x y) z)
			))

		(calc 10 20)
	)
	""") == 230

def test_3(eval_str):
	assert eval_str("""
	(begin

		(var value 100)
	
		(def calc (x y)
			(begin
				(var z (+ x y))
				
				(def inner (foo)
					(+ (+ foo z) value))
				
				inner
			))

		(var fn (calc 10 20))
		
		(fn 30)
	)
	""") == 160


# Test if (set foo 5) works for a variable outside of the function declaration
# As of now, a function can access a variable, but can also set it..
# I'm not sure if this is a desired behavior

def test_4(eval_str):
	assert eval_str("""
	(begin

		(var value 100)
	
		(def calc (x y)
			(begin
				(set value (+ x y))
			))
		
		(calc 10 20)
		
		value

	)
	""") == 30