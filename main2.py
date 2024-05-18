import cv2


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
    return faceBoxes

def predict(path):

    # Model paths and loading
    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"
    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"
    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    # Constants and model lists
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    # Load image
    # image_path = r"C:\Users\thrid\OneDrive\Desktop\age-gender-detector-python-master\test\28_0_1_20170113195927894.jpg.chip.jpg"
    vidFrame = cv2.imread(path)

    padding = 20
    faceBoxes = getFaceBox(faceNet, vidFrame)


    if not faceBoxes:
        print("No face detected")
    else:
        for faceBox in faceBoxes:
            face = vidFrame[max(0, faceBox[1]-padding):min(faceBox[3]+padding, vidFrame.shape[0]-1),
                            max(0, faceBox[0]-padding):min(faceBox[2]+padding, vidFrame.shape[1]-1)]
            
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            
            
            print(f"Detected Gender: {gender}, Age Category: {age}")

    return age, gender

            
