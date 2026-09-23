    def __getitem__(self, t):
        return type('JsonWrapperValue', (JsonWrapper, ), {'inner_type': t})
