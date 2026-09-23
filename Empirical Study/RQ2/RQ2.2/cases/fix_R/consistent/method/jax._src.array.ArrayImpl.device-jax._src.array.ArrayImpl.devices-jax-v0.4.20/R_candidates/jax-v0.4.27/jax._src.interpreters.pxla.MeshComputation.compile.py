  def compile(self, compiler_options=None) -> MeshExecutable:
    if self._executable is None or compiler_options is not None:
      executable = UnloadedMeshExecutable.from_hlo(
          self._name, self._hlo, **self.compile_args,
          compiler_options=compiler_options)
      if compiler_options is None:
        self._executable = executable
      return executable
    return self._executable
