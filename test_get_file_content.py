from functions.get_file_content import *

test1 = get_file_content("calculator", "main.py")
if "def main():" in test1:
    print("def main():")

test2 = get_file_content("calculator", "pkg/calculator.py")
if "def _apply_operator(self, operators, values)" in test2:
    print("def _apply_operator(self, operators, values)")

print(get_file_content("calculator", "/bin/cat")) #(this should return an error string)

print(get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string)
