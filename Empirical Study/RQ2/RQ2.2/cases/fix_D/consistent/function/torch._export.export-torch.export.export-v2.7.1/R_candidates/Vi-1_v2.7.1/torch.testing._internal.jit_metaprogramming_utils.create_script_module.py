def create_script_module(self, nn_module, constructor_args, *args, **kwargs):
    def script_module(*args, **kwargs):
        _formals, tensors, actuals = get_script_args(args)

        method_args = ', '.join(['self'] + actuals)
        call_args_str = ', '.join(actuals)
        call = f"self.submodule({call_args_str})"
        script = script_method_template.format(method_args, call)

        submodule_constants = []
        if kwargs.get('is_constant'):
            submodule_constants = ['submodule']

        # Create module to use the script method
        class TheModule(torch.jit.ScriptModule):
            __constants__ = submodule_constants

            def __init__(self) -> None:
                super().__init__()
                self.submodule = nn_module(*constructor_args)

        def make_module(script):
            module = TheModule()
            # check __repr__
            str(module)
            module.define(script)
            return module

        module = make_module(script)
        if self:
            self.assertExportImportModule(module, tensors)
            module(*args)
        # skip type annotate function attributes for now, see: https://github.com/python/mypy/issues/2087
        create_script_module.last_graph = module.graph  # type: ignore[attr-defined]
        return module
    return script_module
