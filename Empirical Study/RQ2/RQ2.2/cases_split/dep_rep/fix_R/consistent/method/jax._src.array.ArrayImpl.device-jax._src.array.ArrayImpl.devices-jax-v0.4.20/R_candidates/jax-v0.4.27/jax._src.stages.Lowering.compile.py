  def compile(
      self, compiler_options: CompilerOptions | None = None) -> Executable:
    """Compile and return a corresponding ``Executable``."""
    raise NotImplementedError
