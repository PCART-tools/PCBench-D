@contextlib.contextmanager
def _wrap_text(textobj):
    """Temporarily inserts newlines if the wrap option is enabled."""
    if textobj.get_wrap():
        old_text = textobj.get_text()
        try:
            textobj.set_text(textobj._get_wrapped_text())
            yield textobj
        finally:
            textobj.set_text(old_text)
    else:
        yield textobj
