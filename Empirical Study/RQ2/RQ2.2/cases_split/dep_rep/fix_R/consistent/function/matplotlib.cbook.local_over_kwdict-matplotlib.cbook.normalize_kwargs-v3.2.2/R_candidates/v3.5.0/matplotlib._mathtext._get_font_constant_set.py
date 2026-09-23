def _get_font_constant_set(state):
    constants = _font_constant_mapping.get(
        state.font_output._get_font(state.font).family_name,
        FontConstantsBase)
    # STIX sans isn't really its own fonts, just different code points
    # in the STIX fonts, so we have to detect this one separately.
    if (constants is STIXFontConstants and
            isinstance(state.font_output, StixSansFonts)):
        return STIXSansFontConstants
    return constants
