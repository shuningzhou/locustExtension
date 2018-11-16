import time  
import random  
# from socket import socket, AF_INET, SOCK_STREAM  
import socket  
from locust import Locust, TaskSet, events, task  
  
class TcpClient(socket.socket):  
    def __init__(self, af_inet, socket_type):  
        super(TcpClient, self).__init__(af_inet, socket_type)  
  
    def connect(self, addr):  
        start_time = time.time()  
        try:  
            super(TcpClient, self).connect(addr)  
        except Exception as e:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time, exception=e)  
        else:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time, response_length=0)  
          
    def send(self, msg):  
        start_time = time.time()  
        try:  
            super(TcpClient, self).send(msg)  
        except Exception as e:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)  
        else:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time, response_length=0)  
    
    def recv(self, bufsize):  
        recv_data = ''  
        start_time = time.time()  
        try:  
            recv_data = super(TcpClient, self).recv(bufsize)  
        except Exception as e:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e)  
        else:  
            total_time = int((time.time() - start_time) * 1000)  
            events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time, response_length=0)  
        return recv_data

    def close(self):
        super(TcpClient, self).close()

class TcpLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an TCP socket client
    that can be used to make TCP socket requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(TcpLocust, self).__init__(*args, **kwargs)
        self.client = TcpClient(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (self.host, self.port)
        self.client.connect(ADDR)

class TcpUser(TcpLocust):
    def teardown(self):
        self.client.close()

    host = "127.0.0.1"
    port = 12345
    min_wait = 100
    max_wait = 1000
 
    class task_set(TaskSet):        
        @task
        def send_data(self):
            self.client.send(random_str())
            data = self.client.recv(2048).decode()
            print(data)
 
 
if __name__ == "__main__":
    user = TcpUser()
    user.run()
