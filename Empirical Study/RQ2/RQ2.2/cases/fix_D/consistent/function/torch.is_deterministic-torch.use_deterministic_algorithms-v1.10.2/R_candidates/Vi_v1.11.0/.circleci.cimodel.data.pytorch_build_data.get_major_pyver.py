def get_major_pyver(dotted_version):
    parts = dotted_version.split(".")
    return "py" + parts[0]
