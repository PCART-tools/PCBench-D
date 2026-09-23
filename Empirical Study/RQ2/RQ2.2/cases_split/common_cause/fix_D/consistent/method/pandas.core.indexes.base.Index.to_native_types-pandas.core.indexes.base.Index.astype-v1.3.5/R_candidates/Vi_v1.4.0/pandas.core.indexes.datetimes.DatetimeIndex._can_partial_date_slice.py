    def _can_partial_date_slice(self, reso: Resolution) -> bool:
        # History of conversation GH#3452, GH#3931, GH#2369, GH#14826
        return reso > self._resolution_obj
