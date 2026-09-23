def create_req(path, C, ST, L, O, key):
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, C),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, ST),
        x509.NameAttribute(NameOID.LOCALITY_NAME, L),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, O),
    ])).sign(key, hashes.SHA256())
    with open(path, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
    return csr
