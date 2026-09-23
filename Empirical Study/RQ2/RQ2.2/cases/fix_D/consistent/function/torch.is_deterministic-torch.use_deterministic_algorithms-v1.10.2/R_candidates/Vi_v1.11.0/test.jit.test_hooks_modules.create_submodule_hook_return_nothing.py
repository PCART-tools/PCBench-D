def create_submodule_hook_return_nothing():
    # Use to test that submodules can run hooks that return nothing
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> None:
        assert self.name == "inner_mod_name"
        assert input[0] == "a_outermod"

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "inner_mod_name"
        assert input == ("a_outermod",)

    m.submodule.register_forward_pre_hook(pre_hook)
    m.submodule.register_forward_hook(forward_hook)

    return m
