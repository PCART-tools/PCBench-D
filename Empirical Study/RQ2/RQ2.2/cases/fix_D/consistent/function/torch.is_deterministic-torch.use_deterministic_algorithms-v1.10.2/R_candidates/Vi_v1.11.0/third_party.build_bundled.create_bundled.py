def create_bundled(d, outstream):
    """Write the information to an open outstream"""
    collected = collect_license(d)
    sorted_keys = sorted(collected.keys())
    outstream.write('The Pytorch repository and source distributions bundle '
                    'several libraries that are \n')
    outstream.write('compatibly licensed.  We list these here.\n\n')
    for k in sorted_keys:
        c = collected[k]
        files = ',\n     '.join(c['Files'])
        license_file = ',\n     '.join(c['License_file'])
        outstream.write(f"Name: {c['Name']}\n")
        outstream.write(f"License: {c['License']}\n")
        outstream.write(f"Files: {files}\n")
        outstream.write('  For details, see ')
        outstream.write(license_file)
        outstream.write('\n\n') 
