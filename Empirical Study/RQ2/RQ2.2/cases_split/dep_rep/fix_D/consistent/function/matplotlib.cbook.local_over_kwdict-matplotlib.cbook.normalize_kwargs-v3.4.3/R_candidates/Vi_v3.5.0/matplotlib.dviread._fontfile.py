@lru_cache()
def _fontfile(cls, suffix, texname):
    filename = find_tex_file(texname + suffix)
    return cls(filename) if filename else None
