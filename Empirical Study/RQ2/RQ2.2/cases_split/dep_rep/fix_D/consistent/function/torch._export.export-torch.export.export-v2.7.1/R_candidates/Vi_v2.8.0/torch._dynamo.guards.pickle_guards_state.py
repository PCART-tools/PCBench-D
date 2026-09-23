def pickle_guards_state(state: GuardsState) -> bytes:
    buf = io.BytesIO()
    pickler = GuardsStatePickler(buf)
    try:
        pickler.dump(state)
    except AttributeError as e:
        raise torch._dynamo.exc.PackageError(str(e)) from e
    return buf.getvalue()
