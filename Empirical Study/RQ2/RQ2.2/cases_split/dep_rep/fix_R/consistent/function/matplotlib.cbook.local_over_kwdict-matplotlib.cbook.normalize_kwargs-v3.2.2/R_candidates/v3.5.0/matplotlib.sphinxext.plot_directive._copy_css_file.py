def _copy_css_file(app, exc):
    if exc is None and app.builder.format == 'html':
        src = cbook._get_data_path('plot_directive/plot_directive.css')
        dst = app.outdir / Path('_static')
        dst.mkdir(exist_ok=True)
        shutil.copy(src, dst)
