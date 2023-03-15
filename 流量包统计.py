from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.http import HTTPRequest
from scapy.layers.inet import IP, TCP, UDP

def analyze_pcap(pcap_file, output_file):
    try:
        packets = rdpcap(pcap_file)  # 读取PCAP文件
    except FileNotFoundError:
        print(f"无法找到PCAP文件：{pcap_file}")
        return

    with open(output_file, 'w') as f:
        for packet in packets:  # 遍历所有数据包
            ip_layer = packet.getlayer(IP)  # 获取IP层
            if not ip_layer:
                continue

            tcp_layer = packet.getlayer(TCP)
            udp_layer = packet.getlayer(UDP)

            # 如果数据包包含HTTP请求层且目标端口是80
            if packet.haslayer(HTTPRequest) and tcp_layer and tcp_layer.dport == 80:
                http_layer = packet.getlayer(HTTPRequest)  # 获取HTTP请求层
                complete_url = http_layer.Host + http_layer.Path  # 获取完整URL
                timestamp = packet.time  # 获取时间戳
                f.write(f"HTTP\t{timestamp}\t{complete_url}\t{ip_layer.dst}\n")  # 写入文件

            # 如果数据包包含DNS层且目标端口是53
            if packet.haslayer(DNS) and udp_layer and udp_layer.dport == 53:
                dns_layer = packet.getlayer(DNS)  # 获取DNS层
                dns_query = dns_layer.getlayer(DNSQR).qname.decode("utf-8")  # 获取DNS查询
                timestamp = packet.time  # 获取时间戳
                f.write(f"DNS\t{timestamp}\t{dns_query}\t{ip_layer.dst}\n")  # 写入文件

            # 如果目标端口是443
            if tcp_layer and tcp_layer.dport == 443:#由于HTTPS流量（端口443）是加密的，我们可能无法获取完整的URL
                try:
                    http_layer = packet.getlayer(HTTPRequest)  # 获取HTTP请求层
                    complete_url = http_layer.Host + http_layer.Path  # 获取完整URL
                    timestamp = packet.time  # 获取时间戳
                    f.write(f"{timestamp}\t{complete_url}\t{ip_layer.dst}\n")  # 写入文件
                except AttributeError:#在这种情况下，我们会跳过这个数据包并继续处理下一个数据包。
                    pass

if __name__ == '__main__':
    pcap_file = input("请输入PCAP文件路径：")
    output_file = input("请输入输出文件名：")
    analyze_pcap(pcap_file, output_file)
