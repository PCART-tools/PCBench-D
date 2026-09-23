def setup(app):
    # NOTE: in Sphinx 1.8+ `html_css_files` is an official configuration value
    # and can be moved outside of this function (and the setup(app) function
    # can be deleted).
    html_css_files = [
        'https://cdn.jsdelivr.net/npm/katex@0.10.0-beta/dist/katex.min.css'
    ]

    # In Sphinx 1.8 it was renamed to `add_css_file`, 1.7 and prior it is
    # `add_stylesheet` (deprecated in 1.8).
    add_css = getattr(app, 'add_css_file', app.add_stylesheet)
    for css_file in html_css_files:
        add_css(css_file)

    app.connect("build-finished", coverage_post_process)
