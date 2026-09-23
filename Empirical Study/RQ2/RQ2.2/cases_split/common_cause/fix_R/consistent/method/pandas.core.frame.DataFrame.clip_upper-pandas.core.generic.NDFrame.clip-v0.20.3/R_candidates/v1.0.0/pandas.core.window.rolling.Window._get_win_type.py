    def _get_win_type(self, kwargs: Dict) -> Union[str, Tuple]:
        """
        Extract arguments for the window type, provide validation for it
        and return the validated window type.

        Parameters
        ----------
        kwargs : dict

        Returns
        -------
        win_type : str, or tuple
        """
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
            all_args = []
            for n in arg_names:
                if n not in kwargs:
                    raise ValueError(f"{win_type} window requires {n}")
                all_args.append(kwargs.pop(n))
            return all_args

        return _validate_win_type(self.win_type, kwargs)
