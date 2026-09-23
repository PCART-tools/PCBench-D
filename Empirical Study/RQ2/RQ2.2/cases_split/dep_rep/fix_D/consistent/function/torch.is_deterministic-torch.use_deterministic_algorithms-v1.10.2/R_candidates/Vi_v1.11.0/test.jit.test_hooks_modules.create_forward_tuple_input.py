def create_forward_tuple_input():
    # Use to test case where forward is passed a single tuple for input.
    # This is different because eager always wraps pre-hook return arguments
    # in a tuple when the returned pre-hook result isn't a tuple
    # (to allow the result to be passed to another pre-hook if needed).
    # The eager behavior doesn't wrap the single tuple input pre-hook return in a
    # tuple as it should. To get consistent behavior between single tuple inputs and
    # the rest of the possible forward inputs, pre-hooks need to
    # wrap single tuple inputs returns in another tuple. This is
    # enforced by the schema checker.
    m = ModuleForwardTupleInput("outer_mod_name", "inner_mod_name")

    def pre_hook_outermod(self, input: Tuple[Tuple[int]]) -> Tuple[Tuple[int]]:
        # 'return (11,)' doesn't work with eager, inner tuple lost
        return ((11,),)

    def pre_hook_innermod(self, input: Tuple[Tuple[int]]) -> Tuple[Tuple[int]]:
        # 'return (22,)' doesn't work with eager, inner tuple lost
        return ((22,),)

    def forward_hook_outermod(self, input: Tuple[Tuple[int]], output: int):
        return (11,)

    def forward_hook_innermod(self, input: Tuple[Tuple[int]], output: Tuple[int]):
        return 22

    m.register_forward_pre_hook(pre_hook_outermod)
    m.submodule.register_forward_pre_hook(pre_hook_innermod)
    m.register_forward_hook(forward_hook_outermod)
    m.submodule.register_forward_hook(forward_hook_innermod)

    return m
