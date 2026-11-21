<div align="center">

<!-- Logo du projet -->
<img src="docs/logo.png" alt="Mini Cloud Provider Logo" width="150"/>

# 🚀 Mini Cloud Provider

### Infrastructure Cloud Virtualisée Automatisée

**Déployez, gérez et contrôlez des VPS isolés avec allocation dynamique de ressources depuis une interface web moderne.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[Demo](#-demo) • [Installation](#-installation) • [Architecture](#-architecture) • [Fonctionnalités](#-fonctionnalités)

</div>

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies](#-technologies-utilisées)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Ce que ce projet démontre](#-ce-que-ce-projet-démontre)
- [Améliorations futures](#-améliorations-futures)

---

## 🎯 Vue d'ensemble

**Mini Cloud Provider** est un projet de démonstration qui simule un fournisseur de VPS (Virtual Private Server) complet, permettant de déployer des conteneurs Linux isolés avec des ressources strictement limitées (CPU, RAM, Stockage) via une interface web moderne.

Chaque VPS est un conteneur Docker indépendant avec :
- ✅ Accès root sécurisé par authentification
- ✅ Stockage persistant via volumes Docker
- ✅ Terminal web intégré (ttyd)
- ✅ Monitoring en temps réel des ressources
- ✅ Isolation complète (namespaces, cgroups)

---

## ✨ Fonctionnalités

### Pour les Clients (Utilisateurs)
- 🚀 **Déploiement instantané** : Création de VPS en moins de 3 secondes
- 🔐 **Authentification personnalisée** : Définissez vos propres identifiants root
- 📊 **Monitoring temps réel** : Visualisez l'utilisation CPU/RAM de votre VPS
- 💾 **Stockage persistant** : Volumes Docker de 1 à 15 Go
- 🖥️ **Terminal web intégré** : Accédez à votre VPS directement depuis le navigateur
- 🎮 **Environnement complet** : Installez et exécutez n'importe quel logiciel (Python, Node.js, bases de données, etc.)

### Pour l'Administrateur
- 📈 **Dashboard global** : Vue d'ensemble de tous les VPS et de l'hôte
- 🎛️ **Contrôle total** : Démarrer, arrêter, supprimer des VPS
- 🔍 **Monitoring avancé** : Statistiques détaillées de chaque conteneur
- 🗑️ **Nettoyage automatique** : Suppression des volumes orphelins

---

## 🏗️ Architecture

<div align="center">

![Architecture Diagram](docs/architecture.png)

</div>

### Flux de données

1. **Frontend (HTML/CSS/JS)** : Interface utilisateur moderne et responsive
2. **Backend (FastAPI)** : API REST qui orchestre la création et la gestion des VPS
3. **Docker Engine** : Crée et isole les conteneurs avec des limites strictes (cgroups)
4. **Conteneurs VPS** : Images Debian avec ttyd préinstallé pour l'accès terminal web
5. **Volumes Docker** : Stockage persistant monté sur `/data` dans chaque VPS

---

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.11+** : Langage principal
- **FastAPI** : Framework web moderne et ultra-rapide
- **Docker SDK for Python** : Orchestration des conteneurs
- **Uvicorn** : Serveur ASGI

### Frontend
- **HTML5 / CSS3 / JavaScript (Vanilla)** : Interface utilisateur sans dépendances
- **Fetch API** : Communication avec le backend

### Infrastructure
- **Docker** : Conteneurisation et isolation
- **Docker Compose** : Orchestration multi-conteneurs
- **ttyd** : Terminal web (accès root via navigateur)
- **nip.io** : Résolution DNS magique pour les URLs locales

---

## 🚀 Installation

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et en cours d'exécution
- [Git](https://git-scm.com/) (optionnel, pour cloner le projet)

### Étapes d'installation

1. **Cloner le repository** (ou télécharger le ZIP) :
   ```bash
   git clone https://github.com/votre-username/mini-cloud-provider.git
   cd mini-cloud-provider

2. Construire l'image de base des VPS (avec ttyd préinstallé)

docker build -t mini-cloud-provider_vps-base ./vps-base

3. Construire et lancer tous les services 

docker-compose up --build

4. Accéder à l'interface :
Frontend : http://localhost:3000
API Backend : http://localhost:8000
Documentation API (Swagger) : http://localhost:8000/docs

📖 Utilisation
1. Créer un VPS
Ouvrez http://localhost:3000 dans votre navigateur
Remplissez le formulaire :
Nom : mon-premier-vps
RAM : 1 Go
vCPU : 1
Stockage : 5 GB
Nom d'utilisateur : admin
Mot de passe : MonMotDePasse123!
Cliquez sur "⚡ Déployer le VPS"

2. Accéder au Terminal Web
Sur la carte du VPS, cliquez sur "🖥️ Ouvrir le Terminal Web"
Une fenêtre d'authentification apparaît : entrez vos identifiants
Vous êtes maintenant connecté en root à votre VPS !
3. Utiliser votre VPS
Exemple de commandes à exécuter dans le terminal :

# Vérifier les ressources allouées
free -h
df -h /data

# Installer Python
apt-get update && apt-get install -y python3

# Créer un script de monitoring
cat > /data/monitor.py << 'EOF'
import time
from datetime import datetime

while True:
    print(f"[{datetime.now()}] VPS actif")
    time.sleep(5)
EOF

# Lancer le script
python3 /data/monitor.py &


4. Mode Administrateur
Cliquez sur "🔒 Passer en Mode Administrateur" pour voir :
Nombre de cœurs de l'hôte
Nombre total de VPS
Nombre de VPS actifs
🎯 Ce que ce projet démontre
Compétences Techniques
✅ Maîtrise de Docker :
Utilisation avancée de l'API Docker (SDK Python)
Gestion des conteneurs, réseaux, volumes
Limitation de ressources via cgroups (CPU, RAM)
Isolation complète (namespaces)
✅ Développement Backend :
API REST complète avec FastAPI
Gestion d'état et persistance
Documentation automatique (Swagger/OpenAPI)
✅ Développement Frontend :
Interface utilisateur moderne et responsive
Communication asynchrone avec l'API
Monitoring en temps réel
✅ Infrastructure as Code :
Docker Compose pour l'orchestration
Automatisation du provisioning
Gestion du cycle de vie des VPS
✅ Sécurité :
Authentification par utilisateur
Isolation des conteneurs
Pas d'exposition inutile de ports
Compétences Transversales
✅ Résolution de problèmes complexes : Debugging Docker sur Windows/WSL2
✅ Architecture logicielle : Séparation des responsabilités (frontend/backend/infrastructure)
✅ Documentation technique : README complet et professionnel
✅ Déploiement : Projet 100% fonctionnel et reproductible
🔮 Améliorations Futures
Base de données : Remplacer le registre en mémoire par PostgreSQL
Authentification utilisateurs : Système de comptes clients avec JWT
Templates de VPS : Images pré-configurées (WordPress, Node.js, PostgreSQL)
Monitoring avancé : Intégration Prometheus + Grafana
Système de facturation : Intégration Stripe pour la facturation automatique
Déploiement cloud : Version déployée sur AWS/DigitalOcean
SSH natif : Accès SSH en plus du terminal web
Backup automatique : Snapshots des volumes Docker


🎥 Vidéo de Démonstration
🚧 Bientôt disponible : Une vidéo de 2 minutes montrant le projet en action
📄 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
👤 Auteur
[Votre Nom]
Développeur Fullstack & Passionné de Cloud
GitHub : @votre-username
LinkedIn : Votre Profil
Portfolio : votre-site.com
🙏 Remerciements
FastAPI pour le framework backend exceptionnel
Docker pour la technologie de conteneurisation
ttyd pour le terminal web
nip.io pour la résolution DNS magique
<div align="center">

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !



