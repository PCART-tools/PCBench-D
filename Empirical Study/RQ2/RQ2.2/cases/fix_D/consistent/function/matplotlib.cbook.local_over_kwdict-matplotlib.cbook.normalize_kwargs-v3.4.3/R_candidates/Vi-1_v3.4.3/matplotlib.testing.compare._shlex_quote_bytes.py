def _shlex_quote_bytes(b):
    return (b if _find_unsafe_bytes(b) is None
            else b"'" + b.replace(b"'", b"'\"'\"'") + b"'")
