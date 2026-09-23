def render(s):
    s = str(s)
    cmd_exists = lambda x: any(
        os.access(os.path.join(path, x), os.X_OK)
        for path in os.getenv("PATH", "").split(os.pathsep)
    )
    if cmd_exists("graph-easy"):
        p = Popen("graph-easy", stdin=PIPE)
        try:
            p.stdin.write(s.encode("utf-8"))
        except IOError as e:
            if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
                pass
            else:
                # Raise any other error.
                raise

        p.stdin.close()
        p.wait()
    else:
        print(s)
