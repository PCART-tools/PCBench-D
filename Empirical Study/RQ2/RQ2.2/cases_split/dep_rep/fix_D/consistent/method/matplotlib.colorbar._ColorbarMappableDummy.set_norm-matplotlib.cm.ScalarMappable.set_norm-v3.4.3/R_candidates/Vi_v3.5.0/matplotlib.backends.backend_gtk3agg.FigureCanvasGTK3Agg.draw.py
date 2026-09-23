    def draw(self):
        # Call these explicitly because GTK's draw is a GObject method which
        # isn't cooperative with Python class methods.
        backend_agg.FigureCanvasAgg.draw(self)
        backend_gtk3.FigureCanvasGTK3.draw(self)
