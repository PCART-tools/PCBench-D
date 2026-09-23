    def view_limits(self, vmin, vmax):
        'Try to choose the view limits intelligently'
        b = self._base
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            if not is_decade(abs(vmin), b):
                if vmin < 0:
                    vmin = -decade_up(-vmin, b)
                else:
                    vmin = decade_down(vmin, b)
            if not is_decade(abs(vmax), b):
                if vmax < 0:
                    vmax = -decade_down(-vmax, b)
                else:
                    vmax = decade_up(vmax, b)

            if vmin == vmax:
                if vmin < 0:
                    vmin = -decade_up(-vmin, b)
                    vmax = -decade_down(-vmax, b)
                else:
                    vmin = decade_down(vmin, b)
                    vmax = decade_up(vmax, b)

        result = mtransforms.nonsingular(vmin, vmax)
        return result
