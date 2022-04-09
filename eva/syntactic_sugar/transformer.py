
from typing import List


class Transformer:

	@staticmethod
	def def_to_var_lambda(def_exp):
		[_, name, params, body] = def_exp
		return [ 'var', name, ['lambda', params, body]]

	@staticmethod
	def switch_to_if(switch_exp):
		# (switch (cond1 block1) (cond2 block2) (else block3))
		# (if cond1 block1 (if cond2 block2 block3))
		[_, *cases] = switch_exp

		if_exp = ['if', None, None, None]
		
		current = if_exp

		for i, _ in enumerate(cases):
			[curr_cond, curr_block] = cases[i]
			current[1] = curr_cond
			current[2] = curr_block 
			[nxt_cond, nxt_block] = cases[i+1]
			if nxt_cond == 'else':
				current[3] = nxt_block
				break
			else:
				current[3] = ['if', None, None, None]

			current = current[3]
		
		return if_exp

	@staticmethod
	def for_to_while(for_exp):
		# for-expression: (for init cond modifier body)
		[_, init, cond, modifier, body] = for_exp
		while_exp = ['begin', init, ['while', cond , ['begin', body, modifier]]]
		return while_exp

	@staticmethod
	def inc_to_set(inc_exp):
		[_, x, *y] = inc_exp
		if y:
			return ['set', x, ['+', x, *y]]
		return ['set', x, ['+', x, 1]]

	@staticmethod
	def dec_to_set(dec_exp):
		[_, x, *y] = dec_exp
		if y:
			return ['set', x, ['-', x, *y]]
		return ['set', x, ['-', x, 1]]

	@staticmethod
	def mul_to_set(mul_exp):
		[_, var, mul] = mul_exp
		return ['set', var, ['*', var, mul]]

	@staticmethod
	def pow_to_set(pow_exp):
		[_, var, pow] = pow_exp
		return ['set', var, ['**', var, pow]]