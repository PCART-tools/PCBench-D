    class FavIcon(tornado.web.RequestHandler):
        def get(self):
            self.set_header('Content-Type', 'image/png')
            self.write(Path(mpl.get_data_path(),
                            'images/matplotlib.png').read_bytes())
