def _make_unique_name(seen, name, min_version=0):
    assert name is not None
    i = min_version
    x = '%s_%d' % (name, i) if i else name
    while x in seen:
        i += 1
        x = '%s_%d' % (name, i)
    seen.add(x)
    return x
