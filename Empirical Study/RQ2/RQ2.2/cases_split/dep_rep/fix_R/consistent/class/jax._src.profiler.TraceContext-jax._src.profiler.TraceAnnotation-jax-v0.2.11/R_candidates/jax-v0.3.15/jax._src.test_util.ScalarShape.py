class ScalarShape:
  def __len__(self): return 0
  def __getitem__(self, i): raise IndexError(f"index {i} out of range.")
