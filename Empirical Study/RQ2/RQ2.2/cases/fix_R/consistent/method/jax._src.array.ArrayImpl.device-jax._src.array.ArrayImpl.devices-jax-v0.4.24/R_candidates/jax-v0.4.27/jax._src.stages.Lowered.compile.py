  def compile(
      self, compiler_options: CompilerOptions | None = None) -> Compiled:
    """Compile, returning a corresponding ``Compiled`` instance."""
    kw: dict[str, Any] = {"compiler_options": compiler_options}
    return Compiled(
        self._lowering.compile(**kw),  # pytype: disable=wrong-keyword-args
        self.args_info,
        self.out_tree,
        no_kwargs=self._no_kwargs,
    )
