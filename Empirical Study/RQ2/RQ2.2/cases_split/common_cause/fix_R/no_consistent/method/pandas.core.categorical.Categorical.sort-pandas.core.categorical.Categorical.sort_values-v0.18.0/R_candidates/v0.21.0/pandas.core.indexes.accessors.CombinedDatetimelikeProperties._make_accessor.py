    @classmethod
    def _make_accessor(cls, data):
        try:
            return maybe_to_datetimelike(data)
        except Exception:
            raise AttributeError("Can only use .dt accessor with "
                                 "datetimelike values")
