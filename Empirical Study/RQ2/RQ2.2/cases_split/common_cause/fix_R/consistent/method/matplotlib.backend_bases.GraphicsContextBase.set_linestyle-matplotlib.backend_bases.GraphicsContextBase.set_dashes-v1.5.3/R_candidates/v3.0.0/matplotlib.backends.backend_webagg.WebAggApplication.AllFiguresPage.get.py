        def get(self):
            ws_uri = 'ws://{req.host}{prefix}/'.format(req=self.request,
                                                       prefix=self.url_prefix)
            self.render(
                "all_figures.html",
                prefix=self.url_prefix,
                ws_uri=ws_uri,
                figures=sorted(Gcf.figs.items()),
                toolitems=core.NavigationToolbar2WebAgg.toolitems)
