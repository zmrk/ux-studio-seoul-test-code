import serial
import threading
import time

# 시리얼 포트 설정 (COM2, 보드레이트 9600, 타임아웃 1초)
ser = serial.Serial(port="COM2", baudrate=9600, timeout=1)


def read_response():
    """
    스레드를 이용하여 지속적으로 응답을 수신하는 함수
    """
    while True:
        if ser.in_waiting > 0:
            response = ser.read_until(b"\x03")  # 패킷 끝 0x03까지 읽기
            print(f"[응답 수신] {response}")


# 응답 수신을 위한 스레드 실행
threading.Thread(target=read_response, daemon=True).start()


def send_command(command):
    """
    도어 제어 명령을 전송하는 함수
    :param command: 전송할 명령 문자열 (예: 'D1', 'D2')
    """
    packet = b"\x02" + command.encode() + b"\x03"
    ser.write(packet)
    print(f"[명령 전송] {packet}")


# 도어 열기 명령어 전송 (D1)
send_command("D1")
# 예상 응답: [응답 수신] b'\x02D1\x03'
# 잠시 후 도어 열림 응답 수신 (D3)
# 예상 응답: [응답 수신] b'\x02D3\x03'

time.sleep(10)  # 10초 대기

# 도어 닫기 명령어 전송 (D2)
send_command("D2")
# 예상 응답: [응답 수신] b'\x02D2\x03'
# 잠시 후 도어 닫힘 응답 수신 (D4)
# 예상 응답: [응답 수신] b'\x02D4\x03'

# 일정 시간 이후 프로그램 종료 방지
while True:
    time.sleep(1)
