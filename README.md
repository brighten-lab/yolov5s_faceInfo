# [yolov5](https://github.com/heymin2/yolov5)를 이용한 얼굴 인식
2023년 브라이튼 겨울 방학 프로젝트

1. 브라이튼 경산 사무실에 있는 4명의 인물 사진을 마스크, 노마스크로 구분해 라벨링 후 [yolov5](https://github.com/heymin2/yolov5)를 이용해 학습시킴
2. 웹에 학습시킨 데이터가 포함된 카메라를 띄운 후, 날짜별 순위, 날짜별 데이터 보여줌

---

## ⭐️ YOLOv5 ⭐️
### 📝 data.yaml 작성
1. train, val 폴더 경로 작성
2. 라벨 이름 순서대로 작성


### 📖 학습
``` 
python3 train.py ---img 640 --batch 16 --epochs 100 --data dataset/data.yaml
```
🔹img: 이미지 크기


🔹batch: 배치 크기


🔹epoch: 전체 데이터 학습 횟수


🔹data: data.yaml 파일 경로


❗️ 결과가 좋지 않다면 epoch를 최대한 늘리기 ❗️


=> runs/train/exp로 결과 저장


### 💡 추론
```
python3 test.py
```


### 🔅 확인
```
python3 detect.py --weights run/train/exp/weights/best.pt --source 0
```
🔹--weights: best.pt 파일 경로


🔹--source 0: 웹캠

---

## 📌 실행
```
python3 app.py
```

---

## ⭐️ 기능 ⭐️
### 1️⃣ Main 
상단의 이모티콘을 누르면 데이터베이스에 기록된 화면을 볼 수 있다.
![스크린샷, 2023-01-20 13-15-06](https://user-images.githubusercontent.com/97522726/214493419-71d915cd-c0bd-442a-9a41-ff15f53f6ce9.png)

### 2️⃣ 기록1
년월일에 맞는 데이터를 보여준다.
![스크린샷, 2023-01-20 13-16-00](https://user-images.githubusercontent.com/97522726/214493427-01d3ef4c-25fe-468b-8d33-8941bb575402.png)

### 3️⃣ 기록2
해당 년월일에 가장 많이 인식된 순위를 보여준다.
![스크린샷, 2023-01-20 13-16-07](https://user-images.githubusercontent.com/97522726/214493431-c3fbdd76-20af-46a2-b6fc-d29b0810d1ee.png)

