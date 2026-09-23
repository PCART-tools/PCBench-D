    def _make_dt_accessor(self):
        try:
            return maybe_to_datetimelike(self)
        except Exception:
            raise AttributeError("Can only use .dt accessor with datetimelike "
                                 "values")
