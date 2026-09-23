def _has_tex_package(package):
    return bool(mpl.dviread.find_tex_file(f"{package}.sty"))
