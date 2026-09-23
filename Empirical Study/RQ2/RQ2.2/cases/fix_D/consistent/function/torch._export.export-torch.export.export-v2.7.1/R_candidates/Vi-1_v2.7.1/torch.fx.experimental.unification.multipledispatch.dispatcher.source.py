def source(func):
    s = f"File: {inspect.getsourcefile(func)}\n\n"
    s = s + inspect.getsource(func)
    return s
