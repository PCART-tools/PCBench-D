@contextlib.contextmanager
def dynamo_disable_grad(tx):
    from . import GradModeVariable

    gmv = GradModeVariable.create(tx, False)
    try:
        gmv.enter(tx)
        yield
    finally:
        gmv.exit(tx)
