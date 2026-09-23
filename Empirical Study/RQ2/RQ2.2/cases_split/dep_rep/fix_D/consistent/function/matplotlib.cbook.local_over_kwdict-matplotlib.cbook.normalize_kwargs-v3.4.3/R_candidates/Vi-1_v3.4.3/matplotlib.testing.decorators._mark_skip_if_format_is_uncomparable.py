def _mark_skip_if_format_is_uncomparable(extension):
    import pytest
    if isinstance(extension, str):
        name = extension
        marks = []
    elif isinstance(extension, tuple):
        # Extension might be a pytest ParameterSet instead of a plain string.
        # Unfortunately, this type is not exposed, so since it's a namedtuple,
        # check for a tuple instead.
        name, = extension.values
        marks = [*extension.marks]
    else:
        # Extension might be a pytest marker instead of a plain string.
        name, = extension.args
        marks = [extension.mark]
    return pytest.param(name,
                        marks=[*marks, _skip_if_format_is_uncomparable(name)])
