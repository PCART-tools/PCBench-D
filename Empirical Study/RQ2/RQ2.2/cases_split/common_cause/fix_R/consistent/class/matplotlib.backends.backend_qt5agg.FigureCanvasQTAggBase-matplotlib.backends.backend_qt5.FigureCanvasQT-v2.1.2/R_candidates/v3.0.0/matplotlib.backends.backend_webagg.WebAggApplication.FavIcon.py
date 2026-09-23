    class FavIcon(tornado.web.RequestHandler):
        def get(self):
            self.set_header('Content-Type', 'image/png')
            image_path = Path(rcParams["datapath"], "images", "matplotlib.png")
            self.write(image_path.read_bytes())
