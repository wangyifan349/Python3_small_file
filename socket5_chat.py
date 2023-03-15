#客户端和服务器端功能。其中，接收消息线程在对方断开连接后会自动将服务器端转换为等待新客户端连接的状态。
import socket
import threading
import sys
import time
# 客户端和服务器通用的Socket5通信类
class Socket5:
    def __init__(self):
        self.sock = None       # 套接字对象
        self.conn = None       # 服务器端连接对象
        self.role = None       # 角色，服务器或客户端
        self.connected = False # 连接状态
    # 初始化服务器
    def init_server(self, port):
        try:
            # 创建套接字对象
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置套接字选项
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 绑定端口
            self.sock.bind(('0.0.0.0', port))
            # 监听连接
            self.sock.listen(1)
            self.role = 'server'
            print('等待客户端连接...')
        except Exception as e:
            print('初始化服务器失败:', e)
            sys.exit(1)
    # 初始化客户端
    def init_client(self, ip, port):
        try:
            # 创建套接字对象
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接到服务器
            self.sock.connect((ip, port))
            self.role = 'client'
            self.connected = True
            print('连接到服务器...')
        except Exception as e:
            print('初始化客户端失败:', e)
            sys.exit(1)
    # 等待客户端连接
    def wait_for_client(self):
        try:
            # 接受客户端连接
            self.conn, addr = self.sock.accept()
            self.connected = True
            print(f'客户端 {addr} 已连接')
        except Exception as e:
            print('等待客户端连接失败:', e)
            sys.exit(1)
    # 发送消息
    def send_msg(self, msg):
        try:
            # 根据角色发送消息
            if self.role == 'server':
                self.conn.sendall(msg.encode('utf-8'))
            else:
                self.sock.sendall(msg.encode('utf-8'))
        except Exception as e:
            print('发送消息失败:', e)
    # 接收消息
    def recv_msg(self):
        try:
            # 根据角色接收消息
            if self.role == 'server':
                return self.conn.recv(1024).decode('utf-8')
            else:
                return self.sock.recv(1024).decode('utf-8')
        except Exception as e:
            print('接收消息失败:', e)
            return None
    # 关闭连接
    def close(self):
        if self.connected:
            # 根据角色关闭连接
            if self.role == 'server':
                self.conn.close()
            else:
                self.sock.close()
            self.connected = False
# 发送消息线程
def send_thread(s5):
    while True:
        msg = input('请输入消息: ')
        if msg == 'exit':
            s5.close()
            sys.exit(0)
        s5.send_msg(msg)
# 接收消息线程
def recv_thread(s5):
    while True:
        msg = s5.recv_msg()
        if not msg:
            print('对方已断开连接，等待新的客户端连接...')
            s5.close()
            s5.wait_for_client()
            continue
        print(f'对方: {msg}')
def main():
    ip, port = '127.0.0.1', 5555
    # 创建Socket5实例
    s5 = Socket5()
    # 根据用户输入选择服务器或客户端模式
    mode = input('请输入模式（server/client）：')
    if mode == 'server':
        s5.init_server(port)
        s5.wait_for_client()
    elif mode == 'client':
        s5.init_client(ip, port)
    else:
        print('输入错误，请重新运行程序并输入正确的模式。')
        sys.exit(1)
    # 创建发送和接收消息的线程
    send_t = threading.Thread(target=send_thread, args=(s5,))
    recv_t = threading.Thread(target=recv_thread, args=(s5,))
    # 启动线程
    send_t.start()
    recv_t.start()
    # 等待线程结束
    send_t.join()
    recv_t.join()
if __name__ == '__main__':
    main()
            
            
           
