def _get_stmt(
    benchmark: GroupedBenchmark,
    runtime: RuntimeMode,
    autograd: AutogradMode,
    language: Language,
) -> Optional[str]:
    """Specialize a GroupedBenchmark for a particular configuration."""
    is_python = (language == Language.PYTHON)

    # During GroupedBenchmark construction, py_fwd_stmt and cpp_fwd_stmt are
    # set to the eager invocation. So in the RuntimeMode.EAGER case we can
    # simply reuse them. For the RuntimeMode.JIT case, we need to generate
    # an appropriate `jit_model(...)` invocation.
    if runtime == RuntimeMode.EAGER:
        stmts = (benchmark.py_fwd_stmt, benchmark.cpp_fwd_stmt)

    else:
        assert runtime == RuntimeMode.JIT
        assert benchmark.signature_args is not None
        stmts = GroupedBenchmark._make_model_invocation(
            benchmark.signature_args, benchmark.signature_output, RuntimeMode.JIT)

    stmt = stmts[0 if is_python else 1]

    if autograd == AutogradMode.FORWARD_BACKWARD and stmt is not None:
        assert benchmark.signature_output is not None
        backward = (
            f"{benchmark.signature_output}"

            # In C++ we have to get the Tensor out of the IValue to call `.backward()`
            f"{'.toTensor()' if runtime == RuntimeMode.JIT and language == Language.CPP else ''}"
            f".backward(){';' if language == Language.CPP else ''}"
        )
        stmt = f"{stmt}\n{backward}"
    return stmt
