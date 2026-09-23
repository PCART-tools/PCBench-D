def get_jit_class_def(cls, self_name):
    # Get defs for each method within the current class independently
    # TODO: proper overriding analysis when implementing class inheritance
    methods = inspect.getmembers(
        cls,
        predicate=lambda m: (inspect.ismethod(m) or inspect.isfunction(m))
        and not is_static_fn(cls, m.__name__)
        and m.__name__ in cls.__dict__
    )

    def is_classmethod(fn):
        return inspect.ismethod(fn) and getattr(fn, "__self__", None) == cls

    methods = [get_jit_def(obj,
                           name,
                           self_name=self_name,
                           is_classmethod=is_classmethod(obj)) for (name, obj) in methods]

    properties = get_class_properties(cls, self_name)

    sourcelines, file_lineno, filename = get_source_lines_and_file(cls, torch._C.ErrorReport.call_stack())
    source = ''.join(sourcelines)
    dedent_src = dedent(source)
    py_ast = ast.parse(dedent_src)
    leading_whitespace_len = len(source.split('\n', 1)[0]) - len(dedent_src.split('\n', 1)[0])
    ctx = make_source_context(source, filename, file_lineno, leading_whitespace_len, False)
    class_ast = py_ast.body[0]
    assert isinstance(class_ast, ast.ClassDef)
    assigns = get_class_assigns(ctx, class_ast)

    return build_class_def(ctx, class_ast, methods, properties, self_name, assigns)
