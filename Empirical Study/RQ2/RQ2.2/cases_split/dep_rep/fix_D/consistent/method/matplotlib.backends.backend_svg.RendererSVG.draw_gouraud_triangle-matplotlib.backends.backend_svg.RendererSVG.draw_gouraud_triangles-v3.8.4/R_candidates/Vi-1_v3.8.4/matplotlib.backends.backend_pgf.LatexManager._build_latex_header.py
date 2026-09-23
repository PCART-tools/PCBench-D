    @staticmethod
    def _build_latex_header():
        latex_header = [
            r"\documentclass{article}",
            # Include TeX program name as a comment for cache invalidation.
            # TeX does not allow this to be the first line.
            rf"% !TeX program = {mpl.rcParams['pgf.texsystem']}",
            # Test whether \includegraphics supports interpolate option.
            r"\usepackage{graphicx}",
            _get_preamble(),
            r"\begin{document}",
            r"\typeout{pgf_backend_query_start}",
        ]
        return "\n".join(latex_header)
