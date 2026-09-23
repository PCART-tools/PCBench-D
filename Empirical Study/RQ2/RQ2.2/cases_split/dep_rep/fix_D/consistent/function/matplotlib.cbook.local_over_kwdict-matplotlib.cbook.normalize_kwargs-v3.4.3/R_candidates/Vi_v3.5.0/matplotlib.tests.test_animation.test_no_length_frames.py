@pytest.mark.parametrize('anim', [dict(frames=iter(range(5)))],
                         indirect=['anim'])
def test_no_length_frames(anim):
    anim.save('unused.null', writer=NullMovieWriter())
