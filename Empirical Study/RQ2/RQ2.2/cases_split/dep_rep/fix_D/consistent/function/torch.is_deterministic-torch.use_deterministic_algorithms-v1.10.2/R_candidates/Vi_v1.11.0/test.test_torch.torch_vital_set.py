@contextlib.contextmanager
def torch_vital_set(value):
    stash = None
    if 'TORCH_VITAL' in os.environ:
        stash = os.environ['TORCH_VITAL']
    os.environ['TORCH_VITAL'] = value
    try:
        yield
    finally:
        if stash:
            os.environ['TORCH_VITAL'] = stash
        else:
            del os.environ['TORCH_VITAL']
