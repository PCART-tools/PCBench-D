  def addressable_data(self, index: int) -> PRNGKeyArray:
    return PRNGKeyArray(self._impl, self._base_array.addressable_data(index))
