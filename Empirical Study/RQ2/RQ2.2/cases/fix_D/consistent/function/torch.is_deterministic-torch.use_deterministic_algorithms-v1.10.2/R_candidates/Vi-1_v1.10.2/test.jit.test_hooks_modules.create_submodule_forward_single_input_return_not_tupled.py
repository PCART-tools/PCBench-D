def create_submodule_forward_single_input_return_not_tupled():
    # Use to check that submodules can return modified inputs
    # that aren't wrapped in a tuple (to match eager behavior)
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> str:
        assert self.name == "inner_mod_name"
        assert input[0] == "a_outermod"
        # return is wrapped in tuple in other test cases
        return "pre_hook_override_name"

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "inner_mod_name"
        assert input == ("pre_hook_override_name",)
        output = output + "_fh"
        return output

    m.submodule.register_forward_pre_hook(pre_hook)
    m.submodule.register_forward_hook(forward_hook)

    return m
