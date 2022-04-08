from eva import interpreter, environment
import pytest

@pytest.fixture
def new_eva():
	"""Returns a new Eva instance"""
	return interpreter.Eva()