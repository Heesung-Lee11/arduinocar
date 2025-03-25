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

# 간단설명
EntryPoint는 QmainWindow
initUI 부분에서 레이아웃과 버튼, 이벤트핸들러를 추가하였습니다.
update_status 를 통해 기기의 현재상태를 갱신하여 버튼에 표시합니다.
update_frame 부분에서 아두이노 자동차가 받아온 영상을 처리하여 메인화면에 표시합니다.
keyPressEvent 부분에서 키보드의 입력을 받아 동작하는 부분을 구현하였습니다.
haar는 얼굴인식 기능
line_drive는 라인트레이싱 온오프
save,delte는 파일 저장삭제기능
아래 left,right 기능같은 경우 url요청을 통해 차량의 동작을 제어하는 부분입니다.

버튼또는 키보드로 url에 요청을 하면 웹 서버에서 자동차의 동작을 제어합니다.

