def create_submodule_to_call_directly_with_hooks():
    # Use to test that submodules have their hooks invoked when called
    # directly
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> Tuple[str]:
        assert self.name == "inner_mod_name"
        return ("pre_hook_override_name",)

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "inner_mod_name"
        assert input == ("pre_hook_override_name",)
        return output + "_fh"

    m.submodule.register_forward_pre_hook(pre_hook)
    m.submodule.register_forward_hook(forward_hook)

    return m
