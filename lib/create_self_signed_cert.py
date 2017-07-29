
from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
from os.path import exists, join

CERT_FILE = "myapp.crt"
KEY_FILE = "myapp.key"

def create_self_signed_cert(cert_dir="cert", data={}, certFile="myapp.crt", keyFile="myapp.key"):
    """
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """
    if not exists(join(cert_dir, CERT_FILE)) \
            or not exists(join(cert_dir, KEY_FILE)):

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        if not data:
            data = {"C" : "US",
                    "ST" : "Minnisota",
                    "L" : "Minnetonka",
                    "O" : "my company",
                    "OU" : "my organization",
                    "CN" : gethostname(),
                    "Serial Number" : 1000,
                    "not before" : 0,
                    "not after" : 5*365*24*60*60, # 5 years
                    "pubkey" : k,
                    "algorithm" : "sha256" }

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = data["C"]
        cert.get_subject().ST = data["ST"]
        cert.get_subject().L = data["L"]
        cert.get_subject().O = data["O"]
        cert.get_subject().OU = data["OU"]
        cert.get_subject().CN = data["CN"]
        cert.set_serial_number(data["Serial Number"])
        cert.gmtime_adj_notBefore(data["not before"])
        cert.gmtime_adj_notAfter(data["not after"])
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(data["pubkey"])
        cert.sign(k, data["algorithm"])

        open(join(cert_dir, CERT_FILE), "wt").write(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(
            crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


