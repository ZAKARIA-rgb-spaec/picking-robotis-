import gym
from gym import spaces
import numpy as np
import cv2
from stable_baselines3 import PPO
import time

try:
    import rtde_control
    import rtde_receive
except ImportError as e:
    print(f"Error importing RTDE modules: {e}")
    exit()

ROBOT_IP = '172.31.116.25'

class RobotEnv(gym.Env):
    def __init__(self, rtde_c, rtde_r):
        super(RobotEnv, self).__init__()
        self.rtde_c = rtde_c
        self.rtde_r = rtde_r
        self.action_space = spaces.Discrete(4)  # Example: 4 possible actions
        self.observation_space = spaces.Box(low=0, high=255, shape=(640, 480, 3), dtype=np.uint8)
        self.camera_index = 1
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not self.cap.isOpened():
            raise Exception("Error: Unable to open camera")

    def reset(self):
        self.rtde_c.moveJ([0, -1.57, 0, -1.57, 0, 0])
        ret, frame = self.cap.read()
        return frame

    def step(self, action):
        if action == 0:  # Example action: close gripper
            close_gripper(self.rtde_c)
        elif action == 1:  # Example action: open gripper
            open_gripper(self.rtde_c)
        elif action == 2:  # Move robot left
            self.rtde_c.moveL([0.1, 0, 0, 0, 0, 0])
        elif action == 3:  # Move robot right
            self.rtde_c.moveL([-0.1, 0, 0, 0, 0, 0])

        ret, frame = self.cap.read()
        reward = self.calculate_reward(frame)
        done = self.check_done(frame)
        info = {}

        return frame, reward, done, info

    def calculate_reward(self, frame):
        reward = 0
        return reward

    def check_done(self, frame):
        done = False
        return done

    def render(self, mode='human'):
        pass

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

def connect_to_robot():
    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    try:
    
        if not (rtde_c.isConnected() and rtde_r.isConnected()):
            raise Exception("Error: Unable to connect to UR5e robot")
        return rtde_c, rtde_r
    except Exception as e:
        print(f"Error connecting to robot: {e}")
        exit()

def open_gripper(rtde_c):
    if rtde_c:
        try:
            rtde_c.sendCustomScript("def myProg():\n\tset_standard_digital_out(0, True)\nend\n")
            time.sleep(1)
        except Exception as e:
            print(f"Error opening gripper: {e}")
    else:
        print("Error: rtde_c is not initialized")

def close_gripper(rtde_c):
    if rtde_c:
        try:
            rtde_c.sendCustomScript("def myProg():\n\tset_standard_digital_out(0, False)\nend\n")
            time.sleep(1)
        except Exception as e:
            print(f"Error closing gripper: {e}")
    else:
        print("Error: rtde_c is not initialized")

def move_robot_to_coordinates(rtde_c, x, y, z, defective):
    if rtde_c:
        try:
            if defective:
                target_pose = [20.06, -19.77, -17.53, 2.2, 2.1, -0.15]
            else:
                target_pose = [20.69, 14.83, -13.8, 2.3, 2.1, -0.03]
            print(f"Moving to position: {target_pose}")
            rtde_c.moveL(target_pose)
        except Exception as e:
            print(f"Error moving robot: {e}")
    else:
        print("Error: rtde_c is not initialized")

# Load YOLO classes
classes = []
with open("yolov3.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = net.getUnconnectedOutLayersNames()

rtde_c, rtde_r = connect_to_robot()

# Create the environment
env = RobotEnv(rtde_c, rtde_r)

# Create the PPO model
model = PPO('CnnPolicy', env, verbose=1)
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_robot")

# Load the model
model = PPO.load("ppo_robot")

while True:
    ret, frame = env.cap.read()
    if not ret:
        print("Error: Unable to read camera frame")
        continue

    height, width, channels = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label + " " + confidence, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

            # Use coordinates to move the robot
            robot_x = (x + w / 2) / width
            robot_y = (y + h / 2) / height
            robot_z = 0.1

            action, _states = model.predict(frame)
            obs, rewards, done, info = env.step(action)
            if done:
                obs = env.reset()

    cv2.imwrite("output.jpg", frame)
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

env.close()

if rtde_c:
    rtde_c.stopScript()
if rtde_r:
    rtde_r.disconnect()
