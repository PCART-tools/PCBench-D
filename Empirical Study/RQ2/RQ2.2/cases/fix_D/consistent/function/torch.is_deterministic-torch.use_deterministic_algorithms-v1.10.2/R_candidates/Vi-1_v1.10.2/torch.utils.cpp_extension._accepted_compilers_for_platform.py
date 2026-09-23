def _accepted_compilers_for_platform() -> List[str]:
    # gnu-c++ and gnu-cc are the conda gcc compilers
    return ['clang++', 'clang'] if sys.platform.startswith('darwin') else ['g++', 'gcc', 'gnu-c++', 'gnu-cc']
