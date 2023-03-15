##########需要wireshark先抓包。

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP, UDP

def analyze_pcap(pcap_file, output_file):
    packets = rdpcap(pcap_file)  # 读取PCAP文件

    with open(output_file, 'w') as f:
        for packet in packets:  # 遍历所有数据包
            ip_layer = packet.getlayer(IP)  # 获取IP层

            # 如果数据包包含HTTP请求层且目标端口是80
            if packet.haslayer(HTTPRequest) and packet.getlayer(TCP).dport == 80:
                http_layer = packet.getlayer(HTTPRequest)  # 获取HTTP请求层
                complete_url = http_layer.Host + http_layer.Path  # 获取完整URL
                timestamp = packet.time  # 获取时间戳
                f.write(f"HTTP\t{timestamp}\t{complete_url}\t{ip_layer.dst}\n")  # 写入文件

            # 如果数据包包含DNS层且目标端口是53
            if packet.haslayer(DNS) and packet.getlayer(UDP).dport == 53:
                dns_layer = packet.getlayer(DNS)  # 获取DNS层
                dns_query = dns_layer.getlayer(DNSQR).qname.decode("utf-8")  # 获取DNS查询
                timestamp = packet.time  # 获取时间戳
                f.write(f"DNS\t{timestamp}\t{dns_query}\t{ip_layer.dst}\n")  # 写入文件
            if tcp_layer.dport == 443:  # 如果目标端口是443,注意这部分可能无法用，443端口https是加密流量。
                    http_layer = packet.getlayer(HTTPRequest)  # 获取HTTP请求层
                    complete_url = http_layer.Host + http_layer.Path  # 获取完整URL
                    timestamp = packet.time  # 获取时间戳
                    f.write(f"{timestamp}\t{complete_url}\t{ip_layer.dst}\n")  # 写入文件

#处理HTTP请求（端口80）和DNS查询（端口53），并将结果写入同一个输出文件中。输出文件的每一行将包含请求类型（HTTP或DNS）、时间戳、URL或DNS查询以及目标IP地址。
if __name__ == '__main__':
    pcap_file = input("请输入PCAP文件路径：")
    output_file = input("请输入输出文件名：")
    analyze_pcap(pcap_file, output_file)
