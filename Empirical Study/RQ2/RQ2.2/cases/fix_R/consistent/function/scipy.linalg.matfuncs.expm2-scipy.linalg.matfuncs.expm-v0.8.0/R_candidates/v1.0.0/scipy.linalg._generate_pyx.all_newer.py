def all_newer(src_files, dst_files):
    from distutils.dep_util import newer
    return all(os.path.exists(dst) and newer(dst, src)
               for dst in dst_files for src in src_files)
