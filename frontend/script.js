const API_URL = 'http://localhost:8000';
let isAdmin = false;

document.addEventListener('DOMContentLoaded', () => {
    loadVPSList();
    setInterval(loadVPSList, 5000);
    if(isAdmin) loadAdminStats();
});

function toggleAdmin() {
    isAdmin = !isAdmin;
    const btn = document.getElementById('admin-toggle');
    const dashboard = document.getElementById('admin-dashboard');
    
    if (isAdmin) {
        btn.textContent = '👤 Passer en Mode Client';
        btn.classList.add('active');
        dashboard.style.display = 'block';
        loadAdminStats();
    } else {
        btn.textContent = '🔒 Passer en Mode Administrateur';
        btn.classList.remove('active');
        dashboard.style.display = 'none';
    }
}

async function loadAdminStats() {
    if (!isAdmin) return;
    try {
        const res = await fetch(`${API_URL}/admin/stats`);
        const data = await res.json();
        document.getElementById('host-cpu').textContent = data.host_cpu_threads + ' Threads';
        document.getElementById('total-vps').textContent = data.total_vps;
        document.getElementById('running-vps').textContent = data.running_vps;
    } catch (e) { console.error("Erreur stats admin", e); }
}

document.getElementById('create-vps-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.textContent = '⏳ Déploiement en cours...';
    btn.disabled = true;

    try {
        const res = await fetch(`${API_URL}/vps/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: document.getElementById('vps-name').value,
                ram_mb: parseInt(document.getElementById('vps-ram').value),
                cpu_limit: parseFloat(document.getElementById('vps-cpu').value),
                storage_gb: parseInt(document.getElementById('vps-storage').value),
                username: document.getElementById('vps-username').value,
                password: document.getElementById('vps-password').value
            })
        });
        
        if (!res.ok) throw new Error('Échec du déploiement');
        
        document.getElementById('create-vps-form').reset();
        loadVPSList();
        if(isAdmin) loadAdminStats();
        alert('✅ VPS déployé avec succès !');
    } catch (error) {
        alert('Erreur: ' + error.message);
    } finally {
        btn.textContent = '⚡ Déployer le VPS';
        btn.disabled = false;
    }
});

async function loadVPSList() {
    try {
        const res = await fetch(`${API_URL}/vps/list`);
        const data = await res.json();
        const container = document.getElementById('vps-container');
        const noVps = document.getElementById('no-vps');
        
        if (data.vps.length === 0) {
            container.innerHTML = '';
            noVps.style.display = 'block';
            return;
        }
        
        noVps.style.display = 'none';
        container.innerHTML = data.vps.map(vps => `
            <div class="vps-card">
                <div class="vps-header">
                    <div class="vps-name">${vps.name}</div>
                    <div class="vps-status status-${vps.status}">${vps.status}</div>
                </div>
                <div class="vps-info">
                    <div class="info-row"><span class="info-label">RAM</span><span class="info-value">${vps.ram_usage_mb.toFixed(1)} / ${vps.ram_limit_mb} MB</span></div>
                    <div class="progress-bar"><div class="progress-fill" style="width: ${Math.min((vps.ram_usage_mb/vps.ram_limit_mb)*100, 100)}%"></div></div>
                    <div class="info-row" style="margin-top:10px;"><span class="info-label">CPU</span><span class="info-value">${vps.cpu_percent.toFixed(1)}% / ${vps.cpu_limit} vCPU</span></div>
                    <div class="progress-bar"><div class="progress-fill" style="width: ${Math.min(vps.cpu_percent, 100)}%"></div></div>
                    <div class="info-row" style="margin-top:10px;"><span class="info-label">💾 Stockage</span><span class="info-value">${vps.storage_gb} GB (Volume Persistant)</span></div>
                    <div class="info-row" style="margin-top:10px;"><span class="info-label">🔐 Identifiants</span><span class="info-value">${vps.username} / ${vps.password}</span></div>
                </div>
                <div class="vps-actions">
                    ${vps.status === 'running' 
                        ? `<button class="btn-small btn-stop" onclick="controlVPS('${vps.id}', 'stop')">Arrêter</button>`
                        : `<button class="btn-small btn-start" onclick="controlVPS('${vps.id}', 'start')">Démarrer</button>`
                    }
                    <button class="btn-small btn-delete" onclick="controlVPS('${vps.id}', 'delete')">Supprimer</button>
                </div>
                ${vps.status === 'running' ? `<a href="${vps.url}" target="_blank" class="btn-terminal">🖥️ Ouvrir le Terminal Web</a>` : ''}
            </div>
        `).join('');
    } catch (error) { console.error('Erreur chargement VPS:', error); }
}

async function controlVPS(vpsId, action) {
    if (action === 'delete' && !confirm('Supprimer définitivement ce VPS et ses données ?')) return;
    
    const method = action === 'delete' ? 'DELETE' : 'POST';
    const url = action === 'delete' ? `${API_URL}/vps/${vpsId}` : `${API_URL}/vps/${vpsId}/${action}`;
    
    try {
        await fetch(url, { method });
        loadVPSList();
        if(isAdmin) loadAdminStats();
    } catch (error) { alert('Erreur: ' + error.message); }
}