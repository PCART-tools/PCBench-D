def _checked_on_freetype_version(required_freetype_version):
    import pytest
    reason = ("Mismatched version of freetype. "
              "Test requires '%s', you have '%s'" %
              (required_freetype_version, ft2font.__freetype_version__))
    return pytest.mark.xfail(
        not check_freetype_version(required_freetype_version),
        reason=reason, raises=ImageComparisonFailure, strict=False)
