import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import serial
import time

# ==========================================
# UART 설정
# ==========================================

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

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
#
# -1.0 → 0
#  0.0 → 127
#  1.0 → 255
# ==========================================

def axis_to_byte(axis_value):

    value = int((axis_value + 1.0) * 127.5)

    if value < 0:
        value = 0

    if value > 255:
        value = 255

    return value

# ==========================================
# 메인 루프
# ==========================================

while True:

    try:

        pygame.event.pump()

        # ==================================
        # Axis 읽기
        #
        # Axis 1 : 전진 / 후진
        # Axis 2 : 좌회전 / 우회전
        # ==================================

        axis_speed = js.get_axis(1)
        axis_steer = js.get_axis(2)

        # ==================================
        # Byte 변환
        # ==================================

        speed_byte = axis_to_byte(axis_speed)
        steer_byte = axis_to_byte(axis_steer)

        # ==================================
        # UART 패킷 생성
        #
        # [START][SPEED][STEER][END]
        #
        # START = 0x3B
        # END   = 0x0D
        # ==================================

        packet = bytes([
            0x3B,
            speed_byte,
            steer_byte,
            0x0D
        ])

        # ==================================
        # UART 송신
        # ==================================

        ser.write(packet)

        # ==================================
        # 디버깅 출력
        # ==================================

        print(f"Speed Axis : {axis_speed:.3f} -> {speed_byte}")
        print(f"Steer Axis : {axis_steer:.3f} -> {steer_byte}")

        print("Packet :", packet.hex().upper())
        print("--------------------------------")

        time.sleep(0.1)

    except Exception as e:

        print("오류 발생 :", e)

        time.sleep(1)