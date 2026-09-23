def latex2png(latex, filename, fontset='cm'):
    latex = "$%s$" % latex
    with mpl.rc_context({'mathtext.fontset': fontset}):
        try:
            depth = mathtext.math_to_image(
                latex, filename, dpi=100, format="png")
        except Exception:
            _api.warn_external(f"Could not render math expression {latex}")
            depth = 0
    return depth
