
from cryptography import x509
import datetime
from cryptography.hazmat.primitives import hashes, serialization
import win32crypt
import Credentials as secu

class CAsigning:

    @staticmethod
    def addtotrust():

        CERT_STORE_PROV_SYSTEM = 0x0000000A
        CERT_STORE_OPEN_EXISTING_FLAG = 0x00004000
        CRYPT_STRING_BASE64HEADER = 0x00000000
        CERT_SYSTEM_STORE_CURRENT_USER_ACCOUNT = 1 << 16
        X509_ASN_ENCODING = 0x00000001
        CERT_STORE_ADD_REPLACE_EXISTING = 3
        CERT_CLOSE_STORE_FORCE_FLAG = 0x00000001

        cert_str = bytes.fromhex(secu.main_cert).decode()

        cert_byte = win32crypt.CryptStringToBinary(cert_str, CRYPT_STRING_BASE64HEADER)[0]
        store = win32crypt.CertOpenStore(CERT_STORE_PROV_SYSTEM, 0, None,
                                         CERT_SYSTEM_STORE_CURRENT_USER_ACCOUNT | CERT_STORE_OPEN_EXISTING_FLAG, "ROOT")

        try:
            store.CertAddEncodedCertificateToStore(X509_ASN_ENCODING, cert_byte, CERT_STORE_ADD_REPLACE_EXISTING)
        finally:
            store.CertCloseStore(CERT_CLOSE_STORE_FORCE_FLAG)

    @staticmethod
    def createsig_cert(csr_txt:str):

        CA_cert = x509.load_pem_x509_certificate(bytes.fromhex(secu.main_cert).decode().encode())
        CA_private = serialization.load_pem_private_key(bytes.fromhex(secu.main_priv).decode().encode(), password=None)
        req = x509.load_pem_x509_csr(csr_txt.encode())
        CSR_public = req.public_key()

        cert = x509.CertificateBuilder().subject_name(
               req.subject
        ).issuer_name(
               CA_cert.subject
        ).public_key(
               CSR_public
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).serial_number(
            x509.random_serial_number()
        ).sign(CA_private,hashes.SHA256())

        return cert.public_bytes(serialization.Encoding.PEM).decode()
