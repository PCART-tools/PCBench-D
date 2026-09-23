def create_module_multiple_hooks_single_input():
    # Use to test that modules can run multiple hooks with single input
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook1(self, input: Tuple[str]) -> Tuple[str]:
        assert self.name == "outer_mod_name"
        assert input[0] == "a"
        return ("pre_hook_override_name1",)

    def pre_hook2(self, input: Tuple[str]) -> Tuple[str]:
        assert self.name == "outer_mod_name"
        assert input[0] == "pre_hook_override_name1"
        return ("pre_hook_override_name2",)

    def forward_hook1(self, input: Tuple[str], output: str):
        assert self.name == "outer_mod_name"
        assert input == ("pre_hook_override_name2",)
        assert output == "pre_hook_override_name2_outermod_inner_mod"
        output = output + "_fh1"
        return output, output

    def forward_hook2(self, input: Tuple[str], output: Tuple[str, str]):
        assert self.name == "outer_mod_name"
        assert input == ("pre_hook_override_name2",)
        assert output[0] == "pre_hook_override_name2_outermod_inner_mod_fh1"
        output = output[0] + "_fh2"
        return output

    m.register_forward_pre_hook(pre_hook1)
    m.register_forward_pre_hook(pre_hook2)
    m.register_forward_hook(forward_hook1)
    m.register_forward_hook(forward_hook2)

    return m
