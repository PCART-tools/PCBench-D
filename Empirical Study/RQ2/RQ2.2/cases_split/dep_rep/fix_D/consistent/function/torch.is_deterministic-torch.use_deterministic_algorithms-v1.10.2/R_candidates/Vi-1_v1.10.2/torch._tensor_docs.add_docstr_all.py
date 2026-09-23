def add_docstr_all(method, docstr):
    add_docstr(getattr(torch._C._TensorBase, method), docstr)
