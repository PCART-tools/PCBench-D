def generate_build_files() -> None:
    update_submodules()
    gen_compile_commands()
    run_autogen()
