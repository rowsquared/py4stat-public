import requests
import requests.auth
import sys
import os

import dotenv

dotenv.load_dotenv()

site = "https://learning.rowsquared.org/mod/book/view.php?id=6"
user = os.getenv("USER")
password = os.getenv("PASSWORD")

auth = requests.auth.HTTPBasicAuth(user, password)
r = requests.request(
    "GET",
    url=site,
    auth=auth

)

print(r.text)