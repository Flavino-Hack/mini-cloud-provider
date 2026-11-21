# vps-base/Dockerfile
FROM debian:bookworm-slim

# Installation de ttyd (Terminal Web) et outils de base
RUN apt-get update && apt-get install -y wget curl htop nano && \
    wget https://github.com/tsl0922/ttyd/releases/download/1.7.4/ttyd.x86_64 -O /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Le point de montage pour le stockage persistant
RUN mkdir -p /data && chmod 777 /data

EXPOSE 7681

# Démarrage automatique du terminal web au lancement du conteneur
CMD ["ttyd", "-p", "7681", "-W", "bash"]

