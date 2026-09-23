@pytest.mark.parametrize('writer, frame_format, output', gen_writers())
@pytest.mark.parametrize('anim', [dict(klass=dict)], indirect=['anim'])
def test_save_animation_smoketest(tmpdir, writer, frame_format, output, anim):
    if frame_format is not None:
        plt.rcParams["animation.frame_format"] = frame_format
    anim = animation.FuncAnimation(**anim)
    dpi = None
    codec = None
    if writer == 'ffmpeg':
        # Issue #8253
        anim._fig.set_size_inches((10.85, 9.21))
        dpi = 100.
        codec = 'h264'

    # Use temporary directory for the file-based writers, which produce a file
    # per frame with known names.
    with tmpdir.as_cwd():
        anim.save(output, fps=30, writer=writer, bitrate=500, dpi=dpi,
                  codec=codec)

    del anim
