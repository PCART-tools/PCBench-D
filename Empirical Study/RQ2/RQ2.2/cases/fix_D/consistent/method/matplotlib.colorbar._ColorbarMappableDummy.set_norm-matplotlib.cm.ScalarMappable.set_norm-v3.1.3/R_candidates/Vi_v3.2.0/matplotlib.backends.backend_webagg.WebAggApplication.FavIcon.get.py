        def get(self):
            self.set_header('Content-Type', 'image/png')
            self.write(
                cbook._get_data_path('images/matplotlib.png').read_bytes())
