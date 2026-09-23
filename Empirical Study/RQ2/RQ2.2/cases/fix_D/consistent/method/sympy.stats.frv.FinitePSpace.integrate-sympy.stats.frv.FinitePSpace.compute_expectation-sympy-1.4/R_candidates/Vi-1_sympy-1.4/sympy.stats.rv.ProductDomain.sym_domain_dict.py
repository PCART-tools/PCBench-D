    @property
    def sym_domain_dict(self):
        return dict((symbol, domain) for domain in self.domains
                                     for symbol in domain.symbols)
