def compile_timeit_template(*, stmt: str, setup: str, global_setup: str) -> TimeitModuleType:
    template_path: str = os.path.join(SOURCE_ROOT, "timeit_template.cpp")
    with open(template_path) as f:
        src: str = f.read()

    module = _compile_template(stmt=stmt, setup=setup, global_setup=global_setup, src=src, is_standalone=False)
    assert isinstance(module, TimeitModuleType)
    return module
