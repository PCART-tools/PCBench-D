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
