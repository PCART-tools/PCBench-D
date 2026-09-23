@pytest.mark.parametrize(
    "afm_data",
    [
        b"""nope
really nope""",
        b"""StartFontMetrics 2.0
Comment Comments are ignored.
Comment Creation Date:Mon Nov 13 12:34:11 GMT 2017
FontName MyFont-Bold
EncodingScheme FontSpecific""",
    ],
)
def test_bad_afm(afm_data):
    fh = BytesIO(afm_data)
    with pytest.raises(RuntimeError):
        afm._parse_header(fh)
