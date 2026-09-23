    def display_js(self):
        # XXX How to do this just once? It has to deal with multiple
        # browser instances using the same kernel (require.js - but the
        # file isn't static?).
        display(Javascript(FigureManagerNbAgg.get_javascript()))
