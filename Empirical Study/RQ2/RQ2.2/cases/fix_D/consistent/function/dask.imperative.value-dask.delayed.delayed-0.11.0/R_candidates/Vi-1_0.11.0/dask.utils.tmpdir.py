@contextmanager
def tmpdir(dir=None):
    dirname = tempfile.mkdtemp(dir=dir)

    try:
        yield dirname
    finally:
        if os.path.exists(dirname):
            if os.path.isdir(dirname):
                shutil.rmtree(dirname)
            else:
                with ignoring(OSError):
                    os.remove(dirname)
