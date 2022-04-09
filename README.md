# eva-interpreter
💃 Eva - Building an interpreter from scratch

Multi-paradigm interpretter written in python.

## Example OO program with inheritance.
```scala
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
```

Grammar:
```ebnf
Exp 
	: NUMBER
	| STRING
	| ['begin', Exp...]
	| ['var', NAME, Exp]
	| ['set', NAME, Exp]
	| ['if', Exp, Exp, Exp]
	| ['while', Exp, Exp]
	| NAME
	| [NAME, Exp...] # Function call
	;
 ```

Reserved keywords:

|keyword|
|------|
|begin|
|var|
|set|
|if|
|while|
|for|
|switch|
|def|
|lambda|
|class|
|super|
|new|
|prop|

