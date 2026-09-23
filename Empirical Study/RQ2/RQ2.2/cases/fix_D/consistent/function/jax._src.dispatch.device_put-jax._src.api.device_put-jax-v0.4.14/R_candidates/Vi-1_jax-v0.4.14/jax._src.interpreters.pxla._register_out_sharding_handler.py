def _register_out_sharding_handler(
    sharding_cls: type[_ShardingT],
    handler: Callable[[xc.OpSharding, _ShardingT], _ShardingT],
) -> None:
  _orig_out_sharding_handlers[sharding_cls] = handler
