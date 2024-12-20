#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import socket
import os
import sys
import struct
import time
import random
import traceback # useful for exception handling
import threading

def setupArgumentParser() -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description='A collection of Network Applications developed for SCC.203.')
        parser.set_defaults(func=ICMPPing, hostname='lancaster.ac.uk')
        subparsers = parser.add_subparsers(help='sub-command help')
        
        parser_p = subparsers.add_parser('ping', aliases=['p'], help='run ping')
        parser_p.set_defaults(timeout=4)
        parser_p.add_argument('hostname', type=str, help='host to ping towards')
        parser_p.add_argument('--count', '-c', nargs='?', type=int,
                              help='number of times to ping the host before stopping')
        parser_p.add_argument('--timeout', '-t', nargs='?',
                              type=int,
                              help='maximum timeout before considering request lost')
        parser_p.set_defaults(func=ICMPPing)

        parser_t = subparsers.add_parser('traceroute', aliases=['t'],
                                         help='run traceroute')
        parser_t.set_defaults(timeout=4, protocol='icmp')
        parser_t.add_argument('hostname', type=str, help='host to traceroute towards')
        parser_t.add_argument('--timeout', '-t', nargs='?', type=int,
                              help='maximum timeout before considering request lost')
        parser_t.add_argument('--protocol', '-p', nargs='?', type=str,
                              help='protocol to send request with (UDP/ICMP)')
        parser_t.set_defaults(func=Traceroute)
        
        parser_pt = subparsers.add_parser('paris-traceroute', aliases=['pt'],
                                         help='run paris-traceroute')
        parser_pt.set_defaults(timeout=4, protocol='icmp')
        parser_pt.add_argument('hostname', type=str, help='host to traceroute towards')
        parser_pt.add_argument('--timeout', '-t', nargs='?', type=int,
                              help='maximum timeout before considering request lost')
        parser_pt.add_argument('--protocol', '-p', nargs='?', type=str,
                              help='protocol to send request with (UDP/ICMP)')
        parser_pt.set_defaults(func=ParisTraceroute)

        parser_w = subparsers.add_parser('web', aliases=['w'], help='run web server')
        parser_w.set_defaults(port=8080)
        parser_w.add_argument('--port', '-p', type=int, nargs='?',
                              help='port number to start web server listening on')
        parser_w.set_defaults(func=WebServer)

        parser_x = subparsers.add_parser('proxy', aliases=['x'], help='run proxy')
        parser_x.set_defaults(port=8000)
        parser_x.add_argument('--port', '-p', type=int, nargs='?',
                              help='port number to start web server listening on')
        parser_x.set_defaults(func=Proxy)

        args = parser.parse_args()
        return args


class NetworkApplication:

    def checksum(self, dataToChecksum: str) -> str:
        csum = 0
        countTo = (len(dataToChecksum) // 2) * 2
        count = 0

        while count < countTo:
            thisVal = dataToChecksum[count+1] * 256 + dataToChecksum[count]
            csum = csum + thisVal
            csum = csum & 0xffffffff
            count = count + 2

        if countTo < len(dataToChecksum):
            csum = csum + dataToChecksum[len(dataToChecksum) - 1]
            csum = csum & 0xffffffff

        csum = (csum >> 16) + (csum & 0xffff)
        csum = csum + (csum >> 16)
        answer = ~csum
        answer = answer & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)

        answer = socket.htons(answer)

        return answer

    def printOneResult(self, destinationAddress: str, packetLength: int, time: float, ttl: int, destinationHostname=''):
        if destinationHostname:
            print("%d bytes from %s (%s): ttl=%d time=%.2f ms" % (packetLength, destinationHostname, destinationAddress, ttl, time))
        else:
            print("%d bytes from %s: ttl=%d time=%.2f ms" % (packetLength, destinationAddress, ttl, time))

    def printAdditionalDetails(self, packetLoss=0.0, minimumDelay=0.0, averageDelay=0.0, maximumDelay=0.0):
        print("%.2f%% packet loss" % (packetLoss))
        if minimumDelay > 0 and averageDelay > 0 and maximumDelay > 0:
            print("rtt min/avg/max = %.2f/%.2f/%.2f ms" % (minimumDelay, averageDelay, maximumDelay))

    def printMultipleResults(self, ttl: int, destinationAddress: str, measurements: list, destinationHostname=''):
        latencies = ''
        noResponse = True
        for rtt in measurements:
            if rtt is not None:
                latencies += str(round(rtt, 3))
                latencies += ' ms  '
                noResponse = False
            else:
                latencies += '* ' 

        if noResponse is False:
            print("%d %s (%s) %s" % (ttl, destinationHostname, destinationAddress, latencies))
        else:
            print("%d %s" % (ttl, latencies))

class ICMPPing(NetworkApplication):

    def receiveOnePing(self, icmpSocket, destinationAddress, ID, timeout):
        # 1. Wait for the socket to receive a reply
        # 2. Once received, record time of receipt, otherwise, handle a timeout
        # 3. Compare the time of receipt to time of sending, producing the total network delay
        # 4. Unpack the packet header for useful information, including the ID
        # 5. Check that the ID matches between the request and reply
        # 6. Return total network delay
    
     
        packet_data, ip =icmpSocket.recvfrom(1024)
        
        header = packet_data[20:28]
        ttl = packet_data[8]
        print(ttl)
        
        type,code,checksum,packetID,seq = struct.unpack("bbHHh",header)
        if packetID == ID:
            print("ID matches")

        return timeout
        pass

    def sendOnePing(self, icmpSocket, destinationAddress, ID):
        # 1. Build ICMP header
        # 2. Checksum ICMP packet using given function
        # 3. Insert checksum into packet
        # 4. Send packet using socket
        # 5. Record time of sending

        checksum=0
        icmp_type=8 #8 is echo request
        seq_num=1
        header = struct.pack("bbHHh",icmp_type,0,checksum,ID,seq_num)
        #data = struct.pack('d', time.time())
        checksum = self.checksum(header)

        header = struct.pack("bbHHh",icmp_type,0,checksum,ID,seq_num)
        packet = header
        sending_time=time.time()
        print(header)
        try:
            icmpSocket.sendto(header,(destinationAddress,1))

        except socket.error as e:
            print("error")

        return time.time()-sending_time
        pass

    def doOnePing(self, destinationAddress, timeout):
        # 1. Create ICMP socket
        icmpsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        # 2. Call sendOnePing function
        id = 10
    
        self.sendOnePing(icmpsocket,destinationAddress,id)
        # 3. Call receiveOnePing function
        self.receiveOnePing(icmpsocket,destinationAddress,id,timeout)
        # 4. Close ICMP socket
        icmpsocket.close()
        # 5. Return total network delay

        return timeout

    def __init__(self, args):
        
        startTime = time.time()
        ip = socket.gethostbyname(args.hostname) #lancaster ip
        self.doOnePing(ip,1)
        print('Ping to: %s...' % (args.hostname))


        # 1. Look up hostname, resolving it to an IP address
        # 2. Call doOnePing function, approximately every second
        # 3. Print out the returned delay (and other relevant details) using the printOneResult method
        self.printOneResult(ip, 50, 20.0, 150) # Example use of printOneResult - complete as appropriate
        # 4. Continue this process until stopped


class Traceroute(NetworkApplication):

    def __init__(self, args):
        # Please ensure you print each result using the printOneResult method!
        print('Traceroute to: %s...' % (args.hostname))
        ip = socket.gethostbyname(args.hostname)
        self.tr(ip)
    
    def tr(self,dest):
        dest_addr = dest
        ttl = 1
        port = 1050
        
        checksum=0
        print("start addr: "+ str(dest)) 

        # do for UDP as well
        
        while True:
            header = struct.pack("bbHHh",8,0,checksum,1,1)
            checksum = self.checksum(header) 
            header = struct.pack("bbHHh",8,0,checksum,1,1)

            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
            
            recv_socket.bind(("", port))
            sys.stdout.write(" %d  " % ttl)

            addr = None
            curr_name = None
            finished = False
            
            while not finished:
                try:
                    newsoc, addr = recv_socket.recvfrom(512)

                    finished = True
                    curr_addr = addr[0]
                    try:
                        curr_name = socket.gethostbyaddr(addr)[0]
                    except socket.error:
                        curr_name = addr
                except socket.error as errmsg:
                    sys.stdout.write("* ")
            
            recv_socket.close()
            if not finished:
                pass



class ParisTraceroute(NetworkApplication):

    packet_loss=0

    def __init__(self, args):
        # Please ensure you print each result using the printOneResult method!
        print('Paris-Traceroute to: %s...' % (args.hostname))
        ip = socket.gethostbyname(args.hostname)

        self.tr(ip)

    def receiveOnePing(self, icmpSocket, destinationAddress, ID, timeout):
        # 1. Wait for the socket to receive a reply
        # 2. Once received, record time of receipt, otherwise, handle a timeout
        # 3. Compare the time of receipt to time of sending, producing the total network delay
        # 4. Unpack the packet header for useful information, including the ID
        # 5. Check that the ID matches between the request and reply
        # 6. Return total network delay
    
        
        try:
            
            packet_data, ip =icmpSocket.recvfrom(1024)
            end_time = time.time()
            

            header = packet_data[20:28]
            ttl = packet_data[8]
            type,code,checksum,packetID,seq = struct.unpack("bbHHh",header)
            
            return end_time
        except socket.timeout:
            
            self.packet_loss+=1
            
            end_time = time.time()
            return end_time
        except socket.error:

            end_time = time.time()
            return end_time
        
        
    def sendOnePing(self, icmpSocket, destinationAddress, ID):
        # 1. Build ICMP header
        # 2. Checksum ICMP packet using given function
        # 3. Insert checksum into packet
        # 4. Send packet using socket
        # 5. Record time of sending

        checksum=0
        icmp_type=8 #8 is echo request
        seq_num=1
        header = struct.pack("bbHHh",icmp_type,0,0,1,1)
        #data = struct.pack('d', time.time())
        checksum = self.checksum(header)

        header = struct.pack("bbHHh",icmp_type,0,checksum,1,1)
        packet = header
        
        
        try:
            icmpSocket.sendto(header,(destinationAddress,1))
            start_time=time.time()
        except socket.error as e:
            print("error")
        
        return start_time
        

    def doOnePing(self, destinationAddress, timeout):
        # 1. Create ICMP socket
        icmpsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        icmpsocket.settimeout(timeout)
        # 2. Call sendOnePing function
       
        sop = self.sendOnePing(icmpsocket,destinationAddress,id)
        # 3. Call receiveOnePing function
        rop = self.receiveOnePing(icmpsocket,destinationAddress,id,timeout)
        totaltime = rop - sop
        totaltime = totaltime * 1000
        
        # 4. Close ICMP socket
        icmpsocket.close()
        # 5. Return total network delay

        return totaltime
           
    def tr(self,dest):
        dest_addr = dest
        ttl = 1
        port = 33434
        max_hops = 50
        checksum=0
        
       # print("start addr: "+ str(dest)) 
        if(args.protocol=='icmp'):
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('icmp'))
        else:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
        
        while True:
           
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            if(args.protocol)=="icmp":
                header = struct.pack("bbHHh",8,0,checksum,1,1)
                checksum = self.checksum(header) 
                header = struct.pack("bbHHh",8,0,checksum,1,1)

                recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
               
            else:
                port = 33434
                recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
               
            timeout = args.timeout
            recv_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, timeout)
            recv_socket.settimeout(timeout) 
            recv_socket.bind(("", port))
           
            if(args.protocol=='udp'):
                send_socket.sendto("msg".encode(), (dest, port))
            else:
                send_socket.sendto(header, (dest, port))
            
            addr = None
            curr_name = None
            finished = False
            tries=1
            while not finished and tries >0:
                try:
                    
                    soc, addr = recv_socket.recvfrom(1024)
                    header = soc[20:28]
                    type,code,checksum,packetID,seq = struct.unpack("bbHHh",header)
                    # ping a router if not reaching then unreachable if send 50 and only receive 25 back, 50 % loss
                    finished = True
                  
                    addr = addr[0]
                    
                    curr_name = socket.gethostbyaddr(addr)[0]
                    
                except socket.timeout:
                    print("***")
                    tries = tries - 1
                except socket.error:
                    curr_name = addr
                    
            recv_socket.close()
            
            if not finished:
                pass
            
            if addr is not None:
                # ping  times and report how many back to get packet loss
                self.packet_loss=0
              #  successfulPings =0
                for i in range(0,10): #
                    self.doOnePing(addr,args.timeout)
                 
                # get average time to get respond for time, use printoneresult method
                avgTimes = []
                for i in range(0,3):
                    time = self.doOnePing(addr,args.timeout)
                    avgTimes.append(time)
                
                self.printMultipleResults(ttl,addr,avgTimes,curr_name)
                self.printAdditionalDetails(self.packet_loss,min(avgTimes),sum(avgTimes)/3,max(avgTimes))

            
            ttl += 1
            if addr == dest_addr or ttl > max_hops:
                break
        send_socket.close()
    


    
class WebServer(NetworkApplication):

    def handleRequest(tcpSocket):
        # 1. Receive request message from the client on connection socket
        # 2. Extract the path of the requested object from the message (second part of the HTTP header)
        # 3. Read the corresponding file from disk
        # 4. Store in temporary buffer
        # 5. Send the correct HTTP response error
        # 6. Send the content of the file to the socket
        # 7. Close the connection socket
        pass

    def createServer(self):
        folder_path = '/home/lavickas/h-drive/203'
        serversockett = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversockett.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        try:
            serversockett.bind(('localhost',8080))
            serversockett.listen(5)
            while(1):
                indexGet = False
                content=""
                (clientsocket,address)=serversockett.accept()
                request = clientsocket.recv(5000).decode()
                pieces = request.split("\n")
                print(pieces[0])
                
                #http header
                headers = request.split('\n')
                filename = headers[0].split()[1]

                #content of file
                if filename == '/index.html':
                    indexGet=True
                    filename = '/index.html'
                    fin = open('/home/lavickas/h-drive/203'+filename )
                    content = fin.read()
                    #print(content)
                    fin.close()
                data = "HTTP/1.1 200 OK\r\n"
                data += "Content-Type: text/html; charset=utf-8\r\n"
                data += "\r\n"
                if(indexGet):
                    data+= content
                #data += "<html><body>Hello World</body></html>\r\n\rn\n"
                clientsocket.sendall(data.encode())
                clientsocket.shutdown(socket.SHUT_WR)
        except KeyboardInterrupt:
            print("\nShutting down...\n")
        except Exception as exc:
            data = "HTTP/1.1 404 Not Found\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            clientsocket.sendall(data.encode())
            print("Error:\n")
            print(exc)
        serversockett.close()
        pass

    def __init__(self, args):
        print('Web Server starting on port: %i...' % (args.port))
        self.createServer()
        # 1. Create server socket
        # 2. Bind the server socket to server address and server port
        # 3. Continuously listen for connections to server socket
        # 4. When a connection is accepted, call handleRequest function, passing new connection socket (see https://docs.python.org/3/library/socket.html#socket.socket.accept)
        # 5. Close server socket


class Proxy(NetworkApplication):

    def __init__(self, args):
        print('Web Proxy starting on port: %i...' % (args.port))
        port=args.port
        host='localhost'
        try:
            startSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            startSoc.bind((host, port)) #listen on this ip
            startSoc.listen(5)
    
        except socket.error as exc:
            if startSoc:
                startSoc.close()
            print("Could not open socket:")
            print(exc)
            sys.exit(1)

    
        while 1: # get client req
            con, client_addr = startSoc.accept()
            x=threading.Thread(target=self.proxy_thread,args=(con,))
            x.start()  
        startSoc.close()
    
    def proxy_thread(self,conn):
        
        #browseReq
        request = conn.recv(5000).decode()
        #firstLine
        print(request)
        print(request.split('\n'))
        first_line = request.split('\n')[0]
        print(first_line)
        #url
        url = first_line.split(' ')[1]
        print(url)
        #Webserver and port
        h_pos = url.find("://")
        print(h_pos)          
        if (h_pos==-1):
            temp = url
        else:
            temp = url[(h_pos+3):]       
        
        print(temp)
        webserver_pos = temp.find("/")
        print(webserver_pos)     
        port = 80
        webserver = temp[:webserver_pos]
        print(webserver)
     
        try:
            # create a socket to connect to the web server
            webserverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
            webserverSoc.connect((webserver, port))
            webserverSoc.send(request.encode())         
        
            while 1:
                
                data = webserverSoc.recv(5000)
                if (len(data) > 0):
                  
                    conn.send(data)
                    
                else:
                    break
            webserverSoc.close()
            conn.close()
        except socket.error:
            if webserverSoc:
                webserverSoc.close()
            if conn:
                conn.close()
            
            sys.exit(1)   

if __name__ == "__main__":

    args = setupArgumentParser()
    args.func(args)
