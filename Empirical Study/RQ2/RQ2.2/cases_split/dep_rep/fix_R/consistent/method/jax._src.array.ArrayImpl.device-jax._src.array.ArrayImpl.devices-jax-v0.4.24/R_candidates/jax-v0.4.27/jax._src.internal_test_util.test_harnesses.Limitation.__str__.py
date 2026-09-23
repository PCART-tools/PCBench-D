  def __str__(self):
    return (f"\"{self.description}\" devices={self.devices} "
            f"dtypes={[np.dtype(dt).name for dt in self.dtypes]}" +
            (" (skip_run) " if self.skip_run else ""))
