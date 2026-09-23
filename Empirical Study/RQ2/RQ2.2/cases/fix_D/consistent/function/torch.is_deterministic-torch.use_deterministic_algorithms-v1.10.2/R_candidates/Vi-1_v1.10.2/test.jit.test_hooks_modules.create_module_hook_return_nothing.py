def create_module_hook_return_nothing():
    # Use to test module level hooks that return nothing
    m = ModuleForwardSingleInput("outer_mod_name", "inner_mod_name")

    def pre_hook(self, input: Tuple[str]) -> None:
        assert self.name == "outer_mod_name"
        assert input[0] == "a"

    def forward_hook(self, input: Tuple[str], output: str):
        assert self.name == "outer_mod_name"
        assert input == ("a",)

    m.register_forward_pre_hook(pre_hook)
    m.register_forward_hook(forward_hook)

    return m
