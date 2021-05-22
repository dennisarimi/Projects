import struct

class IP_Header:
    ip_header_len = None #<type 'int'>
    total_len = None    #<type 'int'>
    identification = None
    flags = None
    frag_offset = None
    ttl = None
    protocol = None
    src_ip = None #<type 'str'>
    dst_ip = None #<type 'str'>
    
    
    def __init__(self):
        self.ip_header_len = 0
        self.total_len = 0
        self.identification = 0
        self.flags = 0
        self.frag_offset = 0
        self.ttl = 0
        self.protocol = 0
        self.src_ip = None
        self.dst_ip = None
    
    def header_len_set(self,length):
        self.ip_header_len = length
    
    def total_len_set(self, length):
        self.total_len = length
    
    def set_flags(self, value):
        self.flags = value

    def set_frag_offset(self, value):
        self.frag_offset = value 
    
    def ip_set(self,src_ip,dst_ip):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
    
    def get_header_len(self,value):
        result = struct.unpack('B', value)[0]
        length = (result & 15)*4
        self.header_len_set(length)

    def get_total_len(self,buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        length = num1+num2+num3+num4
        self.total_len_set(length)
    
    def get_identification(self,buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        value = num1+num2+num3+num4
        self.identification = value
    
    def get_flags(self, buffer):
        result = struct.unpack("B", buffer)[0]
        value = result >> 5
        self.set_flags(value)
    
    def get_frag_offset(self, buffer):
        result = struct.unpack('BB', buffer)[1]
        fragment_offset = (result * 8)
        self.set_frag_offset(fragment_offset)
    
    def get_ttl(self, buffer):
        value = struct.unpack('B', buffer)[0]
        self.ttl = value
    
    def get_protocol(self, buffer):
        value = struct.unpack('B', buffer)[0]
        self.protocol = value  
        
    def get_IP(self,buffer1,buffer2):
        src_addr = struct.unpack('BBBB',buffer1)
        dst_addr = struct.unpack('BBBB',buffer2)
        s_ip = str(src_addr[0])+'.'+str(src_addr[1])+'.'+str(src_addr[2])+'.'+str(src_addr[3])
        d_ip = str(dst_addr[0])+'.'+str(dst_addr[1])+'.'+str(dst_addr[2])+'.'+str(dst_addr[3])
        self.ip_set(s_ip, d_ip)
 
class TCP_Header:
    src_port = 0
    dst_port = 0
    seq_num = 0
    ack_num = 0
    data_offset = 0
    flags = {}
    window_size =0
    checksum = 0
    ugp = 0
    
    def __init__(self):
        self.src_port = 0
        self.dst_port = 0
        self.seq_num = 0
        self.ack_num = 0
        self.data_offset = 0
        self.flags = {}
        self.window_size =0
        self.checksum = 0
        self.ugp = 0
    
    def src_port_set(self, src):
        self.src_port = src
        
    def dst_port_set(self,dst):
        self.dst_port = dst
        
    def seq_num_set(self,seq):
        self.seq_num = seq
        
    def ack_num_set(self,ack):
        self.ack_num = ack
        
    def data_offset_set(self,data_offset):
        self.data_offset = data_offset
        
    def flags_set(self,ack, rst, syn, fin):
        self.flags["ACK"] = ack
        self.flags["RST"] = rst
        self.flags["SYN"] = syn
        self.flags["FIN"] = fin
    
    def win_size_set(self,size):
        self.window_size = size
        
    def get_src_port(self,buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.src_port_set(port)
        return None
    
    def get_dst_port(self,buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.dst_port_set(port)
        return None
    
    def get_seq_num(self,buffer):
        seq = struct.unpack(">I",buffer)[0]
        self.seq_num_set(seq)
        return None
    
    def get_ack_num(self,buffer):
        ack = struct.unpack('>I',buffer)[0]
        self.ack_num_set(ack)
        return None
    
    def get_flags(self,buffer):
        value = struct.unpack("B",buffer)[0]
        fin = value & 1
        syn = (value & 2)>>1
        rst = (value & 4)>>2
        ack = (value & 16)>>4
        self.flags_set(ack, rst, syn, fin)
        return None

    def get_window_size(self,buffer1,buffer2):
        buffer = buffer2+buffer1
        size = struct.unpack('H',buffer)[0]
        self.win_size_set(size)
        return None
        
    def get_data_offset(self,buffer):
        value = struct.unpack("B",buffer)[0]
        length = ((value & 240)>>4)*4
        self.data_offset_set(length)
        #print(self.data_offset)
        return None
    
    def relative_seq_num(self,orig_num):
        if(self.seq_num>=orig_num):
            relative_seq = self.seq_num - orig_num
            self.seq_num_set(relative_seq)
        #print(self.seq_num)
        
    def relative_ack_num(self,orig_num):
        if(self.ack_num>=orig_num):
            relative_ack = self.ack_num-orig_num+1
            self.ack_num_set(relative_ack)

class UDP_Header:
    src_port = 0
    dst_port = 0
    udp_hdr_len = 0

    def __init__(self):
        self.src_port = 0
        self.dst_port = 0
        self.udp_hdr_len = 0
    
    def set_src_port(self, value):
        self.src_port = value
    
    def set_dst_port(self, value):
        self.dst_port = value
    
    def set_len(self, value):
        self.udp_hdr_len = value

    def get_src_port(self, buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.set_src_port(port)
    
    def get_dst_port(self, buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.set_dst_port(port)
    
    def get_udp_hdr_len(self, buffer):
        length = struct.unpack('BB', buffer)[0]
        self.set_len(length)

class ICMP_Header():
    icmp_type = 0
    code = 0
    seq_num = 0
    identification = 0
    ttl = 0
    src_port = 0
    dst_port = 0

    def __init__(self):
        self.icmp_type = 0
        self.code = 0
        self.seq_num = 0
        self.identification = 0
        self.ttl = 0
        self.src_port = 0
        self.dst_port = 0
    
    def set_icmp_type(self, value):
        self.icmp_type = value
    
    def set_code(self, value):
        self.code = value
    
    def set_identification(self, value):
        self.identification = value
    
    def set_seq_num(self, value):
        self.seq_num = value
    
    def set_ttl(self, value):
        self.ttl = value
    
    def set_src_port(self, value):
        self.src_port = value
    
    def set_dst_port(self, value):
        self.dst_port = value
    
    def get_icmp_type(self, buffer):
        value = struct.unpack("B", buffer)[0]
        self.set_icmp_type(value)
    
    def get_code(self, buffer):
        value = struct.unpack("B", buffer)[0]
        self.set_code(value)
    
    def get_identification(self, buffer):
        value = struct.unpack("BB", buffer)[0]
        self.set_identification(value)
    
    def get_seq_num(self, buffer):
        value = struct.unpack("H", buffer)[0]
        self.set_seq_num(value)
    
    def get_ttl(self, buffer):
        value = struct.unpack('B', buffer)[0]
        self.set_ttl(value)
    
    def get_src_port(self,buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.set_src_port(port)
    
    def get_dst_port(self, buffer):
        num1 = ((buffer[0]&240)>>4)*16*16*16
        num2 = (buffer[0]&15)*16*16
        num3 = ((buffer[1]&240)>>4)*16
        num4 = (buffer[1]&15)
        port = num1+num2+num3+num4
        self.set_dst_port(port)

class packet():
    
    #pcap_hd_info = None
    IP_header = None
    TCP_header = None
    UDP_header = None
    ICMP_Header = None
    timestamp = 0
    databytes = 0
    packet_No = 0
    RTT_value = 0
    RTT_flag = False
    buffer = None
    
    
    def __init__(self):
        self.IP_header = IP_Header()
        self.TCP_header = TCP_Header()
        self.UDP_header = UDP_Header()
        self.ICMP_header = ICMP_Header()
        self.timestamp = 0
        self.databytes = 0
        self.packet_No = 0
        self.RTT_value = 0.0
        self.RTT_flag = False
        self.buffer = None
        
    def timestamp_set(self,buffer1,buffer2,orig_time):
        seconds = struct.unpack('I',buffer1)[0]
        microseconds = struct.unpack('<I',buffer2)[0]
        self.timestamp = round((seconds + (microseconds * 0.000000001)) - orig_time, 6)
    
    def get_databytes(self, total_len, tcp_hdr_offset, ip_hdr_len):
        self.databytes = total_len - tcp_hdr_offset - ip_hdr_len
        
    def packet_No_set(self,number):
        self.packet_No = number
        
    def get_RTT_value(self, p):
        rtt = round(p.timestamp - self.timestamp, 6)
        self.RTT_value = round(rtt,6)

class connection():
    id = ()
    reverseId = ()
    firstPacket = None
    numDataBytes_src_to_dst = 0
    numberOfSyn = 0
    numberOfFin = 0
    numberOfReset = 0
    numPackets_src_to_dst = 0
    lastFinPacket = None
    numPackets_dst_to_src = 0
    numDataBytes_dst_to_src = 0
    timeDuration = 0
    WindowSizes = []
    connection_packets = []

    def __init__(self):
        self.id = ()
        self.reverseId = ()
        self.firstPacket = packet()
        self.numberOfSyn = 0
        self.numberOfFin = 0
        self.numberOfReset = 0
        self.lastFinPacket = packet()
        self.timeDuration = 0
        self.WindowSizes = []
        self.connection_packets = []
    
    def set_id(self, id):
        self.id = id

    def set_reverseId(self, reverse):
        self.reverseId = reverse

    def set_firstPacket(self, packet):
        self.firstPacket = packet
    
    def set_lastFinPckt(self, packet):
        self.lastFinPacket = packet
    
    def get_timeDuration(self, startTime, endTime):
        self.timeDuration = round(endTime - startTime, 6)
    
    def add_window_size(self, size):
        self.WindowSizes.append(size)
    
    def add_packet(self, packet):
        self.connection_packets.append(packet)
