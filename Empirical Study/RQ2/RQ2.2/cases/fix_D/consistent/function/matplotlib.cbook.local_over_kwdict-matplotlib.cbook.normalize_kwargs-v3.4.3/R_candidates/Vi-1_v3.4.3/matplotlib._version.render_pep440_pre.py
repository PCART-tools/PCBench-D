def render_pep440_pre(pieces):
    # TAG[.post.devDISTANCE] . No -dirty

    # exceptions:
    # 1: no tags. 0.post.devDISTANCE

    if pieces["closest-tag"]:
        rendered = pieces["closest-tag"]
        if pieces["distance"]:
            rendered += ".post.dev%d" % pieces["distance"]
    else:
        # exception #1
        rendered = "0.post.dev%d" % pieces["distance"]
    return rendered
