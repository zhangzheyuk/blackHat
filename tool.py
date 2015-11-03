#coding=utf-8
__author__ = 'zzy'

import sys
import socket
import getopt
import threading
import subprocess

# globe variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
prot = 0


def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen             - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command     - initialize a command shell"
    print "-u --upload=destination - upon receiving connection upload a file and write to [destination]"

    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1 -p 5555 -1 -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -1 -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -1 -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #连接到目标主机
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:

            # 现在等待数据回传
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response

            # 等待更多的输入
            buffer = raw_input("")
            buffer += "\n"

            # 发送出去
            client.send(buffer)

    except:

        print "[*] Exception! Exiting."
        # close
        client.close()





def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()


    #读取命令行选项
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", \
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])

        print "[*opt] =" + opts
        print "[*args] =" + args

    except getopt.GetoptError as err:
        print str(err)
        usage()


    for o,a in opts:
        if o in ("-h", "--help"):
            usage()

        elif o in ("-l", "--listen"):
            listen = True

        elif o in ("-e", "--execute"):
            execute = True

        elif o in ("-c", "--command"):
            command = True

        elif o in ("-u", "--upload"):
            upload_destination = a

        elif o in ("-t", "--target"):
            target = a

        elif o in ("-p", "--port"):
            port = int(a)

        else:
            assert False, "Unhandled Option"


# 监听还是从stdin发送数据？
    if not listen and len(target) and len(port) > 0:

        # 从命令行读取数据
        # 阻塞， 不发送数据时输入ctrl+d

        buffer = sys.stdin.read()

    # 开始监听并准备上传文件，执行命令
    # 设置一个反向shell
    # 取决于上面的命令行选项
    if listen:
        server_loop()


main()
