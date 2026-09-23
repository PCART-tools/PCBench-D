    def draw_idle(self):
        # docstring inherited
        if not (getattr(self, '_draw_pending', False) or
                getattr(self, '_is_drawing', False)):
            self._draw_pending = True
            # Add a singleshot timer to the eventloop that will call back
            # into the Python method _draw_idle to take care of the draw
            self._single_shot_timer(self._draw_idle)
