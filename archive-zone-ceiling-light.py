import socket
import threading
import time

SERVER_IP = "192.168.0.10"
SERVER_PORT = 1234

# TCP 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to {SERVER_IP}:{SERVER_PORT}")


# 수신 메시지를 처리하는 함수
def receive_messages():
    while True:
        try:
            # 서버로부터 메시지 수신
            response = client_socket.recv(1024).decode("utf-8")
            if response:
                print(f"Received: {response}")
            else:
                break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


# 수신을 위한 스레드 시작
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# 'on' 명령어 전송
print("Sending: on")
client_socket.sendall("on".encode("utf-8"))
# 예상 응답: "on"

# 10초 대기
time.sleep(10)

# 'off' 명령어 전송
print("Sending: off")
client_socket.sendall("off".encode("utf-8"))
# 예상 응답: "off"

# 5초 대기 후 소켓 종료
time.sleep(5)
client_socket.close()
print("Connection closed")
