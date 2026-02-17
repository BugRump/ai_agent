from functions.run_python_file import run_python_file

test1 = run_python_file("calculator", "main.py") #(should print the calculator's usage instructions)
print(test1)
test2 = run_python_file("calculator", "main.py", ["3 + 5"]) #(should run the calculator... which gives a kinda nasty rendered result)
print(test2)
test3 = run_python_file("calculator", "tests.py") #(should run the calculator's tests successfully)
print(test3)
test4 = run_python_file("calculator", "../main.py") #(this should return an error)
print(test4)
test5 = run_python_file("calculator", "nonexistent.py") #(this should return an error)
print(test5)
test6 = run_python_file("calculator", "lorem.txt") #(this should return an error)
print(test6)