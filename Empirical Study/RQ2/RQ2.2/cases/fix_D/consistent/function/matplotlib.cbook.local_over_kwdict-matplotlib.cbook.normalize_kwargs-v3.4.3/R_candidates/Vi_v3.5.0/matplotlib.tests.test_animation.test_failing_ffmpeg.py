@pytest.mark.skipif(os.name != "posix", reason="requires a POSIX OS")
def test_failing_ffmpeg(tmpdir, monkeypatch, anim):
    """
    Test that we correctly raise a CalledProcessError when ffmpeg fails.

    To do so, mock ffmpeg using a simple executable shell script that
    succeeds when called with no arguments (so that it gets registered by
    `isAvailable`), but fails otherwise, and add it to the $PATH.
    """
    with tmpdir.as_cwd():
        monkeypatch.setenv("PATH", ".:" + os.environ["PATH"])
        exe_path = Path(str(tmpdir), "ffmpeg")
        exe_path.write_text("#!/bin/sh\n"
                            "[[ $@ -eq 0 ]]\n")
        os.chmod(str(exe_path), 0o755)
        with pytest.raises(subprocess.CalledProcessError):
            anim.save("test.mpeg")
