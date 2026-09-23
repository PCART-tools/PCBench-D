def reorganize_partitions(partitions: List[Partition]) -> None:
    """Given a list of partitions, reorganzie partiton id,
    its parents and its children for each partition
    """
    # Rearrange partition ids
    for i, partition in enumerate(partitions):
        partition.partition_id = i
    set_parents_and_children(partitions)
    return
