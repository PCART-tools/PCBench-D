def build_sphinx_html(source_dir, doctree_dir, html_dir, extra_args=None):
    # Build the pages with warnings turned into errors
    extra_args = [] if extra_args is None else extra_args
    cmd = [sys.executable, '-msphinx', '-W', '-b', 'html',
           '-d', str(doctree_dir), str(source_dir), str(html_dir), *extra_args]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True,
                 env={**os.environ, "MPLBACKEND": ""})
    out, err = proc.communicate()

    assert proc.returncode == 0, \
        f"sphinx build failed with stdout:\n{out}\nstderr:\n{err}\n"
    if err:
        pytest.fail(f"sphinx build emitted the following warnings:\n{err}")

    assert html_dir.is_dir()
