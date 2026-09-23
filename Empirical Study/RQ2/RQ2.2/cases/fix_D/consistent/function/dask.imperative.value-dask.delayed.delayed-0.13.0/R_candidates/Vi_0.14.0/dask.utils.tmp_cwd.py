@contextmanager
def tmp_cwd(dir=None):
    with tmpdir(dir) as dirname:
        with changed_cwd(dirname):
            yield dirname
