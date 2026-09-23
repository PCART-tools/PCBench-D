  def __str__(self):
    mesh_str = ", ".join(f"'{k}': {v}" for k, v in self.shape.items())
    return f"Mesh({mesh_str})"
