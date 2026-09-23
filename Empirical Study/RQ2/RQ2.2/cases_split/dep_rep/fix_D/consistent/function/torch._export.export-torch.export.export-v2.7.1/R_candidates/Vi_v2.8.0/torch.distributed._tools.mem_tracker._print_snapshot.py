def _print_snapshot(snapshot: dict[torch.device, dict[str, int]], units: str) -> None:
    if len(snapshot) == 0:
        print("No memory tracked.")
        return
    divisor = _get_mem_divisor(units)
    for dev, dev_snap in snapshot.items():
        if _rounding_fn(dev_snap[_TOTAL_KEY], divisor, 2) <= 0:
            continue
        print(
            f"Device: {dev}",
            *(
                f"\t{k.value}: {_rounding_fn(v, divisor, 2)} {units}"
                if isinstance(k, _RefType)
                else f"\t{k}: {_rounding_fn(v, divisor, 2)} {units}"
                for k, v in dev_snap.items()
            ),
            sep="\n",
        )
