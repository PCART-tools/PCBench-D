def test_plot_html_show_source_link(tmpdir):
    source_dir = Path(tmpdir) / 'src'
    source_dir.mkdir()
    parent = Path(__file__).parent
    shutil.copyfile(parent / 'tinypages/conf.py', source_dir / 'conf.py')
    shutil.copytree(parent / 'tinypages/_static', source_dir / '_static')
    doctree_dir = source_dir / 'doctrees'
    (source_dir / 'index.rst').write_text("""
.. plot::

    plt.plot(range(2))
""")
    # Make sure source scripts are created by default
    html_dir1 = source_dir / '_build' / 'html1'
    build_sphinx_html(source_dir, doctree_dir, html_dir1)
    assert "index-1.py" in [p.name for p in html_dir1.iterdir()]
    # Make sure source scripts are NOT created when
    # plot_html_show_source_link` is False
    html_dir2 = source_dir / '_build' / 'html2'
    build_sphinx_html(source_dir, doctree_dir, html_dir2,
                      extra_args=['-D', 'plot_html_show_source_link=0'])
    assert "index-1.py" not in [p.name for p in html_dir2.iterdir()]
