def elastic_launch_wrapper(
    test_dir: str,
    rdzv_endpoint: str,
    min_nodes: int,
    max_nodes: int,
    nproc_per_node: int,
    run_id: str,
):
    """A wrapper function for class `elastic_launch.` in order to make multiprocess returns correct exit code."""
    elastic_launch(
        get_test_launch_config(
            rdzv_endpoint, min_nodes, max_nodes, nproc_per_node, run_id
        ),
        sys.executable,
    )("-u", path("bin/test_script.py"), f"--touch_file_dir={test_dir}")
