    @staticmethod
    def _build_latex_header():
        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        # Create LaTeX header with some content, else LaTeX will load some math
        # fonts later when we don't expect the additional output on stdout.
        # TODO: is this sufficient?
        latex_header = [r"\documentclass{minimal}",
                        latex_preamble,
                        latex_fontspec,
                        r"\begin{document}",
                        r"text $math \mu$",  # force latex to load fonts now
                        r"\typeout{pgf_backend_query_start}"]
        return "\n".join(latex_header)
