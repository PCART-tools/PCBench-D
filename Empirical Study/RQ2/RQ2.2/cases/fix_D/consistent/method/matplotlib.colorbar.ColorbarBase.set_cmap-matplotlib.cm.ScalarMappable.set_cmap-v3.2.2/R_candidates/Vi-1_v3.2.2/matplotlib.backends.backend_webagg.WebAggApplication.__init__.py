    def __init__(self, url_prefix=''):
        if url_prefix:
            assert url_prefix[0] == '/' and url_prefix[-1] != '/', \
                'url_prefix must start with a "/" and not end with one.'

        super().__init__(
            [
                # Static files for the CSS and JS
                (url_prefix + r'/_static/(.*)',
                 tornado.web.StaticFileHandler,
                 {'path': core.FigureManagerWebAgg.get_static_file_path()}),

                # A Matplotlib favicon
                (url_prefix + r'/favicon.ico', self.FavIcon),

                # The page that contains all of the pieces
                (url_prefix + r'/([0-9]+)', self.SingleFigurePage,
                 {'url_prefix': url_prefix}),

                # The page that contains all of the figures
                (url_prefix + r'/?', self.AllFiguresPage,
                 {'url_prefix': url_prefix}),

                (url_prefix + r'/js/mpl.js', self.MplJs),

                # Sends images and events to the browser, and receives
                # events from the browser
                (url_prefix + r'/([0-9]+)/ws', self.WebSocket),

                # Handles the downloading (i.e., saving) of static images
                (url_prefix + r'/([0-9]+)/download.([a-z0-9.]+)',
                 self.Download),
            ],
            template_path=core.FigureManagerWebAgg.get_static_file_path())
