  def m_type_str(self, api_name):
    return (f'{self.source_info and self.source_info.eqn_name} inside {api_name}'
            if self.m_type == MismatchType.SHARDING_INSIDE_COMPUTATION else self.m_type)
