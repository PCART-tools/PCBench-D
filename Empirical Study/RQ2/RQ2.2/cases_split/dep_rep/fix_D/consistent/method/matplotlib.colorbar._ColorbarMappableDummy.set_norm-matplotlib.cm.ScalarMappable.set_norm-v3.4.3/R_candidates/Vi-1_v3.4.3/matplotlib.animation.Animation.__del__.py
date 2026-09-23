    def __del__(self):
        if not getattr(self, '_draw_was_started', True):
            warnings.warn(
                'Animation was deleted without rendering anything. This is '
                'most likely unintended. To prevent deletion, assign the '
                'Animation to a variable that exists for as long as you need '
                'the Animation.')
