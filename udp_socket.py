import socket
from datetime import datetime
class rpi_socket():
	def __init__(self, ip, port,pathin):
		try:
			self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			self.sock.bind((ip, port))
			self.pathin=pathin
		except Exception as e: 
			print(e)
			print(f'Unable to establish connection with {ip}') 
	def run(self):
		while True: 
			data, addr=self.sock.recvfrom(1024)
			data=data.decode('utf-8')
			if data[0]=='i':
				with open(self.pathin,"a") as RFIDs:
					RFIDs.write('SPT_IN'+','+str(datetime.now())+','+data+'\n')
				print(f'Tag{str(data[1:])} entered the SPT_tunnel at {str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"))}')
			elif data[0]=='o':
				with open(self.pathin,"a") as RFIDs:
					RFIDs.write('SPT_OUT'+','+str(datetime.now())+','+data+'\n')
				print(f'Tag{str(data[1:])} existed the SPT_tunnel at {str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"))}')
