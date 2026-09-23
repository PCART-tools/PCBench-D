def save_graph_repro(
    fd,
    gm,
    args,
    compiler_name,
    *,
    stable_output=False,
    save_dir=None,
    command="run",
    accuracy=None,
    tracing_mode=None,
    check_str=None,
    stable_hash=False,
):
    if any(
        isinstance(arg, torch.fx.experimental._backward_state.BackwardState)
        for arg in args
    ):
        fd.write(
            "Repro is not generated due to existence of BackwardState in graph input"
        )
        return

    fd.write(
        generate_compiler_repro_string(
            gm,
            args,
            stable_output=stable_output,
            save_dir=save_dir,
            stable_hash=stable_hash,
        )
    )
    if accuracy is None:
        accuracy = "_accuracy" in compiler_name
    if tracing_mode is None:
        tracing_mode = "real"
        if any(
            has_free_symbols(a) for a in args if not isinstance(a, FakeScriptObject)
        ):
            tracing_mode = "symbolic"
    fd.write("if __name__ == '__main__':\n")
    fd.write("    from torch._dynamo.repro.after_aot import run_repro\n")
    fd.write(
        f"    with torch.no_grad():\n"
        f"        run_repro(mod, load_args, accuracy={accuracy!r}, command={command!r}, "
        f"save_dir={save_dir!r}, tracing_mode={tracing_mode!r}, check_str={check_str!r})\n"
        f"        # To run it separately, do \n"
        f"        # mod, args = run_repro(mod, load_args, accuracy={accuracy!r}, command='get_args', "
        f"save_dir={save_dir!r}, tracing_mode={tracing_mode!r}, check_str={check_str!r})\n"
        f"        # mod(*args)"
    )
