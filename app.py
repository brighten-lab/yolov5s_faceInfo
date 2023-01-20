"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
from query import update
import threading
from flask import Flask, render_template, Response, request
import torch
import io
from PIL import Image
import cv2
import numpy as np
from time import sleep
import pymysql
import json
import collections

app = Flask(__name__)

# Load Custom Model
model = torch.hub.load("ultralytics/yolov5", "custom",
                       path="runs/train/exp5/weights/best.pt", force_reload=True)

# Set Model Settings
model.eval()
model.conf = 0.75  # confidence threshold (0-1)
model.iou = 0.45  # NMS IoU threshold (0-1)

# webcam
cap = cv2.VideoCapture(0)

results = None
lst = []

def detect():
    global results
    global lst
    global cap
    if not cap.isOpened():
        print("실패")
    while (cap.isOpened()):
        # Capture frame-by-fram ## read the camera frame
        success, frame = cap.read()
        if success == True:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            img = Image.open(io.BytesIO(frame))

            ''' 학습한 이미지 사이즈 맞추기 '''
            results = model(img, size=640)

            lst = []
            df = results.pandas().xyxy[0]
            for i in df['name']:
                if 'mask' in i:
                    update(i[4:])
                    lst.append(i[4:])
                else:
                    update(i)
                    lst.append(i)
            if(len(lst) != 0):
                print(lst)
          
def gen():
    global results
    while (cap.isOpened()):
        # convert remove single-dimensional entries from the shape of an array
        img = np.squeeze(results.render())  # RGB
        # read image as BGR
        img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # BGR

        # Encode BGR image to bytes so that cv2 will convert to RGB
        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        # print(frame)
        # sleep(0.03)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/show', methods = ['POST', 'GET'])
def sh():
    if request.method == 'POST':
        date = request.form['date']
        con = pymysql.connect(host='localhost', user='nemin', password='1234', db='face', charset='utf8')
        cur = con.cursor()
        sql = "select * from faceInfo where DATE_FORMAT(start, '%%Y-%%m-%%d') = %s;"
        cur.execute(sql, date)
        rows = cur.fetchall()

        sql2 = "select name, count(*) from faceInfo where date_format(start, '%%Y-%%m-%%d') = %s group by name having count(*) order by count(*) desc;"
        cur.execute(sql2, date)
        rows2 = cur.fetchall()
        data = []

        for row in rows2:
            tmp = collections.OrderedDict()
            tmp['name'] = row[0]
            tmp['count'] = int(row[1])
            data.append(tmp)

        return render_template('show.html', rows = rows, data = data)

    con = pymysql.connect(host='localhost', user='nemin', password='1234', db='face', charset='utf8')
    cur = con.cursor()

    sql = "select name, count(*) from faceInfo where date_format(start, '%Y%m%d') = date_format(NOW(), '%Y%m%d') group by name having count(*) order by count(*) desc;"
    cur.execute(sql)
    rows = cur.fetchall()
    data = []

    for row in rows:
        tmp = collections.OrderedDict()
        tmp['name'] = row[0]
        tmp['count'] = int(row[1])
        data.append(tmp)

    # return render_template('show.html', rows = None, data = json.dumps(data))
    return render_template('show.html', rows = None, data = data)

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    detect_thread = threading.Thread(target=detect)
    detect_thread.start()
    app.run(host='0.0.0.0', port=5000)