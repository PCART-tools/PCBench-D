def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir
    app.add_directive('plot', PlotDirective)
    app.add_config_value('plot_pre_code', None, True)
    app.add_config_value('plot_include_source', False, True)
    app.add_config_value('plot_html_show_source_link', True, True)
    app.add_config_value('plot_formats', ['png', 'hires.png', 'pdf'], True)
    app.add_config_value('plot_basedir', None, True)
    app.add_config_value('plot_html_show_formats', True, True)
    app.add_config_value('plot_rcparams', {}, True)
    app.add_config_value('plot_apply_rcparams', False, True)
    app.add_config_value('plot_working_directory', None, True)
    app.add_config_value('plot_template', None, True)
    app.connect('doctree-read', mark_plot_labels)
    app.add_css_file('plot_directive.css')
    app.connect('build-finished', _copy_css_file)
    metadata = {'parallel_read_safe': True, 'parallel_write_safe': True,
                'version': matplotlib.__version__}
    return metadata
