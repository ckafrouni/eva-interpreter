
class Transformer:

	@staticmethod
	def def_to_var_lambda(def_exp):
		[_, name, params, body] = def_exp
		return [ 'var', name, ['lambda', params, body]]