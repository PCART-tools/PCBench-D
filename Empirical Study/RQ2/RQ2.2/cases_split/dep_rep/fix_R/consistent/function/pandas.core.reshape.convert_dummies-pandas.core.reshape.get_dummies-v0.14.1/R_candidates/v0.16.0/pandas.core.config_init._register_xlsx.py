    def _register_xlsx(engine, other):
        cf.register_option('xlsx.writer', engine,
                           writer_engine_doc.format(ext='xlsx',
                                                    default=engine,
                                                    others=", '%s'" % other),
                           validator=str)
