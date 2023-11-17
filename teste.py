import requests

file = open("spi.fs", "r")

files = {"file": file}

r = requests.post("http://localhost:8000/flash_9k",
                  files=files)

print(r.text)
