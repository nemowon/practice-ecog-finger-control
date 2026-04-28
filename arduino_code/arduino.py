import serial
import time
import keyboard

SERIAL_PORT = "COM6"   # 改成你的端口
BAUD_RATE = 9600

valid_keys = ['1', '2', '3', '4', 'q', 'w', 'e', 'r']

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    print("按键控制已启动：")
    print("1/q -> Servo1: 10° / 90°")
    print("2/w -> Servo2: 10° / 90°")
    print("3/e -> Servo3: 10° / 90°")
    print("4/r -> Servo4: 10° / 90°")
    print("按 ESC 退出")

    while True:
        for key in valid_keys:
            if keyboard.is_pressed(key):
                ser.write(key.encode())
                print(f"Sent: {key}")
                time.sleep(0.25)  # 防止按住时疯狂重复发送

                while ser.in_waiting:
                    response = ser.readline().decode(errors='ignore').strip()
                    if response:
                        print("Arduino:", response)

        if keyboard.is_pressed('esc'):
            break

    ser.close()

if __name__ == "__main__":
    main()