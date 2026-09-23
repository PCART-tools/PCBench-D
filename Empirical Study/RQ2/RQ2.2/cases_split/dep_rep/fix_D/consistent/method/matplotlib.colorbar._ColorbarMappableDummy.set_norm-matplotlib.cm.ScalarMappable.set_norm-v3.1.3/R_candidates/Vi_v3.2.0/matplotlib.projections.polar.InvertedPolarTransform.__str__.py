    def __str__(self):
        return ("{}(\n"
                    "{},\n"
                "    use_rmin={},\n"
                "    _apply_theta_transforms={})"
                .format(type(self).__name__,
                        mtransforms._indent_str(self._axis),
                        self._use_rmin,
                        self._apply_theta_transforms))
