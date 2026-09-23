    def get_xaxis_text1_transform(self, pad):
        if _is_full_circle_rad(*self._realViewLim.intervalx):
            return self._xaxis_text_transform, 'center', 'center'
        else:
            return self._xaxis_text_transform, 'bottom', 'center'
