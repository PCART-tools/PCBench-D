def create_module_forward_single_input():
    # Use to test module level hooks for forward with single input
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> Tuple[str]:
        assert self.name == "outer_mod_name"
        assert input[0] == "a"
        return ("pre_hook_override_name",)

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "outer_mod_name"
        assert input == ("pre_hook_override_name",)
        output = output + "_fh"
        return output

    m.register_forward_pre_hook(pre_hook)
    m.register_forward_hook(forward_hook)

    return m
