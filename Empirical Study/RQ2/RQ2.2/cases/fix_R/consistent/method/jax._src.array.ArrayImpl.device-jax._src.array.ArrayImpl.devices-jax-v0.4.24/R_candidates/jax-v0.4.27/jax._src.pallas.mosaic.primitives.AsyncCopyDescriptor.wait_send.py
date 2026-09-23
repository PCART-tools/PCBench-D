  def wait_send(self):
    if not self.is_remote:
      raise ValueError("Cannot `wait_send` on a local copy.")
    wait_args, tree = tree_util.tree_flatten(
        (self.src_sem, self.src_sem_indexers, self.src_ref, self.src_indexers)
    )
    dma_wait_p.bind(
        *wait_args, tree=tree, device_id_type=self.device_id_type
    )
