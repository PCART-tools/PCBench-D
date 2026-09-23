def contains_collective(snode: BaseSchedulerNode) -> bool:
    from torch._inductor.scheduler import GroupedSchedulerNode

    if isinstance(snode, GroupedSchedulerNode):
        return any(contains_collective(x) for x in snode.snodes)

    return is_collective(snode.node)
