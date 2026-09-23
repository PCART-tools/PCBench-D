@contextmanager
def set_original_aten_op(func: OpOverload) -> Generator[None, None, None]:
    global ORIGINAL_ATEN
    if ORIGINAL_ATEN is None and fx_traceback.has_preserved_node_meta():
        ORIGINAL_ATEN = func
        fx_traceback.current_meta["original_aten"] = func
        try:
            yield
        finally:
            ORIGINAL_ATEN = None
            fx_traceback.current_meta["original_aten"] = None
    else:
        yield
