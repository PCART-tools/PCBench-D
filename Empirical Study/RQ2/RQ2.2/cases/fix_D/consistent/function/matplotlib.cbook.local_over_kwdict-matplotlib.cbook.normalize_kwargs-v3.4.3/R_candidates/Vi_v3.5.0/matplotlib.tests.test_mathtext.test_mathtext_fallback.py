@pytest.mark.parametrize(
    "fallback,fontlist",
    [("cm", ['DejaVu Sans', 'mpltest', 'STIXGeneral', 'cmr10', 'STIXGeneral']),
     ("stix", ['DejaVu Sans', 'mpltest', 'STIXGeneral'])])
def test_mathtext_fallback(fallback, fontlist):
    mpl.font_manager.fontManager.addfont(
        str(Path(__file__).resolve().parent / 'mpltest.ttf'))
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
    tspans = (ET.fromstring(buff.getvalue())
              .findall(".//{http://www.w3.org/2000/svg}tspan[@style]"))
    # Getting the last element of the style attrib is a close enough
    # approximation for parsing the font property.
    char_fonts = [shlex.split(tspan.attrib["style"])[-1] for tspan in tspans]
    assert char_fonts == fontlist
    mpl.font_manager.fontManager.ttflist.pop()
