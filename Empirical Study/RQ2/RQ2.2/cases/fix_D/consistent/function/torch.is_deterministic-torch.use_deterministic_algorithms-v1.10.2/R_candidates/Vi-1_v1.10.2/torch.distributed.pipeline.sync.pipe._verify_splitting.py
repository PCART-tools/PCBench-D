def _verify_splitting(
    module: nn.Sequential, partitions: List[nn.Sequential], devices: List[torch.device]
) -> None:
    num_parameters = len(list(module.parameters()))
    num_child_parameters = sum(len(list(child.parameters())) for child in module.children())
    if num_parameters == num_child_parameters:
        return

    for i in range(len(partitions)):
        for j in range(i + 1, len(partitions)):
            parti = partitions[i]
            partj = partitions[j]
            if devices[i] == devices[j]:
                continue
            for p in parti.parameters():
                for q in partj.parameters():
                    if p is q:
                        raise ValueError("module with duplicate parameters on distinct devices is not supported")
