    class Download(tornado.web.RequestHandler):
        def get(self, fignum, fmt):
            fignum = int(fignum)
            manager = Gcf.get_fig_manager(fignum)
            self.set_header(
                'Content-Type', mimetypes.types_map.get(fmt, 'binary'))
            buff = BytesIO()
            manager.canvas.figure.savefig(buff, format=fmt)
            self.write(buff.getvalue())
