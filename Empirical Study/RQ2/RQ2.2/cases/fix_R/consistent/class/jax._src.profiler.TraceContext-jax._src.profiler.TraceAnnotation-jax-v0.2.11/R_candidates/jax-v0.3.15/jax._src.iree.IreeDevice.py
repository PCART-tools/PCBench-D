class IreeDevice:

  def __init__(self, client):
    self.id = 0
    self.host_id = 0
    self.process_index = 0
    self.platform = "iree"
    self.device_kind = "IREE device"
    self.client = client

  def __str__(self) -> str:
    return "IreeDevice"

  def transfer_to_infeed(self, literal: Any):
    raise NotImplementedError("transfer_to_infeed")

  def transfer_from_outfeed(self, shape: xla_client.Shape):
    raise NotImplementedError("transfer_to_outfeed")

  def live_buffers(self) -> List[IreeBuffer]:
    raise NotImplementedError("live_buffers")
