def _check_for_pgf(texsystem):
    """
    Check if a given TeX system + pgf is available

    Parameters
    ----------
    texsystem : str
        The executable name to check
    """
    with TemporaryDirectory() as tmpdir:
        tex_path = Path(tmpdir, "test.tex")
        tex_path.write_text(r"""
            \documentclass{minimal}
            \usepackage{pgf}
            \begin{document}
            \typeout{pgfversion=\pgfversion}
            \makeatletter
            \@@end
        """)
        try:
            subprocess.check_call(
                [texsystem, "-halt-on-error", str(tex_path)], cwd=tmpdir,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.CalledProcessError):
            return False
        return True
