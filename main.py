# 자동차 아두이노 활용해서 동작하기
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from urllib.request import urlopen
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt

import numpy as np
import cv2
import os


class App(QMainWindow):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))   
    # images 폴더가 없으면 생성
    if not os.path.exists("images"):
            os.mkdir("images")    
    
    ip = '192.168.137.47'

    def __init__(self):
        super().__init__()

        self.face_active = False
        self.face_model = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


        self.line_drive_active = False 
        
        self.stream = urlopen('http://' + App.ip +':81/stream')
        self.buffer = b""
        urlopen('http://' + App.ip + "/action?go=speed40")
        self.initUI()

    def initUI(self):
        
        widget = QWidget() 

        self.video_label = QLabel(self)
        self.video_label.setGeometry(0, 0, 800, 600)

        # 타이머 설정하여 일정 간격으로 프레임 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(2) 

        # 속도관련    
        btn_speed_40 = QPushButton('속도 40', self)
        btn_speed_40.resize(100, 50) 

        btn_speed_50 = QPushButton('속도 50', self)
        btn_speed_50.resize(100, 50) 

        btn_speed_60 = QPushButton('속도 60', self)
        btn_speed_60.resize(100, 50) 

        btn_speed_80 = QPushButton('속도 80', self)
        btn_speed_80.resize(100, 50) 
        
        btn_speed_100 = QPushButton('속도 100', self)
        btn_speed_100.resize(100, 50) 


        # 방향키 관련
        btn_turn_left = QPushButton('왼쪽으로 돌기', self)
        btn_turn_left.resize(100, 50) 

        btn_forward = QPushButton('앞으로', self)
        btn_forward.resize(100, 50) 

        btn_turn_right = QPushButton('오른쪽으로 돌기', self)
        btn_turn_right.resize(100, 50) 

        btn_left = QPushButton('왼쪽', self)
        btn_left.resize(100, 50) 

        btn_stop = QPushButton('멈춤', self)
        btn_stop.resize(100, 50) 

        btn_right = QPushButton('오른쪽', self)
        btn_right.resize(100, 50) 

        btn_haar = QPushButton('Haar', self)
        btn_haar.resize(100, 50) 
        
        btn_backward = QPushButton('뒤로가기', self)
        btn_backward.resize(100, 50) 
        
        # 특수동작 활동 
        btn_line_drive = QPushButton('라인트레이싱', self)
        btn_line_drive.resize(100, 50) 

        btn_save = QPushButton('저장하기', self)
        btn_save.resize(100, 50) 

        btn_delete = QPushButton('삭제하기', self)
        btn_delete.resize(100, 50) 

        self.btn_state = QPushButton('현재상태', self)
        self.btn_state.setDisabled(True)  # 버튼 비활성화
        self.btn_state.resize(100, 50)

        # 버튼을 이벤트와 연결
        btn_speed_40.pressed.connect(self.speed_40)
        btn_speed_50.pressed.connect(self.speed_50)
        btn_speed_60.pressed.connect(self.speed_60)
        btn_speed_80.pressed.connect(self.speed_80)
        btn_speed_100.pressed.connect(self.speed_100)

        btn_turn_left.pressed.connect(self.turn_left)
        btn_turn_right.pressed.connect(self.turn_right)

        btn_haar.pressed.connect(self.haar)
        btn_line_drive.pressed.connect(self.line_drive)
        btn_save.pressed.connect(self.save)
        btn_delete.pressed.connect(self.delete)

        btn_forward.pressed.connect(self.forward)
        btn_right.pressed.connect(self.right)
        btn_stop.pressed.connect(self.stop)
        btn_left.pressed.connect(self.left)
        btn_backward.pressed.connect(self.backward)

        hbox_speed = QHBoxLayout()
        hbox_speed.addWidget(btn_speed_40)
        hbox_speed.addWidget(btn_speed_50)
        hbox_speed.addWidget(btn_speed_60)
        hbox_speed.addWidget(btn_speed_80)
        hbox_speed.addWidget(btn_speed_100)

        hbox_move_1 = QHBoxLayout()
        hbox_move_1.addWidget(btn_turn_left)
        hbox_move_1.addWidget(btn_forward)
        hbox_move_1.addWidget(btn_turn_right)

        hbox_move_2 = QHBoxLayout()
        hbox_move_2.addWidget(btn_left)
        hbox_move_2.addWidget(btn_stop)
        hbox_move_2.addWidget(btn_right)

        hbox_move_3 = QHBoxLayout()
        hbox_move_3.addWidget(btn_haar)
        hbox_move_3.addWidget(btn_backward)
        hbox_move_3.addWidget(btn_line_drive)

        hbox_move_4 = QHBoxLayout()
        hbox_move_4.addWidget(btn_save)
        hbox_move_4.addWidget(self.btn_state)
        hbox_move_4.addWidget(btn_delete)

        vbox = QVBoxLayout(widget) # 세로 방향 레이아웃 
        vbox.addWidget(self.video_label) # 비디오 영상
        vbox.addLayout(hbox_speed) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_1) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_2) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_3) 
        vbox.addStretch(1)
        vbox.addLayout(hbox_move_4) 

        # self 는 현재 MainWindow 
        # 아래 코드는 MainWindow 안에다 Widget 추가하기 코드! 
        self.setCentralWidget(widget)

        self.setWindowTitle('AI CAR CONTROL WINDOW')
        self.move(600, 400)
        self.resize(400, 300)
        self.show()
    
    def update_status(self, status="대기중"):
        self.btn_state.setText(f'현재상태: {status}')

    def update_frame(self):
        self.buffer += self.stream.read(4096)
        head = self.buffer.find(b'\xff\xd8')
        end = self.buffer.find(b'\xff\xd9')

        try: 
            if head > -1 and end > -1:
                jpg = self.buffer[head:end+2]
                self.buffer = self.buffer[end+2:]
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                img = cv2.flip(img, 1) # 이미지 상하반전 

                #  얼굴 인식 활성화 시, 얼굴을 감지
                if self.face_active:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(img, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                #  라인트레이싱
                if self.line_drive_active:
                    height, width, _ = img.shape
                    roi = img[height // 2 :, :]  # 하단 절반 사용

                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                    #  노이즈 제거 및 검은색 라인 감지
                    mask = cv2.inRange(blurred, 0, 50)  # 검은색 검출

                    #  엣지 감지
                    edges = cv2.Canny(mask, 50, 150)

                    #  무게 중심 계산 (X 좌표 평균값 사용)
                    points = np.column_stack(np.where(mask > 0))

                    if len(points) > 500:  # 최소 500개의 픽셀 이상 검출될 때만 동작
                        cX = int(np.mean(points[:, 1]))  # X 좌표의 평균값
                        cY = int(np.median(points[:, 0]))  # Y 좌표의 중앙값
                    else:
                        cX, cY = width // 2, height - 10  # 기본값

                    #  무게 중심 표시
                    cv2.circle(roi, (cX, cY), 10, (0, 255, 0), -1)
                    cv2.putText(roi, f"({cX},{cY})", (cX + 20, cY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # 이동 방향 결정
                    camera_offset = 10  # 카메라 오프셋 (조정 필요)
                    center_offset = (width // 2 + camera_offset) - cX
                    threshold = 25  # 움직이는 기준 값

                    if center_offset > threshold:  # 오른쪽으로 이동
                        print(f"🔵 오른쪽 이동 (offset: {center_offset})")
                        urlopen("http://" + App.ip + "/action?go=right")
                        self.update_status("오른쪽 이동")
                    elif center_offset < -threshold:  # 왼쪽으로 이동
                        print(f"🟢 왼쪽 이동 (offset: {center_offset})")
                        urlopen("http://" + App.ip + "/action?go=left")
                        self.update_status("왼쪽 이동")
                    else:  # 직진
                        print(f"🟡 직진 (offset: {center_offset})")
                        urlopen("http://" + App.ip + "/action?go=forward")
                        self.update_status("직진")

                

                self.capture = img.copy() 

                # OpenCV의 BGR 이미지를 RGB로 변환
                frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # OpenCV의 이미지를 QImage로 변환
                height, width, channels = frame.shape
                bytes_per_line = 3 * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

                # QPixmap을 QLabel에 표시
                pixmap = QPixmap.fromImage(q_image)
                self.video_label.setPixmap(pixmap)
        except Exception as e :
            print(e)
    
    
    def keyPressEvent(self, event):
        print("현재 입력된 키 :", event.key())
        if event.key() == 16777216:  # ESC 는 27 = close
            self.close()

        elif event.key() == Qt.Key_1:
            self.speed_40()
        
        elif event.key() == Qt.Key_2:
            self.speed_50()
        
        elif event.key() == Qt.Key_3:
            self.speed_60()
        
        elif event.key() == Qt.Key_4:
            self.speed_80()
        
        elif event.key() == Qt.Key_5:
            self.speed_100()

        elif event.key() == 87:  # W = 87 이다 아스키코드를 활용해서 넣어 보았음
            self.forward()

        elif event.key() == 65:  # A = 65 
            self.left()

        elif event.key() == 83:  #  S = 83 
            self.stop()

        elif event.key() == 68:  # D = 87 
            self.right()

        elif event.key() == 88:  # x = 88 
            self.backward()

        elif event.key() == Qt.Key_Q: # Q = 왼쪽으로돌기
            self.turn_left()

        elif event.key() == Qt.Key_E: # E = 오른쪽으로돌기
            self.turn_right()

        elif event.key() == Qt.Key_Z: # Z = Haar 
            self.haar()

        elif event.key() == Qt.Key_C: # C = 라인트레이싱
            self.line_drive()
        
        elif event.key() == Qt.Key_I: # I = 저장하기
            self.save()

        elif event.key() == Qt.Key_O: # O = 삭제하기
            self.delete()


    def closeEvent(self, event):
        event.accept()

    def speed_40(self):
        urlopen(f'http://' +App.ip+ '/action?go=speed40')
        print("속도40")

    def speed_50(self):
        urlopen(f'http://' +App.ip+ '/action?go=speed50')
        print("속도50")

    def speed_60(self):
        urlopen(f'http://'+ App.ip+ '/action?go=speed60')
        print("속도60")
    
    def speed_80(self):
        urlopen(f'http://'+App.ip+ '/action?go=speed80')
        print("속도80")

    def speed_100(self):
        urlopen(f'http://'+ App.ip + "/action?go=speed100")
        print("속도100")

    def haar(self):
        """얼굴 인식 기능을 켜거나 끄는 함수"""
        self.face_active = not self.face_active  # 얼굴 인식 상태를 토글
        status = "활성화" if self.face_active else "비활성화"
        print(f"얼굴 인식 기능 {status}")
        

        # 얼굴 인식 상태에 따라 로봇에 명령을 보낼 수 있습니다.
        if self.face_active:
        # 얼굴 인식 활성화에 관련된 코드 추가 (예: 카메라를 활성화하거나 얼굴 추적 시작)
            pass
        else:
        # 얼굴 인식 비활성화에 관련된 코드 추가 (예: 얼굴 추적 중지)
            pass

    def line_drive(self):
        urlopen('http://' + App.ip + "/action?go=stop")
        """라인 트레이싱 자율주행 기능을 켜거나 끄는 함수"""
        self.line_drive_active = not self.line_drive_active  # 자율주행 상태를 토글
        status = "자율주행 활성화중" if self.line_drive_active else "자율주행 비활성화중"
        print(f"Line drive {status}")  # 상태 출력

        if not self.line_drive_active:
            print("🛑 라인트레이싱 중지")
            urlopen("http://" + App.ip + "/action?go=stop")  # 라인트레이싱 종료 시 정지
            self.update_status("라인트레이싱 중지")
    
    # 이미지 저장과 최근이미지를 삭제하는 함수입니다.
    def save(self):
        if hasattr(self, 'capture') and self.capture is not None:
            save_path = f"images/image_{len(os.listdir('images'))}.png"
            cv2.imwrite(save_path, self.capture)
            print(f"이미지 저장 완료: {save_path}")
        else:
            print("⚠ 저장할 이미지가 없습니다!")

    def delete(self):
        files = sorted(os.listdir("images"), reverse=True)
        if files:
            os.remove(f"images/{files[0]}")
            print("최근 이미지 삭제 완료")
    
    def forward(self) :
        urlopen('http://' + App.ip + "/action?go=forward")
        self.update_status("앞으로")
        print("앞으로")

    def turn_left(self) :
        urlopen('http://' + App.ip + "/action?go=turn_left")
        self.update_status("왼쪽으로 돌기")
        print("왼쪽으로 돌기")

    def turn_right(self) :
        urlopen('http://' + App.ip + "/action?go=turn_right")
        self.update_status("오른쪽으로 돌기")
        print("오른쪽으로 돌기")

    def left(self) :
        urlopen('http://' + App.ip + "/action?go=left")
        self.update_status("왼쪽")
        print("왼쪽")

    def right(self) :
        urlopen('http://' + App.ip + "/action?go=right")
        self.update_status("오른쪽")
        print("오른쪽")


    def backward(self) :
        urlopen('http://' + App.ip + "/action?go=backward")
        self.update_status("뒤로가기")
        print("뒤로가기")

    def stop(self) :
        urlopen('http://' + App.ip + "/action?go=stop")
        self.update_status("정지")
        print("정지")
    
    def update_status(self, status="대기중"):
        self.btn_state.setText(f'현재상태: {status}')

if __name__ == '__main__':
    print(sys.argv)
    app = QApplication(sys.argv)
    view = App()
    sys.exit(app.exec_())
