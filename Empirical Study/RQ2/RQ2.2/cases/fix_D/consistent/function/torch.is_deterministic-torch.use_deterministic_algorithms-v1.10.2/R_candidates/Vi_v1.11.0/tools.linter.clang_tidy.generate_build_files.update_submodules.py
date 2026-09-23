def update_submodules() -> None:
    run_cmd(["git", "submodule", "update", "--init", "--recursive"])
