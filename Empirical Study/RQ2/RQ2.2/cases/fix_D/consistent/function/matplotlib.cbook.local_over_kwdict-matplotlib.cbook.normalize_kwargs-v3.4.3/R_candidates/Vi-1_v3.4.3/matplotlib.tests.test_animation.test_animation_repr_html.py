@pytest.mark.parametrize('writer', [
    pytest.param(
        'ffmpeg', marks=pytest.mark.skipif(
            not animation.FFMpegWriter.isAvailable(),
            reason='Requires FFMpeg')),
    pytest.param(
        'imagemagick', marks=pytest.mark.skipif(
            not animation.ImageMagickWriter.isAvailable(),
            reason='Requires ImageMagick')),
])
@pytest.mark.parametrize('html, want', [
    ('none', None),
    ('html5', '<video width'),
    ('jshtml', '<script ')
])
@pytest.mark.parametrize('anim', [dict(klass=dict)], indirect=['anim'])
def test_animation_repr_html(writer, html, want, anim):
    if (writer == 'imagemagick' and html == 'html5'
            # ImageMagick delegates to ffmpeg for this format.
            and not animation.FFMpegWriter.isAvailable()):
        pytest.skip('Requires FFMpeg')
    # create here rather than in the fixture otherwise we get __del__ warnings
    # about producing no output
    anim = animation.FuncAnimation(**anim)
    with plt.rc_context({'animation.writer': writer,
                         'animation.html': html}):
        html = anim._repr_html_()
    if want is None:
        assert html is None
        with pytest.warns(UserWarning):
            del anim  # Animtion was never run, so will warn on cleanup.
    else:
        assert want in html
