def get_gpu_info(run_lambda):
    if get_platform() == 'darwin' or (TORCH_AVAILABLE and hasattr(torch.version, 'hip') and torch.version.hip is not None):
        if TORCH_AVAILABLE and torch.cuda.is_available():
            return torch.cuda.get_device_name(None)
        return None
    smi = get_nvidia_smi()
    uuid_regex = re.compile(r' \(UUID: .+?\)')
    rc, out, _ = run_lambda(smi + ' -L')
    if rc != 0:
        return None
    # Anonymize GPUs by removing their UUID
    return re.sub(uuid_regex, '', out)
