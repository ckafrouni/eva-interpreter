from . import eval_str as eval_str


def test_0(eval_str):
	assert eval_str("""
    (def square (x)
        (* x x))

    (square 5)
	""") == 25

def test_1(eval_str):
	assert eval_str("""
    (def calc (x y)
        (begin
            (var z 30)
            (+ (* x y) z)))

    (calc 10 20)
	""") == 230

# Closures:

def test_2(eval_str):
	assert eval_str("""
    (var z 30)

    (def calc (x y)
        (begin
            (+ (* x y) z)))

    (calc 10 20)
	""") == 230

def test_3(eval_str):
	assert eval_str("""
    (var value 100)

    (def calc (x y)
        (begin
            (var z (+ x y))
            
            (def inner (foo)
                (+ (+ foo z) value))
            
            inner))

    (var fn (calc 10 20))
    
    (fn 30)
	""") == 160

# Recursive functions:
def test_4(eval_str):
	assert eval_str("""
    (def factorial (x)
        (if (= x 1)
            1
            (* x (factorial (- x 1)))))
    
    (factorial 5)
	""") == 120

# Tail-Recursive functions (with accumulator):
def test_5(eval_str):
	assert eval_str("""
    (def factorial (x acc)
        (if (= x 1)
            acc
            (factorial (- x 1) (* x acc))))
    
    (factorial 5 1)
	""") == 120

def test_6(eval_str):
	assert eval_str("""
    (def factorial (x)
        (begin
            (def inner (x acc)
                (if (= x 1)
                    acc
                    (inner (- x 1) (* x acc))))

            (inner x 1)))
    
    (factorial 5)
	""") == 120


# Test if (set foo 5) works for a variable outside of the function declaration
# As of now, a function can access a variable, but can also set it..
# I'm not sure if this is a desired behavior

def test_7(eval_str):
	assert eval_str("""
    (var value 100)

    (def calc (x y)
        (begin
            (set value (+ x y))))
    
    (calc 10 20)
    
    value
	""") == 30