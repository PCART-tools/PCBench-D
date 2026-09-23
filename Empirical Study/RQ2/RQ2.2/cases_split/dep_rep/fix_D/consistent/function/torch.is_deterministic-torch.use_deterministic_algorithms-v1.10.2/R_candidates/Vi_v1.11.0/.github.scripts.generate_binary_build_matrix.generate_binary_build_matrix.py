def generate_binary_build_matrix(os: str) -> List[Dict[str, str]]:
    return {
        "linux": [
            *generate_conda_matrix(os),
            *generate_libtorch_matrix(os, abi_version=PRE_CXX11_ABI),
            *generate_libtorch_matrix(os, abi_version=CXX11_ABI),
            *generate_wheels_matrix(os),
        ]
    }[os]
