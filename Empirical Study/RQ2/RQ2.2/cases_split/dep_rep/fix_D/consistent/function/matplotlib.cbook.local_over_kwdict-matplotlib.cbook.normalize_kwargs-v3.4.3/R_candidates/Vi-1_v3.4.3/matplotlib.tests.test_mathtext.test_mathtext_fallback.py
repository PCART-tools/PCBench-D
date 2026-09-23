@pytest.mark.parametrize(
    "fallback,fontlist",
    [("cm", ['DejaVu Sans', 'mpltest', 'STIXGeneral', 'cmr10', 'STIXGeneral']),
     ("stix", ['DejaVu Sans', 'mpltest', 'STIXGeneral'])])
def test_mathtext_fallback(fallback, fontlist):
    mpl.font_manager.fontManager.addfont(
        os.path.join((os.path.dirname(os.path.realpath(__file__))), 'mpltest.ttf'))
    mpl.rcParams["svg.fonttype"] = 'none'
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.rm'] = 'mpltest'
    mpl.rcParams['mathtext.it'] = 'mpltest:italic'
    mpl.rcParams['mathtext.bf'] = 'mpltest:bold'
    mpl.rcParams['mathtext.fallback'] = fallback

    test_str = r'a$A\AA\breve\gimel$'

    buff = io.BytesIO()
    fig, ax = plt.subplots()
    fig.text(.5, .5, test_str, fontsize=40, ha='center')
    fig.savefig(buff, format="svg")
    char_fonts = [
        line.split("font-family:")[-1].split(";")[0]
        for line in str(buff.getvalue()).split(r"\n") if "tspan" in line
    ]
    assert char_fonts == fontlist
    mpl.font_manager.fontManager.ttflist = mpl.font_manager.fontManager.ttflist[:-1]
