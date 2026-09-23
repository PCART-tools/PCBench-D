def _skip_if_format_is_uncomparable(extension):
    import pytest
    return pytest.mark.skipif(
        extension not in comparable_formats(),
        reason='Cannot compare {} files on this system'.format(extension))
