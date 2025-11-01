import subprocess as sp

file_start = """
def f(p, q, r):
    return p == q == r
def complex_f(p, q, r):
    return """
file_end = """
def main():
    ok = True
    for p in range(2):
        for q in range(2):
            for r in range(2):
                if (p and q and r) != complex_f(p, q, r):
                    ok = False
    print(int(ok))
main()
"""


def upd_find_index(index, s):
    if index == -1:
        return len(s)
    return index


def get_new_funcs(func):
    index = 0
    while True:
        new_index = min([upd_find_index(func.find(arg, index), func) for arg in ["p", "q", "r"]])
        if new_index >= len(func):
            break
        yield func[:new_index] + "f(p,q,r)" + func[new_index + 1:]
        index = new_index + 1


def main():
    funcs = {"f(p,q,r)"}
    while True:
        new_funcs = {""}
        for func in funcs:
            for new_func in get_new_funcs(func):
                if new_func not in new_funcs:
                    new_funcs.add(new_func)
        for func in new_funcs:
            with open("test.py", "w") as file:
                file.write(file_start)
                file.write(func)
                file.write(file_end)
            result = sp.run(["python3", "test.py"], stdout=sp.PIPE, stderr=sp.PIPE, text=True, timeout=5)
            if result.stdout != "0\n":
                print(func)
                exit(0)
        funcs = new_funcs


main()
