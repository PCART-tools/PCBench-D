@dataclasses.dataclass
class AsyncCopyDescriptor:
  src_ref: Any
  src_indexers: tuple[indexing.NDIndexer, ...]
  dst_ref: Any
  dst_indexers: tuple[indexing.NDIndexer, ...]
  dst_sem: int | jax.Array
  dst_sem_indexers: tuple[indexing.NDIndexer, ...]
  src_sem: int | jax.Array | None
  src_sem_indexers: tuple[indexing.NDIndexer, ...] | None
  device_id: int | jax.Array | None
  device_id_type: DeviceIdType = DeviceIdType.MESH

  def __post_init__(self):
    if (self.src_sem is None) ^ (self.device_id is None):
      raise ValueError("Either both or neither `src_sem` and `device_id` "
                       "can be set.")

  @property
  def is_remote(self):
    return self.src_sem is not None

  def start(self):
    flat_args, tree = tree_util.tree_flatten((
        self.src_ref,
        self.src_indexers,
        self.dst_ref,
        self.dst_indexers,
        self.dst_sem,
        self.dst_sem_indexers,
        self.src_sem,
        self.src_sem_indexers,
        self.device_id,
    ))
    dma_start_p.bind(*flat_args, tree=tree, device_id_type=self.device_id_type)

  def wait(self):
    if self.is_remote:
      self.wait_send()
    self.wait_recv()

  def wait_recv(self):
    wait_args, tree = tree_util.tree_flatten(
        (self.dst_sem, self.dst_sem_indexers, self.dst_ref, self.dst_indexers)
    )
    dma_wait_p.bind(
        *wait_args, tree=tree, device_id_type=self.device_id_type
    )

  def wait_send(self):
    if not self.is_remote:
      raise ValueError("Cannot `wait_send` on a local copy.")
    wait_args, tree = tree_util.tree_flatten(
        (self.src_sem, self.src_sem_indexers, self.src_ref, self.src_indexers)
    )
    dma_wait_p.bind(
        *wait_args, tree=tree, device_id_type=self.device_id_type
    )
