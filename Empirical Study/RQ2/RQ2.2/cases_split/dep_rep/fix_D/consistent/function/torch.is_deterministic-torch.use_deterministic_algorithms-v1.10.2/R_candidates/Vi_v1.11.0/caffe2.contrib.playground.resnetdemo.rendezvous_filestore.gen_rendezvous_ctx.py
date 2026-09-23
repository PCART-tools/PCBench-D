def gen_rendezvous_ctx(self, model, dataset, is_train):
    if self.opts['distributed']['num_shards'] < 2:
        return None
    # have issue when try to set this up on more shards
    workspace.RunOperatorOnce(
        core.CreateOperator(
            "FileStoreHandlerCreate", [], ["store_handler"],
            path="/tmp",
            prefix="epoch.{}".format(self.epoch),
        )
    )

    rendezvous = dict(
        kv_handler="store_handler",
        shard_id=self.shard_id,
        num_shards=self.opts['distributed']['num_shards'],
        engine="GLOO",
        # transport=args.distributed_transport,
        transport="tcp",
        # interface=interfaces[0],
        interface=[],
        exit_nets=None) if is_train else None
    return rendezvous
