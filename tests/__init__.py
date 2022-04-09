from eva import interpreter
from parser import parse
import pytest

@pytest.fixture
def new_eva():
	"""Returns a new Eva instance"""
	return interpreter.Eva()

@pytest.fixture
def eval_str():
	"""Returns a functions that evaluates a string"""
	return lambda exp: interpreter.Eva().eval(
		parse(f"(begin {exp})")
	)