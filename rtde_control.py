import rtde_control
import rtde_receive
import time

ROBOT_IP = '172.31.116.25'

# Connexion aux interfaces de contrôle et de réception du robot
rtde_c = None
rtde_r = None

try:
    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    if not (rtde_c.isConnected() and rtde_r.isConnected()):
        print("Erreur : Impossible de se connecter au robot UR5e")
        exit()
except Exception as e:
    print(f"Erreur lors de la connexion au robot: {e}")
    exit()

# Fonction de déplacement simple du robot
def move_robot_to_position(position):
    if rtde_c:
        try:
            rtde_c.moveL(position)
        except Exception as e:
            print(f"Erreur lors du déplacement du robot: {e}")
    else:
        print("Erreur : rtde_c n'est pas initialisé")

# Position cible (x, y, z, rx, ry, rz)
# Exemple : [0.5, 0.0, 0.2, 0, 3.14, 0] pour déplacer le robot à x=0.5m, y=0.0m, z=0.2m
target_position = [1.01,-5.68, -5.67, 0, 0, 0.05]

# Déplacer le robot à la position cible
move_robot_to_position(target_position)

# Libérer les ressources du robot
if rtde_c:
    rtde_c.stopScript()
if rtde_r:
    rtde_r.disconnect()

print("Déplacement terminé")
