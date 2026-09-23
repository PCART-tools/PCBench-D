def create_submodule_forward_multiple_inputs():
    # Use to test that submodules can run hooks that have multiple forward inputs
    m = ModuleForwardMultipleInputs("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[List[str], str]) -> Tuple[List[str], str]:
        assert self.name == "inner_mod_name"
        assert input[0][1] == "outer_mod_name"
        return ["pre_hook_override_name"], "pre_hook_override"

    def forward_hook(self, input: Tuple[List[str], str], output: Tuple[List[str], str]):
        assert self.name == "inner_mod_name"
        assert input[0][0] == "pre_hook_override_name"
        output2 = output[1] + "fh"
        return output[0], output2

    m.submodule.register_forward_pre_hook(pre_hook)
    m.submodule.register_forward_hook(forward_hook)

    return m
