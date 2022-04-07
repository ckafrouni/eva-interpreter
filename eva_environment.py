from typing import Any, Dict, TypeVar
from eva_errors import UndefinedVariable

Environment = TypeVar('Environment')

class Environment:

	def __init__(self, record: Dict[str, Any]=None, parent: Environment=None):
		if not record:
			record = {}
		self.record = record
		self.parent = parent

	def define(self, name: str, value):
		"""
		Creates a variable with the given name and value
		"""
		self.record[name] = value
		return value
	
	def lookup(self, name: str):
		"""
		Returns the value of a defined variable, else raises Error
		"""
		if (value := self.record.get(name)):
			return value
		if self.parent:
			return self.parent.lookup(name)

		raise UndefinedVariable(f"Undefined variable: {name}")