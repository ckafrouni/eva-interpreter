from eva_errors import UndefinedVariable

class Environment:

	def __init__(self, record={}) -> None:
		self.record = record

	def define(self, name, value):
		"""
		Creates a variable with the given name and value
		"""
		self.record[name] = value
		return value
	
	def lookup(self, name):
		"""
		Returns the value of a defined variable, else raises Error
		"""
		if (value := self.record.get(name)):
			return value
		raise UndefinedVariable(f"Undefined variable: {name}")