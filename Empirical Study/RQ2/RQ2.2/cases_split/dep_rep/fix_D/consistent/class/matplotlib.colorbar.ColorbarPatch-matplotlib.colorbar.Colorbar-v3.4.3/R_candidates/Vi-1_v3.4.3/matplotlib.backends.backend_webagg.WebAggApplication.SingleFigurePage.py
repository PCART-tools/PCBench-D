    class SingleFigurePage(tornado.web.RequestHandler):
        def __init__(self, application, request, *, url_prefix='', **kwargs):
            self.url_prefix = url_prefix
            super().__init__(application, request, **kwargs)

        def get(self, fignum):
            fignum = int(fignum)
            manager = Gcf.get_fig_manager(fignum)

            ws_uri = 'ws://{req.host}{prefix}/'.format(req=self.request,
                                                       prefix=self.url_prefix)
            self.render(
                "single_figure.html",
                prefix=self.url_prefix,
                ws_uri=ws_uri,
                fig_id=fignum,
                toolitems=core.NavigationToolbar2WebAgg.toolitems,
                canvas=manager.canvas)
