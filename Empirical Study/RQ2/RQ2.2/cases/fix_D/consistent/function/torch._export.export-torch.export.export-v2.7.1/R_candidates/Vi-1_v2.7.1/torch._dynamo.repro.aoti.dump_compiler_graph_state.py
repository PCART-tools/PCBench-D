def dump_compiler_graph_state(
    gm,
    args,
    compiler_name,
    *,
    config_patches=None,
    accuracy=None,
    strict=False,
):
    subdir = os.path.join(minifier_dir(), "checkpoints")
    if not os.path.exists(subdir):
        os.makedirs(subdir, exist_ok=True)
    file_name = os.path.join(subdir, f"{len(gm.graph.nodes)}.py")
    log.warning(
        "Writing checkpoint with %s nodes to %s", len(gm.graph.nodes), file_name
    )
    with open(file_name, "w") as fd:
        save_graph_repro_ep(
            fd,
            compiler_name,
            gm=gm,
            args=tuple(args),
            config_patches=config_patches,
            save_dir=subdir,
            accuracy=accuracy,
            module_in_comment=True,
            strict=strict,
        )
    curdir = os.getcwd()
    repro_path = os.path.join(curdir, "repro.py")
    try:
        shutil.copyfile(file_name, repro_path)
        log.warning("Copying repro file for convenience to %s", repro_path)
        if use_buck:
            BuckTargetWriter(file_name).write()
    except OSError:
        log.warning("No write permissions for %s", repro_path)
