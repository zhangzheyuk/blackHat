__author__ = 'zzy'
# coding="utf-8"
import socket

target_host = "10.10.12.62"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

client.send("GET /up.html HTTP/1.1\r\nHost: 10.10.12.62\r\n\r\n")

response = client.recv(4096)

print response