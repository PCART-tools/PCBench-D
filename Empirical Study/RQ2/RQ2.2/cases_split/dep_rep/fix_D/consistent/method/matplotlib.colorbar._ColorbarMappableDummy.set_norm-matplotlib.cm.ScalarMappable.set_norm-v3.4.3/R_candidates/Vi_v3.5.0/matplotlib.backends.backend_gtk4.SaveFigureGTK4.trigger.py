    def trigger(self, *args, **kwargs):

        class PseudoToolbar:
            canvas = self.figure.canvas

        return NavigationToolbar2GTK4.save_figure(PseudoToolbar())
