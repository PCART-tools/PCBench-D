    def _import_extension_to_sys_modules(module, memo=None):
        if memo is None:
            memo = set()
        if module in memo:
            return
        memo.add(module)
        module_name = module.__name__
        for name in dir(module):
            member = getattr(module, name)
            member_name = getattr(member, "__name__", "")
            if inspect.ismodule(member) and member_name.startswith(module_name):
                sys.modules.setdefault(member_name, member)
                # Recurse for submodules (e.g., `_C._dynamo.eval_frame`)
                _import_extension_to_sys_modules(member, memo)
