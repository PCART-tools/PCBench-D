def lookup(tag, group=None):
    """
    :param tag: Integer tag number
    :returns: Taginfo namedtuple, From the TAGS_V2 info if possible,
        otherwise just populating the value and name from TAGS.
        If the tag is not recognized, "unknown" is returned for the name

    """

    if group is not None:
        info = TAGS_V2_GROUPS[group].get(tag) if group in TAGS_V2_GROUPS else None
    else:
        info = TAGS_V2.get(tag)
    return info or TagInfo(tag, TAGS.get(tag, "unknown"))
