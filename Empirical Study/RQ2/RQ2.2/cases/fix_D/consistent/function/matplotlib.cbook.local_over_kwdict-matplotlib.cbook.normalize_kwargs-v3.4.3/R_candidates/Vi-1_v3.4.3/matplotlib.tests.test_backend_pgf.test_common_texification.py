@pytest.mark.parametrize('plain_text, escaped_text', [
    (r'quad_sum: $\sum x_i^2$', r'quad\_sum: \(\displaystyle \sum x_i^2\)'),
    (r'no \$splits \$ here', r'no \$splits \$ here'),
    ('with_underscores', r'with\_underscores'),
    ('% not a comment', r'\% not a comment'),
    ('^not', r'\^not'),
])
def test_common_texification(plain_text, escaped_text):
    assert common_texification(plain_text) == escaped_text
