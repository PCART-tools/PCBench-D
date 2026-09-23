def _populate():
    for k, v in TAGS_V2.items():
        # Populate legacy structure.
        TAGS[k] = v[0]
        if len(v) == 4:
            for sk, sv in v[3].items():
                TAGS[(k, sv)] = sk

        TAGS_V2[k] = TagInfo(k, *v)

    for group, tags in TAGS_V2_GROUPS.items():
        for k, v in tags.items():
            tags[k] = TagInfo(k, *v)
