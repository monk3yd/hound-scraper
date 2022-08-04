import requests

url = "https://oficinajudicialvirtual.pjud.cl/ADIR_871/apelaciones/modal/causaApelaciones.php"

# --- Case Unique ID ---
encoded_prefix = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
# prefix = {"typ":"JWT","alg":"HS256"}

encoded_rbody = "eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTY1MzI4NjgyNSwiZXhwIjoxNjUzMjg4NjI1LCJkYXRhIjp7InJvbENhdXNhIjoiMzI5OCIsImVyYUNhdXNhIjoiMjAyMiIsImNvZENvcnRlIjoiMjUiLCJjb2RMaWJybyI6IjM0IiwiY29tb2RpbiI6MH19"
# rbody = {
#     "iss": "https:\/\/oficinajudicialvirtual.pjud.cl",
#     "aud": "https:\/\/oficinajudicialvirtual.pjud.cl",
#     "iat": 1653283983,
#     "exp": 1653285783,
#     "data": {
#         "rolCausa": "3298",
#         "eraCausa": "2022",
#         "codCorte": "25",
#         "codLibro": "34",
#         "comodin": 0,
#     },
# }

# TODO Look for valid random string - seems resusable
random_string = "GApTplldWYH4_925EqQkLvNCMaj2esGxk8s1VE0JXIU"

# TODO Look for valid token - seems reusable
# token = "ysHQ11NiZjVKoXcCJCzMy6ltkQxMyiJgwUgAow0XdKhBIT3QeD6c6y03z73AYUvc6qWzvrAS3YZ5VxJuPEp8Mc27Msz5WYqlTbo9fHko8T30vA4jolwF3nAgfXXAKSwDnmeA2Q1EsJXDFcjIFCucU0y_W_s2OrwvhOecjn"

# payload = f"dtaCausa={encoded_prefix}.{encoded_rbody}.{random_string}"
# payload = f"dtaCausa={encoded_prefix}.{encoded_rbody}.{random_string}&tokenCaptcha={token}"
# payload = f"dtaCausa={prefix}.{rbody}.{random_string}&tokenCaptcha={token}"
headers = {
    "Host": "oficinajudicialvirtual.pjud.cl",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    # "Content-Length": "926",
    "Origin": "https://oficinajudicialvirtual.pjud.cl",
    "Connection": "keep-alive",
    "Referer": "https://oficinajudicialvirtual.pjud.cl/indexN.php",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    # "Cookie": "PHPSESSID=a3be543fe833dcc822e280eac807ff26; TS01262d1d=01b485afe585660d4c67014dbae081e834d7645796134f6239f97c548a3073e914ee141716aed35ac89f551655597512bdb5ed472ea4890221933232314529c1b5d4c1d0ba",
}

response = requests.post(url, headers=headers, data=payload)

print(response.text)
