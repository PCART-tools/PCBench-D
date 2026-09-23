def get_platform(arch_variant_name):
    return "SIMULATOR" if arch_variant_name == "x86_64" else "OS"
