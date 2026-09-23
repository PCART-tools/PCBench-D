def test_url():
    # Test that object url appears in output svg.

    fig, ax = plt.subplots()

    # collections
    s = ax.scatter([1, 2, 3], [4, 5, 6])
    s.set_urls(['http://example.com/foo', 'http://example.com/bar', None])

    # Line2D
    p, = plt.plot([1, 3], [6, 5])
    p.set_url('http://example.com/baz')

    b = BytesIO()
    fig.savefig(b, format='svg')
    b = b.getvalue()
    for v in [b'foo', b'bar', b'baz']:
        assert b'http://example.com/' + v in b
