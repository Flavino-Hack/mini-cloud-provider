from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import docker
import uuid
import os

app = FastAPI(title="Mini Cloud Provider API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = docker.from_env()
NETWORK_NAME = os.getenv("DOCKER_NETWORK_NAME", "mini-cloud-provider_vps-network")

class VPSCreate(BaseModel):
    name: str
    ram_mb: int
    cpu_limit: float
    storage_gb: int
    username: str  # NOUVEAU : Nom d'utilisateur défini par le client
    password: str  # NOUVEAU : Mot de passe défini par le client

class VPSResponse(BaseModel):
    id: str
    name: str
    status: str
    url: str
    ram_mb: int
    cpu_limit: float
    storage_gb: int
    username: str  # NOUVEAU
    password: str  # NOUVEAU

vps_registry = {}

@app.get("/")
async def root():
    return {"message": "Mini Cloud Provider API", "status": "running"}

@app.post("/vps/create", response_model=VPSResponse)
async def create_vps(vps_data: VPSCreate):
    vps_id = str(uuid.uuid4())[:8]
    container_name = f"vps-{vps_data.name}-{vps_id}"
    volume_name = f"{container_name}-data"
    
    try:
        # 1. Création du volume de stockage persistant
        client.volumes.create(name=volume_name, driver="local")
        
        # 2. Création du conteneur avec les identifiants personnalisés du client
        container = client.containers.run(
            "mini-cloud-provider_vps-base",
            name=container_name,
            user="root",
            detach=True,
            tty=True,
            mem_limit=f"{vps_data.ram_mb}m",
            cpu_quota=int(vps_data.cpu_limit * 100000),
            cpu_period=100000,
            network=NETWORK_NAME,
            volumes={volume_name: {'bind': '/data', 'mode': 'rw'}},
            ports={'7681/tcp': None},
            labels={
                "vps.id": vps_id,
                "vps.name": vps_data.name,
                "vps.ram": str(vps_data.ram_mb),
                "vps.cpu": str(vps_data.cpu_limit),
                "vps.storage": str(vps_data.storage_gb),
                "vps.username": vps_data.username,
                "vps.password": vps_data.password
            },
            # 🔒 Utilise les identifiants fournis par le client
            command=f"ttyd -p 7681 -c '{vps_data.username}:{vps_data.password}' -W bash -c 'echo \"\\033[1;32m================================================\\033[0m\" && echo \"\\033[1;32m  Bienvenue sur votre VPS Root (Démo Portfolio)\\033[0m\" && echo \"\\033[1;32m  Ressources: {vps_data.cpu_limit} vCPU / {vps_data.ram_mb}MB RAM / {vps_data.storage_gb}GB Storage\\033[0m\" && echo \"\\033[1;32m================================================\\033[0m\" && echo \"\\033[1;33m  🔒 Connectez-vous avec vos identifiants personnalisés\\033[0m\" && exec bash'"
        )
        
        # 3. Récupérer le port réel attribué par Docker sur l'hôte
        container.reload()
        host_port = container.attrs['NetworkSettings']['Ports']['7681/tcp'][0]['HostPort']
        
        # 4. Générer l'URL magique avec nip.io
        direct_url = f"http://{vps_data.name}.127.0.0.1.nip.io:{host_port}"
        
        vps_registry[vps_id] = {
            "id": vps_id,
            "name": vps_data.name,
            "container_id": container.id,
            "status": "running",
            "ram_mb": vps_data.ram_mb,
            "cpu_limit": vps_data.cpu_limit,
            "storage_gb": vps_data.storage_gb,
            "url": direct_url,
            "username": vps_data.username,
            "password": vps_data.password
        }
        
        return VPSResponse(
            id=vps_id, name=vps_data.name, status="running",
            url=direct_url,
            ram_mb=vps_data.ram_mb, cpu_limit=vps_data.cpu_limit, storage_gb=vps_data.storage_gb,
            username=vps_data.username, password=vps_data.password
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création VPS: {str(e)}")

@app.get("/vps/list")
async def list_vps():
    active_vps = []
    for vps_id, vps_info in list(vps_registry.items()):
        try:
            container = client.containers.get(vps_info['container_id'])
            stats = container.stats(stream=False)
            
            mem_usage = stats['memory_stats'].get('usage', 0) / (1024 * 1024)
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats'].get('system_cpu_usage', 1) - stats['precpu_stats'].get('system_cpu_usage', 1)
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [1])) * 100 if system_delta > 0 else 0.0
            
            active_vps.append({
                "id": vps_id,
                "name": vps_info['name'],
                "status": container.status,
                "url": vps_info['url'],
                "ram_usage_mb": round(mem_usage, 2),
                "ram_limit_mb": vps_info['ram_mb'],
                "cpu_percent": round(cpu_percent, 2),
                "cpu_limit": vps_info['cpu_limit'],
                "storage_gb": vps_info['storage_gb'],
                "username": vps_info['username'],
                "password": vps_info['password']
            })
        except:
            if vps_id in vps_registry:
                del vps_registry[vps_id]
    
    return {"vps": active_vps}

@app.get("/admin/stats")
async def admin_stats():
    """Dashboard Administrateur : Vue globale de l'hôte"""
    try:
        info = client.info()
        total_vps = len(vps_registry)
        running_vps = sum(1 for v in vps_registry.values() if v['status'] == 'running')
        
        return {
            "host_cpu_threads": info.get('NCPU', 0),
            "total_vps": total_vps,
            "running_vps": running_vps,
            "docker_version": info.get('ServerVersion', 'Unknown')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vps/{vps_id}/stop")
async def stop_vps(vps_id: str):
    if vps_id not in vps_registry:
        raise HTTPException(status_code=404, detail="VPS non trouvé")
    try:
        container = client.containers.get(vps_registry[vps_id]['container_id'])
        container.stop()
        vps_registry[vps_id]['status'] = 'stopped'
        return {"message": "VPS arrêté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vps/{vps_id}/start")
async def start_vps(vps_id: str):
    if vps_id not in vps_registry:
        raise HTTPException(status_code=404, detail="VPS non trouvé")
    try:
        container = client.containers.get(vps_registry[vps_id]['container_id'])
        container.start()
        vps_registry[vps_id]['status'] = 'running'
        return {"message": "VPS démarré avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/vps/{vps_id}")
async def delete_vps(vps_id: str):
    if vps_id not in vps_registry:
        raise HTTPException(status_code=404, detail="VPS non trouvé")
    try:
        container = client.containers.get(vps_registry[vps_id]['container_id'])
        container.stop()
        container.remove()
        
        # Supprimer le volume associé pour libérer l'espace disque
        volume_name = f"vps-{vps_registry[vps_id]['name']}-{vps_id}-data"
        try:
            client.volumes.get(volume_name).remove()
        except:
            pass
            
        del vps_registry[vps_id]
        return {"message": "VPS et stockage supprimés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Vérifie que l'API et Docker fonctionnent correctement"""
    try:
        client.ping()
        return {"status": "healthy", "docker": "connected", "network": NETWORK_NAME}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}