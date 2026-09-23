def render_git_describe_long(pieces):
    # TAG-DISTANCE-gHEX[-dirty], like 'git describe --tags --dirty
    # --always -long'. The distance/hash is unconditional.

    # exceptions:
    # 1: no tags. HEX[-dirty]  (note: no 'g' prefix)

    if pieces["closest-tag"]:
        rendered = pieces["closest-tag"]
        rendered += "-%d-g%s" % (pieces["distance"], pieces["short"])
    else:
        # exception #1
        rendered = pieces["short"]
    if pieces["dirty"]:
        rendered += "-dirty"
    return rendered
