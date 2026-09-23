def create_temp_files_for_serving(tmp_dir, file_count, file_size,
                                  file_url_template):
    furl_local_file = os.path.join(tmp_dir, "urls_list")
    with open(furl_local_file, 'w') as fsum:
        for i in range(0, file_count):
            f = os.path.join(tmp_dir, "webfile_test_{num}.data".format(num=i))

            write_chunk = 1024 * 1024 * 16
            rmn_size = file_size
            while rmn_size > 0:
                with open(f, 'ab+') as fout:
                    fout.write(os.urandom(min(rmn_size, write_chunk)))
                rmn_size = rmn_size - min(rmn_size, write_chunk)

            fsum.write(file_url_template.format(num=i))
