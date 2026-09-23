@needs_pdflatex
@pytest.mark.skipif(not _has_tex_package('ucs'), reason='needs ucs.sty')
@pytest.mark.backend('pgf')
@image_comparison(['pgf_pdflatex.pdf'], style='default')
def test_pdflatex():
    if os.environ.get('APPVEYOR'):
        pytest.xfail("pdflatex test does not work on appveyor due to missing "
                     "LaTeX fonts")

    rc_pdflatex = {'font.family': 'serif',
                   'pgf.rcfonts': False,
                   'pgf.texsystem': 'pdflatex',
                   'pgf.preamble': ('\\usepackage[utf8x]{inputenc}'
                                    '\\usepackage[T1]{fontenc}')}
    mpl.rcParams.update(rc_pdflatex)
    create_figure()
