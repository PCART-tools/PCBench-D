@pytest.mark.flaky(reruns=3)
@needs_usetex
def test_missing_psfont(monkeypatch):
    """An error is raised if a TeX font lacks a Type-1 equivalent"""
    def psfont(*args, **kwargs):
        return dviread.PsFont(texname='texfont', psname='Some Font',
                              effects=None, encoding=None, filename=None)

    monkeypatch.setattr(dviread.PsfontsMap, '__getitem__', psfont)
    rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'hello')
    with NamedTemporaryFile() as tmpfile, pytest.raises(ValueError):
        fig.savefig(tmpfile, format='pdf')
