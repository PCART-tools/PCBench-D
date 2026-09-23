@functools.lru_cache
def get_max_num_sms() -> int:
    return torch.cuda.get_device_properties("cuda").multi_processor_count
