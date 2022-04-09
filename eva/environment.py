from typing import Any, Dict, TypeVar
from eva.errors import UndefinedVariable

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

	def assign(self, name: str, value):
		"""
		Creates a variable with the given name and value
		"""
		self._resolve(name).record[name] = value
		return value
	
	def lookup(self, name: str):
		"""
		Returns the value of a defined variable, else raises Error
		"""
		return self._resolve(name).record.get(name)
	
	def _resolve(self, name: str) -> Environment:
		if name in self.record:
			return self
		if self.parent:
			return self.parent._resolve(name)
		raise UndefinedVariable(f"Undefined variable: {name}")
		

GLOBAL_ENVIRONMENT = Environment({
	'nil': None,

	'true': True,
	'false': False,

	'__VERSION': '0.1',
	
	'+': lambda x, y: x+y,
	'-': lambda x, y: x-y,
	'*': lambda x, y: x*y,
	'**': lambda x, y: x**y,
	'/': lambda x, y: x/y,

	'<': lambda x, y: x<y,
	'>': lambda x, y: x>y,
	'>=': lambda x, y: x>=y,
	'<=': lambda x, y: x<=y,
	'=': lambda x, y: x==y,

	'println': lambda *x: print(*x),
	'print': lambda *x: print(*x, end=''),
})