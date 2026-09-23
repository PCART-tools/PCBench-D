    class AllFiguresPage(tornado.web.RequestHandler):
        def __init__(self, application, request, *, url_prefix='', **kwargs):
            self.url_prefix = url_prefix
            super().__init__(application, request, **kwargs)

        def get(self):
            ws_uri = 'ws://{req.host}{prefix}/'.format(req=self.request,
                                                       prefix=self.url_prefix)
            self.render(
                "all_figures.html",
                prefix=self.url_prefix,
                ws_uri=ws_uri,
                figures=sorted(Gcf.figs.items()),
                toolitems=core.NavigationToolbar2WebAgg.toolitems)
