# 🚀 Système de Picking Robotisé

## Introduction

Bienvenue dans notre projet de **Système de Picking Robotisé** ! Ce projet se concentre sur la création d'un système innovant utilisant l'intelligence artificielle et le deep learning pour identifier et sélectionner des objets de manière autonome dans un environnement industriel.

## 🎯 Objectifs du Projet

- **Développer un système de vision artificielle** : Utiliser des caméras et des algorithmes de deep learning pour détecter et identifier les objets.
- **Intégrer un robot de picking** : Créer un robot capable de manipuler divers objets avec précision, en utilisant le deep reinforcement learning pour optimiser les stratégies de picking.
- **Tester et valider le système** : Évaluer les performances et l’efficacité du système dans la Smart Factory de l’Ecole Centrale de Lille.

## 🛠️ Technologies Utilisées

- **Vision par ordinateur** : Caméras et algorithmes de traitement d'image pour la détection d'objets.
- **Capteurs et actionneurs** : Équipements permettant au robot de percevoir son environnement et d'effectuer des mouvements précis.
- **Deep Learning et Deep Reinforcement Learning** : Techniques avancées pour améliorer la précision et l'efficacité des stratégies de picking.
- **Algorithmes de planification de trajectoire** : Calcul des trajectoires optimales pour les mouvements du robot.

## 🏗️ Architecture du Système

<p align="center">
    <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/498f4342-6468-420d-add2-b68cf722bdf4" alt="Architecture du Système" style="width:20%;"/>
</p>

### Composants Principaux

1. **Réseau de caméras** pour la détection et l’identification des objets.
2. **Robot de picking** équipé de capteurs et d’actionneurs pour manipuler les objets.
3. **Système de communication** entre les caméras et le robot pour coordonner les opérations de picking.

## 🧩 System Model

<p align="center">
    <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/0e404db3-ac1a-412a-ae2b-d6c89557e3dc" alt="System Model" style="width:20%;"/>
</p>

## ⚙️ Installation et Configuration

### Configuration Matérielle

1. Installer les caméras et les connecter au réseau.
2. Configurer le robot de picking avec les capteurs et les actionneurs nécessaires.

### Configuration Logicielle

1. Installer les bibliothèques de deep learning :

    ```bash
    pip install tensorflow
    pip install torch
    pip install opencv-python
    pip install numpy
    pip install scipy
    ```

2. Installer la bibliothèque RTD pour la communication avec le robot RTU5 :

    ```bash
    pip install rtd
    ```

3. Configurer les algorithmes de détection d'objets et d'apprentissage par renforcement.
4. Développer les scripts pour la communication entre les caméras et le robot.

### Configuration du Pare-feu

Pour établir une connexion entre le robot et le PC, assurez-vous que les ports nécessaires sont ouverts sur le pare-feu :

1. **Sur Windows** :
    - Ouvrez le Pare-feu Windows avec sécurité avancée.
    - Créez une règle de trafic entrant pour autoriser les ports utilisés par le robot et les caméras.

2. **Sur Linux (UFW)** :

    ```bash
    sudo ufw allow 12345/tcp  # Remplacez 12345 par le port spécifique utilisé
    sudo ufw allow 12345/udp  # Remplacez 12345 par le port spécifique utilisé
    sudo ufw enable
    ```

### Fichiers du Projet

- `main.py` : Code global incluant la détection, la configuration réseau et les scripts de communication.
- `yolo.cfg` : Fichier de configuration pour le modèle YOLO.
- `yolo3.txt` : Fichier texte avec les classes pour YOLO.
- `yolo3.weights` : Poids du modèle YOLO pré-entraîné.
- `rtd_control.py` : Contient la configuration du robot et les fonctions de contrôle.

## 🔍 Classification des Boîtiers

<p align="center">
    <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/8dfb6e06-bf74-4db9-b103-788bc7e29c82" alt="Classification des Boîtiers" style="width:20%;"/>
</p>

Un modèle de machine learning a été entraîné pour différencier les boîtiers avec boutons des boîtiers sans boutons, en utilisant des caractéristiques visuelles telles que la couleur et la forme.

## 🌐 Vérification de la Connectivité

Pour vérifier la connectivité avec le robot, utilisez la commande suivante :

```bash
ping adresse_robot
```
# 🤖 Apprentissage par Renforcement pour le Robot UR5e

Ce projet utilise l'apprentissage par renforcement pour améliorer la précision et l'efficacité des actions du robot UR5e. Nous utilisons le modèle PPO (Proximal Policy Optimization) de la bibliothèque Stable-Baselines3.

## 🚀 Installation

Assurez-vous d'avoir installé les dépendances nécessaires :

```bash
pip install stable-baselines3 gym
```
## 🌟 Définir l'Environnement
Nous avons défini un environnement personnalisé en utilisant la bibliothèque gym pour encapsuler la logique de l'interaction avec le robot et la caméra. L'environnement est défini dans le fichier 'robot_env.py'.

## 📁 Structure du Projet
.
├── README.md          # Documentation
├── main.py            # Script principal
├── rtde_control.py    # Config Robot 
├── robot_env.py       # Définition de l'environnement d'apprentissage par renforcement
└── models
    └── ppo_robot      # Modèle PPO sauvegardé


## ✅ Tests et Validation

Le système sera testé et validé dans la Smart Factory de l’Ecole Centrale de Lille. Les tests comprendront :

- **Détection et identification d’objets** : Validation de la précision des algorithmes de vision par ordinateur.
<p align="center">
    

 <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/f8e8e932-b103-4271-8ad5-d664f3509811" alt="Détection" style="width:15%;"/>
</p>

- **Stratégies de picking** : Optimisation des stratégies de picking à l'aide du deep reinforcement learning.
- **Performance globale** : Évaluation de l’efficacité et de la fiabilité du système dans un environnement industriel réel.
 <p align="center">
    <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/a6c44958-80b1-4c35-ab56-ffdcf9d3b1a7" alt="Performance globale" style="width:15%;"/>
    <img src="https://github.com/ZAKARIA-rgb-spaec/picking-robotis-/assets/126424638/052675e3-8b9e-4e15-9067-254a7e91bcdf" alt="Validation du système" style="width:15%;"/>
 </p>
 
## 🎯 Résultats Attendus

- Amélioration significative de l’efficacité des processus de picking robotisé.
- Réduction des erreurs d’identification et de sélection des objets.
- Démonstration de la faisabilité et des avantages de l’application des techniques de deep learning dans le contexte industriel.

## 👥 Auteurs


- **Zakaria Midine**
- **Zakaria Limi**
- **Lamyae Najih**
- **Superviseur : Dr. A. Rahmani**

## Références

Pour plus de détails, veuillez consulter le rapport complet : [Rapport_ECL_Zakaria_Midine.pdf](https://online.publuu.com/571615/1283441)
