    def _on_timer(self):
        '''
        Runs all function that have been registered as callbacks. Functions
        can return False (or 0) if they should not be called any more. If there
        are no callbacks, the timer is automatically stopped.
        '''
        for func, args, kwargs in self.callbacks:
            ret = func(*args, **kwargs)
            # docstring above explains why we use `if ret == False` here,
            # instead of `if not ret`.
            if ret == False:
                self.callbacks.remove((func, args, kwargs))

        if len(self.callbacks) == 0:
            self.stop()
