def CDNA2OrLater():
    if TEST_WITH_ROCM:
        gcn_arch_name = torch.cuda.get_device_properties('cuda').gcnArchName
        return any(arch in gcn_arch_name for arch in {"gfx90a", "gfx942"})
    return False
