from oscrypto import asymmetric
from csrbuilder import CSRBuilder, pem_armor_csr
from certbuilder import CertificateBuilder, pem_armor_certificate
from cryptography import x509
from cryptography.x509.oid import NameOID


class certs:
    csr_txt = ""; csr_valid_test = ""
    def CSR_and_Private_Generate(self,algo:str,size:int,folder_path:str,
                                 password:str,cn:str,country:str,org:str,mail_id:str,sub_alt:str,
                                 gen_key:bool,gen_csr:bool):

        public_key, private_key = asymmetric.generate_pair(algo, bit_size=size)

        if gen_key is True:
            with open(folder_path+"\\private_key.key", 'wb') as f:
                if password == "":
                    f.write(asymmetric.dump_private_key(private_key, passphrase=None))
                else:
                    f.write(asymmetric.dump_private_key(private_key, passphrase=password))
        else: pass
        builder = CSRBuilder(
            {
                'country_name': country,
                'organization_name': org,
                'common_name': cn,
                'email_address': mail_id
            },
            public_key
        )

        # Add subjectAltName domains
        builder.subject_alt_domains = sub_alt.split(";")
        request = builder.build(private_key)

        if gen_csr is True:
            with open(folder_path+"\\csr_file.pem", 'wb') as f:
                f.write(pem_armor_csr(request))

        txt = str(pem_armor_csr(request))
        certs.csr_txt += txt[1:].replace(txt[len(txt)-1],"").replace("\\n","")

    def self_signed_cert(self,cn:str,country:str,org:str,mail_id:str,alt_names:str,file_save:str,algo:str):
        public_key, private_key = asymmetric.generate_pair(algo,2048)
        builder1 = CertificateBuilder(
            {
                'country_name': country,
                'organization_name': org,
                'common_name': cn,
                'email_address': mail_id
            },
            public_key
        )
        builder1.subject_alt_domains = alt_names.split(";")
        builder1.extended_key_usage = {"1.3.6.1.5.5.7.3.1","1.3.6.1.5.5.7.3.2"}
        builder1.self_signed = True
        certificate = builder1.build(private_key)

        with open(file_save,'wb') as f:
            f.write(pem_armor_certificate(certificate))

    def csr_valid(self,csr_content:str):

        # coloring function
        def colored(r, g, b, text):
            return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

        request = x509.load_pem_x509_csr(csr_content.encode("utf-8"))
        valid = True; result_string = ""
        result_string += "Common Name : "
        for name in request.subject.get_attributes_for_oid(NameOID.COMMON_NAME):
            result_string += name.value
            if name.value[-4:] not in [".com", ".org", ".net"]:
                valid = False
                result_string += "this Common name is invalid"
            result_string += "\n\n"
        result_string += "Country Code : "
        for name in request.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME):
            result_string += name.value
            if len(name.value) > 2:
                valid = False
                result_string += "invalid country code"
            result_string += "\n\n"
        result_string += "mail id : "
        for name in request.subject.get_attributes_for_oid(NameOID.EMAIL_ADDRESS):
            result_string += str(name.value)
            if (str(name.value) is not None) and (name.value[-10:] != "@gmail.com"):
                valid = False
                result_string += "invalid mail address"
        result_string += "\n\n"
        result_string += "SAN are : "
        for i in request.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(
                x509.DNSName):
            result_string += i+"  "
        result_string += "\n\n"
        valid = request.is_signature_valid; result_string += "Signature is : "
        if valid:
            result_string += "Valid"
        else:
            result_string += colored(255, 0, 0, "invalid")
        result_string += "\n\n"
        algo = str(request.signature_algorithm_oid)[-25:-2]
        result_string += "Algorithm used : " + algo + "\n\n"
        key_size = request.public_key().key_size
        result_string += "Key Size : " + str(key_size) + "\n\n\n"
        if valid is True:
            certs.csr_valid_test = "Valid"
        else:
            certs.csr_valid_test = "Invalid"

        return result_string

    def make_CA(self):
        root_ca_public_key, root_ca_private_key = asymmetric.generate_pair('rsa', bit_size=2048)

        with open('D:\\Lasya files\\root_ca.key', 'wb') as f:
            f.write(asymmetric.dump_private_key(root_ca_private_key, None))

        builder = CertificateBuilder(
            {
                'country_name': 'IN',
                'state_or_province_name': 'Andhra',
                'locality_name': 'Swarna_village',
                'organization_name': 'Surya.Inc',
                'common_name': 'SURYA TEJA NEERUKATTU',
                'email_address': 'neerukattusurya1@gmail.com'
            },
            root_ca_public_key
        )
        builder.self_signed = True
        builder.ca = True
        root_ca_certificate = builder.build(root_ca_private_key)

        with open('D:\\Lasya files\\root_ca.crt', 'wb') as f:
            f.write(pem_armor_certificate(root_ca_certificate))

b = certs()
