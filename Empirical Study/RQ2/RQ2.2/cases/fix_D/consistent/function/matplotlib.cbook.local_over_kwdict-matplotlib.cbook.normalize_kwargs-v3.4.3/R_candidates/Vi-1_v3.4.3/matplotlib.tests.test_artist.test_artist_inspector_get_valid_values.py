@pytest.mark.parametrize('accept_clause, expected', [
    ('', 'unknown'),
    ("ACCEPTS: [ '-' | '--' | '-.' ]", "[ '-' | '--' | '-.' ]"),
    ('ACCEPTS: Some description.', 'Some description.'),
    ('.. ACCEPTS: Some description.', 'Some description.'),
    ('arg : int', 'int'),
    ('*arg : int', 'int'),
    ('arg : int\nACCEPTS: Something else.', 'Something else. '),
])
def test_artist_inspector_get_valid_values(accept_clause, expected):
    class TestArtist(martist.Artist):
        def set_f(self, arg):
            pass

    TestArtist.set_f.__doc__ = """
    Some text.

    %s
    """ % accept_clause
    valid_values = martist.ArtistInspector(TestArtist).get_valid_values('f')
    assert valid_values == expected
