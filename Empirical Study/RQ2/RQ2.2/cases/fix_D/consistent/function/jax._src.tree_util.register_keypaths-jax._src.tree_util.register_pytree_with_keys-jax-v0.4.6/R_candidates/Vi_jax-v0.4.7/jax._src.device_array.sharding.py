  def sharding(self):
    return jax.sharding.SingleDeviceSharding(self.device())
