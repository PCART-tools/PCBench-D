def isolate_fails(
    fx_g,
    args,
    compiler_name: str,
    env=None,
    save_dir=None,
    accuracy=None,
    tracing_mode=None,
    check_str=None,
):
    if env is None:
        env = {}
    subdir = os.path.join(os.getcwd(), "isolate")
    if not os.path.exists(subdir):
        os.makedirs(subdir, exist_ok=True)
    file_name = os.path.join(subdir, f"{str(uuid.uuid4())[:5]}.py")
    with open(file_name, "w") as fd:
        save_graph_repro(
            fd,
            fx_g,
            args,
            compiler_name,
            save_dir=save_dir,
            command="minifier-query",
            accuracy=accuracy,
            tracing_mode=tracing_mode,
            check_str=check_str,
        )
    # with open(file_name, "r") as fd:
    #     print(fd.read())
    new_env = os.environ.copy()
    new_env = {**new_env, **env}
    stdout, stderr = TemporaryFile(), TemporaryFile()

    if use_buck:
        cmd = BuckTargetWriter(file_name).write(print_msg=False)
    else:
        cmd = [sys.executable, file_name]

    p = subprocess.Popen(
        cmd,
        cwd=subdir,
        stdout=stdout,
        stderr=stderr,
        env=new_env,
    )
    p.wait()

    stdout.seek(0)
    stderr.seek(0)
    print(
        textwrap.indent(stdout.read().decode("utf-8"), prefix=">>  "), file=sys.stdout
    )
    print(
        textwrap.indent(stderr.read().decode("utf-8"), prefix=">>  "), file=sys.stderr
    )
    # print(f"Isolated test failed - {file_name}")
    return p.returncode != 0
