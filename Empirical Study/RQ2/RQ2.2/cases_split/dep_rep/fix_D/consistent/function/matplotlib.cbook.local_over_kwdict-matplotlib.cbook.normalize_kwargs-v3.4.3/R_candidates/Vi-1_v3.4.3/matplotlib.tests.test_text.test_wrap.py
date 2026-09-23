def test_wrap():
    fig = plt.figure(figsize=(6, 4))
    s = 'This is a very long text that should be wrapped multiple times.'
    text = fig.text(0.7, 0.5, s, wrap=True)
    fig.canvas.draw()
    assert text._get_wrapped_text() == ('This is a very long\n'
                                        'text that should be\n'
                                        'wrapped multiple\n'
                                        'times.')
