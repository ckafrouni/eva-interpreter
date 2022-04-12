import os
import sys

from eva.errors import UndefinedVariable
from eva.parser import parse
from eva.interpreter import Eva

from . import __version__ as V

PROMPT_FG = "\033[35;5;5m"
RESET = "\033[0m"

INTERACTIVE_MSG = (
	f"\n{PROMPT_FG}"
	f"EVA interpreter v:{V}\n"
	"----------------------\n"
	f"{RESET}"
)
END_INTERACTIVE = (
	f"\n\n{PROMPT_FG}"
	"-------- END ---------"
	f"{RESET}\n"
)

PROMPT = f"{PROMPT_FG}meva>> {RESET}"


def run_interactive(interpret: Eva):
	print(INTERACTIVE_MSG)
	txt = ""
	try:
		while True:
			try:
				parsed = parse(input(PROMPT))
				if result := interpret.eval(parsed):
					print(result)
			except UndefinedVariable as e:
				print(e)
			except Exception as e:
				print(e)
	except KeyboardInterrupt as e:
		print(END_INTERACTIVE)


def run_file(interpret: Eva, filename: str):
	try:
		with open(filename,'r') as eva_file:
			parsed = parse(f"(begin {eva_file.read()})")
			interpret.eval(parsed)
	except FileNotFoundError as e:
		print(e)


if __name__ == "__main__":
	interpret = Eva()
	if len(sys.argv) == 2:
		run_file(interpret, filename=sys.argv[1])
	else:
		run_interactive(interpret)