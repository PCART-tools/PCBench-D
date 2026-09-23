def create_module_no_forward_input():
    # Use to test module level hooks with no forward input
    m = ModuleNoForwardInputs("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[()]) -> None:
        assert self.name == "outer_mod_name"

    def forward_hook(self, input: Tuple[()], output: None):
        assert self.name == "outer_mod_name"

    m.register_forward_pre_hook(pre_hook)
    m.register_forward_hook(forward_hook)

    return m
