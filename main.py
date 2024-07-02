import rtde_control
import rtde_receive
import time
import cv2
import numpy as np

ROBOT_IP = '172.31.116.25'

def connect_to_robot():
    rtde_c = None
    rtde_r = None
    try:
        rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
        rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
        if not (rtde_c.isConnected() and rtde_r.isConnected()):
            print("Erreur : Impossible de se connecter au robot UR5e")
            exit()
        return rtde_c, rtde_r
    except Exception as e:
        print(f"Erreur lors de la connexion au robot: {e}")
        exit()

def open_gripper(rtde_c):
    """Ouvre la pince."""
    if rtde_c:
        try:
            rtde_c.sendCustomScript("def myProg():\n\tset_standard_digital_out(0, True)\nend\n")
            time.sleep(1)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de la pince: {e}")
    else:
        print("Erreur : rtde_c n'est pas initialisé")

def close_gripper(rtde_c):
    """Ferme la pince."""
    if rtde_c:
        try:
            rtde_c.sendCustomScript("def myProg():\n\tset_standard_digital_out(0, False)\nend\n")
            time.sleep(1)
        except Exception as e:
            print(f"Erreur lors de la fermeture de la pince: {e}")
    else:
        print("Erreur : rtde_c n'est pas initialisé")

def move_robot_to_coordinates(rtde_c, x, y, z, defective):
    """Déplace le robot aux coordonnées spécifiées en fonction de l'état de l'objet."""
    if rtde_c:
        try:
            if defective:
                target_pose = [20.06, -19.77, -17.53, 2.2, 2.1, -0.15]
            else:
                target_pose = [20.69, 14.83, -13.8, 2.3, 2.1, -0.03]
            print(f"Déplacement vers la position : {target_pose}")
            rtde_c.moveL(target_pose)
        except Exception as e:
            print(f"Erreur lors du déplacement du robot: {e}")
    else:
        print("Erreur : rtde_c n'est pas initialisé")

# Charger les classes YOLO
classes = []
with open("yolov3.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Charger le modèle YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = net.getUnconnectedOutLayersNames()

# Démarrer la capture vidéo
camera_index = 1
cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

# Set resolution (you can adjust these values as needed)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra")
    exit()

rtde_c, rtde_r = connect_to_robot()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire le cadre de la caméra")
        continue

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
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

            # Utiliser les coordonnées pour déplacer le robot
            # Convertir les coordonnées pour le robot
            robot_x = (x + w / 2) / width
            robot_y = (y + h / 2) / height
            robot_z = 0.1  # Hauteur fixe pour saisir l'objet
            
            print(f"Coordonnées détectées : x={robot_x}, y={robot_y}, z={robot_z}")

            # Fermer la pince, déplacer le robot, puis ouvrir la pince
            close_gripper(rtde_c)
            move_robot_to_coordinates(rtde_c, robot_x, robot_y, robot_z, defective=False)
            open_gripper(rtde_c)

    # Sauvegarder l'image avec détection
    cv2.imwrite("output.jpg", frame)
    
    # Affichage de la vidéo en temps réel avec OpenCV
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer la capture vidéo et libérer les ressources
cap.release()
cv2.destroyAllWindows()

# Libérer les ressources du robot
if rtde_c:
    rtde_c.stopScript()
if rtde_r:
    rtde_r.disconnect()
