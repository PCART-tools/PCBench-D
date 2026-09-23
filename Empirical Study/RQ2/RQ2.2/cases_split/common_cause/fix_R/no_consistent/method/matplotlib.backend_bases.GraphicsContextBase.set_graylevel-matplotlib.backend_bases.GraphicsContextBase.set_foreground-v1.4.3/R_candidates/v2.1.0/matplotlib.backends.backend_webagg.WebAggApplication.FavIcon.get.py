        def get(self):
            image_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'mpl-data', 'images')

            self.set_header('Content-Type', 'image/png')
            with open(os.path.join(image_path,
                                   'matplotlib.png'), 'rb') as fd:
                self.write(fd.read())
