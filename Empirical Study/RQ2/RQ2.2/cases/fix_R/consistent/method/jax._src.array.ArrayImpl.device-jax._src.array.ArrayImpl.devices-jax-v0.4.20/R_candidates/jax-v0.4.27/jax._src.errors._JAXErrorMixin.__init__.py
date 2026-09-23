  def __init__(self, message: str):
    error_page = self._error_page
    module_name = self._module_name
    class_name = self.__class__.__name__
    error_msg = f'{message}\nSee {error_page}#{module_name}.{class_name}'
    # https://github.com/python/mypy/issues/5887
    super().__init__(error_msg)  # type: ignore
