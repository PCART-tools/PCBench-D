def coverage_init(reg: Any, options: Any) -> None:
    reg.add_dynamic_context(JitPlugin())
