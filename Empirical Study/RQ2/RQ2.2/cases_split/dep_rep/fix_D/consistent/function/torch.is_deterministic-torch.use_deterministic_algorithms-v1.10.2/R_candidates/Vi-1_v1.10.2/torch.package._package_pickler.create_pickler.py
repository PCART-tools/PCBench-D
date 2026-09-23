def create_pickler(data_buf, importer):
    if importer is sys_importer:
        # if we are using the normal import library system, then
        # we can use the C implementation of pickle which is faster
        return Pickler(data_buf, protocol=3)
    else:
        return PackagePickler(importer, data_buf, protocol=3)
