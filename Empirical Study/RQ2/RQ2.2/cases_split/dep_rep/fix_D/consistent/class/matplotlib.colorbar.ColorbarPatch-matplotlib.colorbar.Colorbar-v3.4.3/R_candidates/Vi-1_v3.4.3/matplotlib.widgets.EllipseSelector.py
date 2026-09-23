class EllipseSelector(RectangleSelector):
    """
    Select an elliptical region of an axes.

    For the cursor to remain responsive you must keep a reference to it.

    Example usage::

        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.widgets import EllipseSelector

        def onselect(eclick, erelease):
            "eclick and erelease are matplotlib events at press and release."
            print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
            print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
            print('used button  : ', eclick.button)

        def toggle_selector(event):
            print(' Key pressed.')
            if event.key in ['Q', 'q'] and toggle_selector.ES.active:
                print('EllipseSelector deactivated.')
                toggle_selector.RS.set_active(False)
            if event.key in ['A', 'a'] and not toggle_selector.ES.active:
                print('EllipseSelector activated.')
                toggle_selector.ES.set_active(True)

        x = np.arange(100.) / 99
        y = np.sin(x)
        fig, ax = plt.subplots()
        ax.plot(x, y)

        toggle_selector.ES = EllipseSelector(ax, onselect, drawtype='line')
        fig.canvas.mpl_connect('key_press_event', toggle_selector)
        plt.show()
    """
    _shape_klass = Ellipse

    def draw_shape(self, extents):
        x1, x2, y1, y2 = extents
        xmin, xmax = sorted([x1, x2])
        ymin, ymax = sorted([y1, y2])
        center = [x1 + (x2 - x1) / 2., y1 + (y2 - y1) / 2.]
        a = (xmax - xmin) / 2.
        b = (ymax - ymin) / 2.

        if self.drawtype == 'box':
            self.to_draw.center = center
            self.to_draw.width = 2 * a
            self.to_draw.height = 2 * b
        else:
            rad = np.deg2rad(np.arange(31) * 12)
            x = a * np.cos(rad) + center[0]
            y = b * np.sin(rad) + center[1]
            self.to_draw.set_data(x, y)

    @property
    def _rect_bbox(self):
        if self.drawtype == 'box':
            x, y = self.to_draw.center
            width = self.to_draw.width
            height = self.to_draw.height
            return x - width / 2., y - height / 2., width, height
        else:
            x, y = self.to_draw.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0
