        def get(self):
            ws_uri = 'ws://{req.host}{prefix}/'.format(req=self.request,
                                                       prefix=self.url_prefix)
            self.render(
                "all_figures.html",
                prefix=self.url_prefix,
                ws_uri=ws_uri,
                figures=sorted(
                    list(Gcf.figs.items()), key=lambda item: item[0]),
                toolitems=core.NavigationToolbar2WebAgg.toolitems)
