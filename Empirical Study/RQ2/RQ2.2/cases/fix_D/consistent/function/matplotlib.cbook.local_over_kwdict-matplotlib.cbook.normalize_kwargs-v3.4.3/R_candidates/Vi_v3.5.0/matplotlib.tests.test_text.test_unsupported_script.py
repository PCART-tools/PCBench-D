def test_unsupported_script(recwarn):
    fig = plt.figure()
    fig.text(.5, .5, "\N{BENGALI DIGIT ZERO}")
    fig.canvas.draw()
    assert all(isinstance(warn.message, UserWarning) for warn in recwarn)
    assert (
        [warn.message.args for warn in recwarn] ==
        [(r"Glyph 2534 (\N{BENGALI DIGIT ZERO}) missing from current font.",),
         (r"Matplotlib currently does not support Bengali natively.",)])
