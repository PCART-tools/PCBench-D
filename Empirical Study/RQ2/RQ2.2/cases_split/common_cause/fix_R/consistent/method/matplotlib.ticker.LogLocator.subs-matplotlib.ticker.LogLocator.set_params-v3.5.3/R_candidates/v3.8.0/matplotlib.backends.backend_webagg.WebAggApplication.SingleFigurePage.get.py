        def get(self, fignum):
            fignum = int(fignum)
            manager = Gcf.get_fig_manager(fignum)

            ws_uri = f'ws://{self.request.host}{self.url_prefix}/'
            self.render(
                "single_figure.html",
                prefix=self.url_prefix,
                ws_uri=ws_uri,
                fig_id=fignum,
                toolitems=core.NavigationToolbar2WebAgg.toolitems,
                canvas=manager.canvas)
