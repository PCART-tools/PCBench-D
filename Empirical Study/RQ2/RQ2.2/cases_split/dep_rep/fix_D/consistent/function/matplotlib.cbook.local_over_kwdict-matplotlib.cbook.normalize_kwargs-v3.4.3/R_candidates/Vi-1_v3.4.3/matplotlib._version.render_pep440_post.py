def render_pep440_post(pieces):
    # TAG[.postDISTANCE[.dev0]+gHEX] . The ".dev0" means dirty. Note that
    # .dev0 sorts backwards (a dirty tree will appear "older" than the
    # corresponding clean one), but you shouldn't be releasing software with
    # -dirty anyways.

    # exceptions:
    # 1: no tags. 0.postDISTANCE[.dev0]

    if pieces["closest-tag"]:
        rendered = pieces["closest-tag"]
        if pieces["distance"] or pieces["dirty"]:
            rendered += ".post%d" % pieces["distance"]
            if pieces["dirty"]:
                rendered += ".dev0"
            rendered += plus_or_dot(pieces)
            rendered += "g%s" % pieces["short"]
    else:
        # exception #1
        rendered = "0.post%d" % pieces["distance"]
        if pieces["dirty"]:
            rendered += ".dev0"
        rendered += "+g%s" % pieces["short"]
    return rendered
