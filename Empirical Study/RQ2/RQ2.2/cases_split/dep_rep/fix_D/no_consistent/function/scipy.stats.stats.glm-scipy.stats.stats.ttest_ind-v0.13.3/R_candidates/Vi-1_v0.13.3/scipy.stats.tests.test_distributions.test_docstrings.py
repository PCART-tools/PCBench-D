@dec.skipif(DOCSTRINGS_STRIPPED)
def test_docstrings():
    badones = [',\s*,', '\(\s*,', '^\s*:']
    for distname in stats.__all__:
        dist = getattr(stats, distname)
        if isinstance(dist, (stats.rv_discrete, stats.rv_continuous)):
            for regex in badones:
                assert_( re.search(regex, dist.__doc__) is None)
