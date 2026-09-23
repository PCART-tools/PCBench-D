def test_memory_repr():
    for power, mem_repr in enumerate(['1.0 bytes', '1.0 KB', '1.0 MB', '1.0 GB']):
        assert memory_repr(1024 ** power) == mem_repr
