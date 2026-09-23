  def wait_recv(self):
    wait_args, tree = tree_util.tree_flatten(
        (self.dst_sem, self.dst_sem_indexers, self.dst_ref, self.dst_indexers)
    )
    dma_wait_p.bind(
        *wait_args, tree=tree, device_id_type=self.device_id_type
    )
