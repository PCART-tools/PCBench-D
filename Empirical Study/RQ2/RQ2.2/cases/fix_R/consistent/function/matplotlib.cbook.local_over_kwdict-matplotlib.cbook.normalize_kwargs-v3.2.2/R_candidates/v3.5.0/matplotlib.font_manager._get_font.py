@lru_cache(64)
def _get_font(filename, hinting_factor, *, _kerning_factor, thread_id):
    return ft2font.FT2Font(
        filename, hinting_factor, _kerning_factor=_kerning_factor)
