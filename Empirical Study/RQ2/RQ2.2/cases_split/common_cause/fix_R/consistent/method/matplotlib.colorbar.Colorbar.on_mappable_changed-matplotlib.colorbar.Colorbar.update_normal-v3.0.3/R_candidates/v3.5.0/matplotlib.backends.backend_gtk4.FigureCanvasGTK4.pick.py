    def pick(self, mouseevent):
        # GtkWidget defines pick in GTK4, so we need to override here to work
        # with the base implementation we want.
        FigureCanvasBase.pick(self, mouseevent)
