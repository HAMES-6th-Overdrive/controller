import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import socket
import struct
import time

# ==========================================
# SOME/IP 설정
# ==========================================

ZCU_IP = "192.168.10.2"
ZCU_PORT = 30500

SERVICE_ID = 0x0001
METHOD_ID  = 0x1001

CLIENT_ID = 0x0001

PROTOCOL_VERSION = 0x01
INTERFACE_VERSION = 0x01

MSG_TYPE_REQUEST = 0x00
RETURN_CODE_OK   = 0x00

session_id = 1

# ==========================================
# Gear 설정
# ==========================================

BUTTON_P = 0
BUTTON_D = 1

GEAR_P = 0
GEAR_D = 1

gear_state = GEAR_P

# ==========================================
# UDP 소켓 생성
# ==========================================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ==========================================
# pygame 초기화
# ==========================================

pygame.init()
pygame.joystick.init()

# ==========================================
# 게임패드 연결 대기
# ==========================================

while pygame.joystick.get_count() == 0:

    print("게임패드 연결 대기중...")

    time.sleep(1)

    pygame.joystick.quit()
    pygame.joystick.init()

# ==========================================
# 게임패드 연결
# ==========================================

js = pygame.joystick.Joystick(0)
js.init()

print("게임패드 연결됨 :", js.get_name())

# ==========================================
# Axis 값을 0~255로 변환
# ==========================================

def axis_to_byte(axis_value):

    value = int((axis_value + 1.0) * 127.5)

    if value < 0:
        value = 0

    if value > 255:
        value = 255

    return value

# ==========================================
# SOME/IP 패킷 생성
# ==========================================

def build_someip(service_id,
                 method_id,
                 client_id,
                 session_id,
                 payload):

    message_id = (service_id << 16) | method_id
    request_id = (client_id << 16) | session_id

    # Request ID 4Byte
    # PV/IV/Type/RC 4Byte
    # + payload

    length = 8 + len(payload)

    header = struct.pack(
        "!IIIBBBB",
        message_id,
        length,
        request_id,
        PROTOCOL_VERSION,
        INTERFACE_VERSION,
        MSG_TYPE_REQUEST,
        RETURN_CODE_OK
    )

    return header + payload

# ==========================================
# 메인 루프
# ==========================================

while True:

    try:

        pygame.event.pump()

        # ==============================
        # Axis 읽기
        # ==============================

        axis_speed = js.get_axis(1)
        axis_steer = js.get_axis(2)

        # ==============================
        # 기어 버튼 입력
        # ==============================

        if js.get_button(BUTTON_P):

            gear_state = GEAR_P

        if js.get_button(BUTTON_D):

            gear_state = GEAR_D

        # ==============================
        # Byte 변환
        # ==============================

        speed_byte = axis_to_byte(axis_speed)
        steer_byte = axis_to_byte(axis_steer)

        if gear_state == GEAR_P:

            speed_byte = 127
            steer_byte = 127

        # ==============================
        # Payload 생성
        #
        # [SPEED][STEER]
        # ==============================

        payload = bytes([
            speed_byte,
            steer_byte
        ])

        # ==============================
        # SOME/IP 패킷 생성
        # ==============================

        packet = build_someip(
            SERVICE_ID,
            METHOD_ID,
            CLIENT_ID,
            session_id,
            payload
        )

        # ==============================
        # Ethernet 송신
        # ==============================

        sock.sendto(packet, (ZCU_IP, ZCU_PORT))

        # ==============================
        # 디버깅 출력
        # ==============================

        print(f"Speed Axis : {axis_speed:.3f} -> {speed_byte}")
        print(f"Steer Axis : {axis_steer:.3f} -> {steer_byte}")

        print(
            f"Gear : "
            f"{'P' if gear_state == GEAR_P else 'D'}"
        )

        print("Payload :", payload.hex().upper())
        print("Packet  :", packet.hex().upper())

        print("--------------------------------")

        # ==============================
        # Session 증가
        # ==============================

        session_id += 1

        if session_id > 0xFFFF:
            session_id = 1

        time.sleep(0.1)

    except Exception as e:

        print("오류 발생 :", e)

        time.sleep(1)