def stitch_sources(output_filehandle):
    for f in YAML_SOURCES:
        f.write(output_filehandle)
