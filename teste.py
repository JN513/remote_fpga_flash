import requests

file = open("spi.fs", "r")

files = {"file": file}

r = requests.post("http://10.68.10.71:8000/flash_9k",
                  files=files)

print(r.text)
