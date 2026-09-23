@contextmanager
def spawn_workers(devices: List[torch.device],) -> Generator[Tuple[List[InQueue], List[OutQueue]], None, None]:
    try:
        (in_queues, out_queues) = create_workers(devices)
        yield (in_queues, out_queues)
    finally:
        pass
