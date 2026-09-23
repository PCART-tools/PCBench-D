def main():
    args = parse_args()

    dist.init_process_group(
        backend="gloo",
        init_method=args.init_method,
        world_size=args.world_size,
        rank=args.rank,
    )

    rank = dist.get_rank()
    world_size = dist.get_world_size()

    # one hot (by rank) tensor of size world_size
    # example:
    # rank 0, world_size 4 => [1, 0, 0, 0]
    # rank 1, world_size 4 => [0, 1, 0, 0]
    # ...
    t = F.one_hot(torch.tensor(rank), num_classes=world_size)

    # after all_reduce t = tensor.ones(size=world_size)
    dist.all_reduce(t)

    # adding all elements in t should equal world_size
    derived_world_size = torch.sum(t).item()
    if derived_world_size != world_size:
        raise RuntimeError(
            f"Wrong world size derived. Expected: {world_size}, Got: {derived_world_size}"
        )

    print("Done")
