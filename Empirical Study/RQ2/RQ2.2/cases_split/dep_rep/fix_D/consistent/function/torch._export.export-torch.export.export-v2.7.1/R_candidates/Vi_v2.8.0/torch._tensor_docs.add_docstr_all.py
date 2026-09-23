def add_docstr_all(method: str, docstr: str) -> None:
    add_docstr(getattr(torch._C.TensorBase, method), docstr)
