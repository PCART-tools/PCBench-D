def create_submodule_forward_single_input():
    # Use to test that submodules can run hooks with a single argument
    # passed to forward
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> Tuple[str]:
        assert self.name == "inner_mod_name"
        assert input[0] == "a_outermod"
        return ("pre_hook_override_name",)

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "inner_mod_name"
        assert input == ("pre_hook_override_name",)
        return output

    m.submodule.register_forward_pre_hook(pre_hook)
    m.submodule.register_forward_hook(forward_hook)

    return m
