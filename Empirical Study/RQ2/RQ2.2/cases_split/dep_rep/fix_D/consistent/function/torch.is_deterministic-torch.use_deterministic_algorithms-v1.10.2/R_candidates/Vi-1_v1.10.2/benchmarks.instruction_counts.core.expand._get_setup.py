def _get_setup(
    benchmark: GroupedBenchmark,
    runtime: RuntimeMode,
    language: Language,
    stmt: str,
    model_path: Optional[str]
) -> str:
    """Specialize a GroupedBenchmark for a particular configuration.

    Setup requires two extra pieces of information:
      1) The benchmark stmt. This is needed to warm up the model and avoid
         measuring lazy initialization.
      2) The model path so we can load it during the benchmark.

    These are only used when `runtime == RuntimeMode.JIT`.
    """

    # By the time we get here, details about how to set up a model have already
    # been determined by GroupedBenchmark. (Or set to None if appropriate.) We
    # simply need to collect and package the code blocks.
    if language == Language.PYTHON:
        setup = benchmark.setup.py_setup
        model_setup = benchmark.py_model_setup
    else:
        assert language == Language.CPP
        setup = benchmark.setup.cpp_setup
        model_setup = benchmark.cpp_model_setup

    if runtime == RuntimeMode.EAGER:
        return "\n".join([setup, model_setup or ""])

    assert runtime == RuntimeMode.JIT
    assert model_path is not None

    # We template `"{model_path}"`, so quotes would break model loading. The
    # model path is generated within the benchmark, so this is just an
    # abundance of caution rather than something that is expected in practice.
    assert '"' not in model_path

    # `stmt` may contain newlines, so we can't use f-strings. Instead we need
    # to generate templates so that dedent works properly.
    if language == Language.PYTHON:
        setup_template: str = textwrap.dedent(f"""
            jit_model = torch.jit.load("{model_path}")

            # Warmup `jit_model`
            for _ in range(3):
            {{stmt}}
        """)

    else:
        assert language == Language.CPP
        setup_template = textwrap.dedent(f"""
            const std::string fpath = "{model_path}";
            auto jit_model = torch::jit::load(fpath);

            // Warmup `jit_model`
            for (int i = 0; i < 3; i++) {{{{
            {{stmt}}
            }}}}
        """)

    model_load = setup_template.format(stmt=textwrap.indent(stmt, ' ' * 4))
    return "\n".join([setup, model_load])
