from flask import * 
from database import *
import uuid
from main2 import *

user=Blueprint("user" ,__name__)


@user.route('/userhome')
def userhome():
    return render_template("userhome.html")

@user.route('/feedback',methods={'get','post'})
def feedbackpage():
    if 'submit' in request.form:
        reviw_desp=request.form['reviw_desp']
        
        qry="insert into feedback values(null,'%s','%s')"%(session['uid'],reviw_desp)
        insert(qry)
    return render_template("feedback.html")

@user.route('/result',methods={'get','post'})
def resultpage():
    name=""
    path=""
    predict_value=""
    if 'submit' in request.form:
        name=request.form['name']
        image=request.files['image']
        path='static/uploads/' + str(uuid.uuid4()) +".jpg"
        image.save(path)

        predict_value=predict(path)
        li=list(predict_value)
        li_str = json.dumps(li)
        print("pi: ",li)

        print(predict_value,"/"*200)

        
        qry="insert into result values(null,'%s','%s','%s','%s')"%(name,path,li_str,session['uid'])
        print(qry)
        insert(qry)

    # data={}
    # a="select * from result "
    # data['key']=select(a)

    return render_template("result.html",predict_value=predict_value,path=path,name=name)



import cv2

@user.route('/live',methods={'get','post'})
def live():
    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"

    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"

    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    video = cv2.VideoCapture(0)

    padding = 20

    while True:
        hasFrame, vidFrame = video.read()

        if not hasFrame:
            cv2.waitKey()
            break

        frame, faceBoxes = getFaceBox(faceNet, vidFrame)

        if not faceBoxes:
            print("No face detected")

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1] - padding):min(faceBox[3] + padding, frame.shape[0] - 1),
                max(0, faceBox[0] - padding):min(faceBox[2] + padding, frame.shape[1] - 1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            genderNet.setInput(blob)
            genderPred = genderNet.forward()
            gender = genderList[genderPred[0].argmax()]

            ageNet.setInput(blob)
            agePred = ageNet.forward()
            age = ageList[agePred[0].argmax()]

            labelGender = "{}".format("Gender : " + gender)
            labelAge = "{}".format("Age : " + age + "Years")
            cv2.putText(frame, labelGender, (faceBox[0], faceBox[1] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, labelAge, (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Age-Gender Detector", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return redirect(url_for('user.resultpage'))





def getFaceBox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    faceBoxes = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return frame, faceBoxes


