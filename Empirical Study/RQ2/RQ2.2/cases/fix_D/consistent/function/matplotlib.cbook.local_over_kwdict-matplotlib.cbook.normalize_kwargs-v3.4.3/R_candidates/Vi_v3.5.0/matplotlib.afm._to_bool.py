def _to_bool(s):
    if s.lower().strip() in (b'false', b'0', b'no'):
        return False
    else:
        return True
