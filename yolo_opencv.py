import cv2
import numpy as np
import matplotlib.pyplot as plt

# Charger les classes YOLO
classes = []
with open("yolov3.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Charger le modèle YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = net.getUnconnectedOutLayersNames()

# Démarrer la capture vidéo
cap = cv2.VideoCapture(0)  # 0 pour la webcam intégrée, 1 pour une webcam externe

while True:
    _, frame = cap.read()
    height, width, channels = frame.shape

    # Prétraitement de l'image pour l'entrée au modèle YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Analyse des détections
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Coordonnées du cadre délimitant l'objet détecté
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Points de l'angle supérieur gauche
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Suppression des détections multiples
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Affichage des résultats
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

    # Affichage de la vidéo en temps réel avec matplotlib
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame)
    plt.pause(0.01)  # Pause nécessaire pour que Matplotlib mette à jour l'affichage
    plt.draw()

    
# Fermer la capture vidéo et libérer les ressources
cap.release()
cv2.destroyAllWindows()
