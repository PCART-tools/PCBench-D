def evaluate_gfx_arch_exact(matching_arch):
    if not torch.cuda.is_available():
        return False
    gcn_arch_name = torch.cuda.get_device_properties('cuda').gcnArchName
    arch = os.environ.get('PYTORCH_DEBUG_FLASH_ATTENTION_GCN_ARCH_OVERRIDE', gcn_arch_name)
    return arch == matching_arch
