def _get_package(zip_reader):
    if zip_reader not in _raw_packages:
        _raw_packages[zip_reader] = PackageImporter(zip_reader)
    return _raw_packages[zip_reader]
