def create_submodule_multiple_hooks_multiple_inputs():
    # Use to test that submodules can run multiple hooks with multiple
    # forward inputs
    m = ModuleForwardMultipleInputs("outer_mod_name", "inner_mod_name")

    def pre_hook1(self, input: Tuple[List[str], str]) -> Tuple[List[str], str]:
        assert self.name == "inner_mod_name"
        assert input[1] == "no_pre_hook"
        return ["pre_hook_override_name"], "pre_hook_override1"

    def pre_hook2(self, input: Tuple[List[str], str]) -> Tuple[List[str], str]:
        assert self.name == "inner_mod_name"
        assert input[1] == "pre_hook_override1"
        return ["pre_hook_override_name"], "pre_hook_override2"

    def forward_hook1(
        self, input: Tuple[List[str], str], output: Tuple[List[str], str]
    ):
        assert self.name == "inner_mod_name"
        assert input[1] == "pre_hook_override2"
        assert output[1] == "pre_hook_override2_"
        output2 = output[1] + "fh1"
        return output[0], output2, output2

    def forward_hook2(
        self, input: Tuple[List[str], str], output: Tuple[List[str], str, str]
    ):
        assert self.name == "inner_mod_name"
        assert input[1] == "pre_hook_override2"
        assert output[1] == "pre_hook_override2_fh1"
        output2 = output[1] + "_fh2"
        return output[0], output2

    m.submodule.register_forward_pre_hook(pre_hook1)
    m.submodule.register_forward_pre_hook(pre_hook2)
    m.submodule.register_forward_hook(forward_hook1)
    m.submodule.register_forward_hook(forward_hook2)

    return m
