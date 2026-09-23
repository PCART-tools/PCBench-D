    def get_xaxis_text2_transform(self, pad):
        if _is_full_circle_rad(*self._realViewLim.intervalx):
            return self._xaxis_text_transform, 'center', 'center'
        else:
            return self._xaxis_text_transform, 'top', 'center'
