    @classmethod
    def _missing_(cls, value: object) -> Precision | None:
      return _precision_strings.get(value)
