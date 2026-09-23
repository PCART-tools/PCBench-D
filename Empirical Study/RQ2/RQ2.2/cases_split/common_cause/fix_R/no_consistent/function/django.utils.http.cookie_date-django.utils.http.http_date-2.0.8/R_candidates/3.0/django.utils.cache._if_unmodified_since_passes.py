def _if_unmodified_since_passes(last_modified, if_unmodified_since):
    """
    Test the If-Unmodified-Since comparison as defined in section 3.4 of
    RFC 7232.
    """
    return last_modified and last_modified <= if_unmodified_since
