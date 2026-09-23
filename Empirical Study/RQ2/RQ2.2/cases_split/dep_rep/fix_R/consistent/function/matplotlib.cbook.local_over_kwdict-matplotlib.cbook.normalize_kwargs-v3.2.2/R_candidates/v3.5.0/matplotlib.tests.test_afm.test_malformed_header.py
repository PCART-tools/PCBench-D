@pytest.mark.parametrize(
    "afm_data",
    [
        b"""StartFontMetrics 2.0
Comment Comments are ignored.
Comment Creation Date:Mon Nov 13 12:34:11 GMT 2017
Aardvark bob
FontName MyFont-Bold
EncodingScheme FontSpecific
StartCharMetrics 3""",
        b"""StartFontMetrics 2.0
Comment Comments are ignored.
Comment Creation Date:Mon Nov 13 12:34:11 GMT 2017
ItalicAngle zero degrees
FontName MyFont-Bold
EncodingScheme FontSpecific
StartCharMetrics 3""",
    ],
)
def test_malformed_header(afm_data, caplog):
    fh = BytesIO(afm_data)
    with caplog.at_level(logging.ERROR):
        afm._parse_header(fh)

    assert len(caplog.records) == 1
