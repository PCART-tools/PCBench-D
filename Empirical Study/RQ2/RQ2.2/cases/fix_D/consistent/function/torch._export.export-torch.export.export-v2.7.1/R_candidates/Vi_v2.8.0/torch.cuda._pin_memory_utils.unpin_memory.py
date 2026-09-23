def unpin_memory(data_ptr: int) -> None:
    succ = int(torch.cuda.cudart().cudaHostUnregister(data_ptr))
    assert succ == 0, f"Unpinning shared memory failed with error-code: {succ}"
