from socket import *
import sys
from time import sleep
#具体功能
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd=sockfd

    def do_list(self):
        self.sockfd.send(b"L")  #发送请求
        #等待回复
        data=self.sockfd.recv(128).decode()
        #ok表示请求成功
        if data=="OK":
            data=self.sockfd.recv(4096)
            print(data.decode())

        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("谢谢使用")

    def do_get(self,filename):
        #发送请求
        self.sockfd.send(("G "+filename).encode())
        #等待回复
        data=self.sockfd.recv(128).decode()
        if data=="OK":
            fd=open(filename,"wb")
            #将接受内容写入文件
            while True:
                data=self.sockfd.recv(1024)
                if data==b"##":
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)


    def do_put(self,filename):
        try:
            f=open(filename,"rb")
        except Exception:
            print("没有该文件")
            return

        #发送请求
        filename=filename.split("/")[-1]
        self.sockfd.send(("P "+filename).encode())
        #等待回复
        data=self.sockfd.recv(128).decode()
        if data=="OK":
            while True:
                data=f.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)









def request(sockfd):
    ftp=FtpClient(sockfd)

    while True:
        print("\n===============命令提示====================")
        print("************list************")
        print("************get file************")
        print("************put file************")
        print("************quit************")
        print("===============命令提示====================")

        cmd=input("输入命令:")
        if cmd.strip()=="list":
            ftp.do_list()
        elif cmd.strip()=="quit":
            ftp.do_quit()
        elif cmd[:3]=="get":
            filename=cmd.strip().split(" ")[-1]
            ftp.do_get(filename)
        elif cmd[:3]=="put":
            filename=cmd.strip().split(" ")[-1]
            ftp.do_put(filename)






#网络连接
def main():
    #服务器地址
    ADDR=("127.0.0.1",8080)
    sockfd=socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        print("连接服务器失败")
        return
    else:
        print("""*********************
        Data File Image
        """)
        cls=input('请输入文件种类:')
        if cls not in ["Data","File","Image"]:
            print("Sorry input Error!!")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)


if __name__ == '__main__':
    main()


