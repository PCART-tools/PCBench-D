    def _prep_window(self, **kwargs):
        """
        Provide validation for our window type, return the window
        we have already been validated.
        """

        window = self._get_window()
        if isinstance(window, (list, tuple, np.ndarray)):
            return com.asarray_tuplesafe(window).astype(float)
        elif is_integer(window):
            import scipy.signal as sig

            # the below may pop from kwargs
            def _validate_win_type(win_type, kwargs):
                arg_map = {
                    "kaiser": ["beta"],
                    "gaussian": ["std"],
                    "general_gaussian": ["power", "width"],
                    "slepian": ["width"],
                    "exponential": ["tau"],
                }

                if win_type in arg_map:
                    win_args = _pop_args(win_type, arg_map[win_type], kwargs)
                    if win_type == "exponential":
                        # exponential window requires the first arg (center)
                        # to be set to None (necessary for symmetric window)
                        win_args.insert(0, None)

                    return tuple([win_type] + win_args)

                return win_type

            def _pop_args(win_type, arg_names, kwargs):
                msg = "%s window requires %%s" % win_type
                all_args = []
                for n in arg_names:
                    if n not in kwargs:
                        raise ValueError(msg % n)
                    all_args.append(kwargs.pop(n))
                return all_args

            win_type = _validate_win_type(self.win_type, kwargs)
            # GH #15662. `False` makes symmetric window, rather than periodic.
            return sig.get_window(win_type, window, False).astype(float)
