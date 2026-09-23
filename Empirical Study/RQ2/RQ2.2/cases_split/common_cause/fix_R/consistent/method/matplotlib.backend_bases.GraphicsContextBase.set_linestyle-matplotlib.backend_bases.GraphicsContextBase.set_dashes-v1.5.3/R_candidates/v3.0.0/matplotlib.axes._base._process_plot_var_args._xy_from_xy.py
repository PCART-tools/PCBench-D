    def _xy_from_xy(self, x, y):
        if self.axes.xaxis is not None and self.axes.yaxis is not None:
            bx = self.axes.xaxis.update_units(x)
            by = self.axes.yaxis.update_units(y)

            if self.command != 'plot':
                # the Line2D class can handle unitized data, with
                # support for post hoc unit changes etc.  Other mpl
                # artists, e.g., Polygon which _process_plot_var_args
                # also serves on calls to fill, cannot.  So this is a
                # hack to say: if you are not "plot", which is
                # creating Line2D, then convert the data now to
                # floats.  If you are plot, pass the raw data through
                # to Line2D which will handle the conversion.  So
                # polygons will not support post hoc conversions of
                # the unit type since they are not storing the orig
                # data.  Hopefully we can rationalize this at a later
                # date - JDH
                if bx:
                    x = self.axes.convert_xunits(x)
                if by:
                    y = self.axes.convert_yunits(y)

        # like asanyarray, but converts scalar to array, and doesn't change
        # existing compatible sequences
        x = _check_1d(x)
        y = _check_1d(y)
        if x.shape[0] != y.shape[0]:
            raise ValueError("x and y must have same first dimension, but "
                             "have shapes {} and {}".format(x.shape, y.shape))
        if x.ndim > 2 or y.ndim > 2:
            raise ValueError("x and y can be no greater than 2-D, but have "
                             "shapes {} and {}".format(x.shape, y.shape))

        if x.ndim == 1:
            x = x[:, np.newaxis]
        if y.ndim == 1:
            y = y[:, np.newaxis]
        return x, y
