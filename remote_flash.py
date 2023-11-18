#!/usr/bin/python

import os
import sys
import requests
import argparse

current_directory = os.getcwd()


parser = argparse.ArgumentParser(
    prog="color_image.py",
    description="Transforme imagens coloridas em escala de cinza e preto e branco",
    epilog="Text at the bottom of help",
)

parser.add_argument("filename", type=str, help="nome do arquivo a ser gravado")
parser.add_argument(
    "-f",
    "--full_path",
    action="store_true",
    default=False,
    help="O nome do arquivo passado e o path completo ou não",
)

parser.add_argument(
    "-b",
    "--board",
    type=str,
    default="tangnano20k",
    help="Placa a ser gravada",
)

args = parser.parse_args()

file_path = ""

if not args.full_path:
    file_path = current_directory + "/" + args.filename
else:
    file_path = args.filename

file = open(file_path, "r")

if not file:
    file.close()

    sys.exit()

url = "http://10.68.10.71:8000/flash_"
board = ""

if args.board == "tangnano20k":
    board = "20k"
else:
    board = "9k"

print("Log: iniciado request ao servidor.")

r = requests.post(f"{url}{board}", files={"file": file})

print("Log: request concluida.")

request_body = r.json()

if r.status_code != 201:
    if "error" in request_body:
        print(f"Log: message de saida: {request_body['error']}")
    else:
        print(f"Log: arquivo gerado: {request_body['filename']}")
        print(f"Log: message de saida: {request_body['message']}")
        print(f"Log: codigo de execução: {request_body['execution_code']}")

else:
    print(f"Log: arquivo gerado: {request_body['filename']}")
    print("Log: Gravação concluida com sucesso")
    print(f"Log: message de saida: \n{request_body['message']}")
print("Log: processo concluido.")
