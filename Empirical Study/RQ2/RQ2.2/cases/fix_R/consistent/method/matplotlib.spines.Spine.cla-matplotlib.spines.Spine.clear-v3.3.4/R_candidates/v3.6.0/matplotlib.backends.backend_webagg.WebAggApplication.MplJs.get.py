        def get(self):
            self.set_header('Content-Type', 'application/javascript')

            js_content = core.FigureManagerWebAgg.get_javascript()

            self.write(js_content)
