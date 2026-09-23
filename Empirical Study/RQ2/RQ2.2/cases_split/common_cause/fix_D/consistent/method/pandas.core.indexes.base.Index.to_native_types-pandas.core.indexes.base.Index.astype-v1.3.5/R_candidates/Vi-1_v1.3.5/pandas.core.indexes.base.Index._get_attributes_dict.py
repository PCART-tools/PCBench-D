    @final
    def _get_attributes_dict(self) -> dict[str_t, Any]:
        """
        Return an attributes dict for my class.
        """
        return {k: getattr(self, k, None) for k in self._attributes}
