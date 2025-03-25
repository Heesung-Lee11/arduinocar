# 프로젝트
## PyQt5 GUI를 사용하여 아두이노 기반의 자동차를 제어하고, 실시간 영상 스트리밍을 표시하는 프로그램입니다.

# 가상환경 생성
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 필수 패키지 설치
pip install PyQt5 opencv-python numpy

# 실행방법
python main.py

# GRID 방식의 레이아웃 활용 결과
### 웹캠을 통하여 자동차의 Grid 레이아웃을 미리 설정해 보았는데 원하는 화면의 배치가 적절하지 않아서 밑에있는 BOX 형식의 레이아웃으로 수정하였습니다.
![grid활용](./images/grid%20활용.jpg)

# BOX 방식의 레이아웃 활용 결과
### Grid 레이아웃에서 Box 형식으로 전환뒤 각각의 키입력을 아스키코드랑 키설정을 하여 화면에 보이는 현재상태에 동작을 추가하였습니다.
![hboxs 레이아웃으로](./images/hboxs%20레이아웃으로.jpg)

# W 키 입력 눌렀을때 화면입니다.
![Box](./images/Box.jpg)