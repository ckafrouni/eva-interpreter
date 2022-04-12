from . import eval_str as eval_str

def test_0(eval_str):
	assert eval_str("""
	(class Point nil
		(begin
			(def constructor (self x y)
				(begin
					(set (prop self x) x)
					(set (prop self y) y)))
			
			(def calc (self)
				(+ (prop self x) (prop self y)))
			))
	
	(var p (new Point 10 20))
	
	((prop p calc) p)
	""")
	
def test_1(eval_str):
	assert eval_str("""
	(class Point nil
		(begin
			(def constructor (self x y)
				(begin
					(set (prop self x) x)
					(set (prop self y) y)
				))	
			
			(def calc (self)
				(+ (prop self x) (prop self y)))
		))
	
	(class ThreeD Point
		(begin
			(def constructor (self x y z)
				(begin
					((prop (super ThreeD) constructor) self x y)
					(set (prop self z) z)))
			
			(def calc (self)
				(+ 
					((prop (super ThreeD) calc) self)
					(prop self z)))))
	
	(var t (new ThreeD 1 2 7))
	
	((prop t calc) t)
	""") == 10
