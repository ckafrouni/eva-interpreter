
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