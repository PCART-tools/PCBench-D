@functools.cache
def _lazy_import():
    from .. import backends
    from ..utils import import_submodule

    import_submodule(backends)

    from ..repro.after_dynamo import dynamo_minifier_backend

    assert dynamo_minifier_backend is not None

    _discover_entrypoint_backends()
