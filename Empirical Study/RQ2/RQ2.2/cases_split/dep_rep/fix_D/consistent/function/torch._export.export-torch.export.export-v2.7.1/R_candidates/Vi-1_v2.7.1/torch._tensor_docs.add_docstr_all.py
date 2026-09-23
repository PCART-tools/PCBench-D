def add_docstr_all(method, docstr):
    add_docstr(getattr(torch._C.TensorBase, method), docstr)
