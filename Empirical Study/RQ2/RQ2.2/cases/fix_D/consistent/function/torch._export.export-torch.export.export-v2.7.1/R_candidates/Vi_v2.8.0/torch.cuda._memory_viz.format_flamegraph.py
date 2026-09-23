def format_flamegraph(flamegraph_lines, flamegraph_script=None):
    if flamegraph_script is None:
        flamegraph_script = f"/tmp/{os.getuid()}_flamegraph.pl"
    if not os.path.exists(flamegraph_script):
        import tempfile
        import urllib.request

        print(f"Downloading flamegraph.pl to: {flamegraph_script}")
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".pl") as f:
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl",
                f.name,
            )
            subprocess.check_call(["chmod", "+x", f.name])
            try:
                os.rename(f.name, flamegraph_script)
            except OSError:  # noqa: B001,E722
                # Ok to skip, the file will be removed by tempfile
                pass
    args = [flamegraph_script, "--countname", "bytes"]
    p = subprocess.Popen(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf-8"
    )
    assert p.stdin is not None
    assert p.stdout is not None
    p.stdin.write(flamegraph_lines)
    p.stdin.close()
    result = p.stdout.read()
    p.stdout.close()
    p.wait()
    assert p.wait() == 0
    return result
