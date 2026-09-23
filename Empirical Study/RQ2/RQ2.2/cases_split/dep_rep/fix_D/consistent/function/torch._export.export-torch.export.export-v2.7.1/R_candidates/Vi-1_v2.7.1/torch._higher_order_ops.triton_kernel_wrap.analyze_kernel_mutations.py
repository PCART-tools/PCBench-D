@MemoizeWithCycleCheck
def analyze_kernel_mutations(
    functions: dict[str, dict[Intermediate, list[Op]]], fn_name: str, num_args: int
) -> list[bool]:
    """
    Analyzes the graph to detect all sinks from a predefined list of sinks
    by using triton's MemWrite trait list. NOTE: What if triton exposed this?
    From each sink, it traverses the CFG backwards to identify all the input
    pointers that are mutated.
    """
    # Name of mutation op to mutated parameter indices
    # List from Triton Github include/triton/Dialect/Triton/IR/TritonOps.td
    # All the OPs that have MemWrite trait.
    # What if Triton exposed this?
    MUTATION_OPS = {
        "tt.store": [0],
        "tt.atomic_cas": [0],
        "tt.atomic_rmw": [0],
        "tt.experimental_descriptor_store": [0],
    }
    # Ops that we want to bail out on
    UNKNOWN_OPS = {"tt.elementwise_inline_asm"}

    stack: list[Union[Param, Intermediate]] = []
    visited = set()
    ops = functions[fn_name]
    for op_list in ops.values():
        for op in op_list:
            # If we encounter an operation with effects that cannot be reliably analyzed
            # (e.g. `tt.elementwise_inline_asm`), we assume it does not mutate any input parameters.
            if op.name in UNKNOWN_OPS:
                if op.name == "tt.elementwise_inline_asm" and op.is_pure:
                    log.warning(
                        "TTIR mutation analysis: Skipping pure tt.elementwise_inline_asm op (is_pure=True)"
                    )
                    continue
                raise RuntimeError(
                    f"ttir analysis hit an op we do not know how to analyze: {op.name}"
                )

            if op.name == "tt.call":
                assert op.fn_call_name in functions
                mutations = analyze_kernel_mutations(
                    functions, op.fn_call_name, len(op.args)
                )
                stack.extend(arg for arg, mutated in zip(op.args, mutations) if mutated)
            else:
                stack.extend(op.args[idx] for idx in MUTATION_OPS.get(op.name, []))

    # The following is an iterative DFS algorithm
    mutated = [False] * num_args
    while stack:
        arg = stack.pop()
        if arg in visited:
            continue

        visited.add(arg)

        if isinstance(arg, Param):
            if arg.idx >= num_args:
                # This is an argument defined in the kernel, not passed in
                continue
            mutated[arg.idx] = True
        elif isinstance(arg, Intermediate) and not arg.fake():
            for op in ops[arg]:
                # Skip arguments to load
                if op.name != "tt.load":
                    stack.extend(op.args)
    return mutated
