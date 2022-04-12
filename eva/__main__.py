import os
import sys
from eva.errors import UndefinedVariable
from parser import parse
from eva.interpreter import Eva


def run_interactive(interpret: Eva):
	txt = ""
	while True:
		txt = input(">>> ")
		if txt == "q":
			break
		parsed = parse(txt)
		try:
			if result := interpret.eval(parsed):
				print(result)
		except UndefinedVariable as e:
			print(e)
		except Exception as e:
			print(e)


def run_file(interpret: Eva, filename: str):
	# print(os.getcwd())
	try:
		with open(filename,'r') as eva_file:
			parsed = parse(f"(begin {eva_file.read()})")
			interpret.eval(parsed)
			# print(parsed)
	except FileNotFoundError as e:
		print(e)


if __name__ == "__main__":
	interpret = Eva()
	if len(sys.argv) == 2:
		run_file(interpret, filename=sys.argv[1])
	else:
		run_interactive(interpret)