// =============================
// MAP
// =============================

let map = L.map('map').setView([10.95, 106.8], 11);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

let points = [];
let markers = [];
let currentPolylines = [];

// =============================
// CLICK ADD POINT
// =============================

map.on('click', function(e) {
    const idx = points.length;

    points.push([e.latlng.lat, e.latlng.lng]);

    let icon;

    if (idx === 0) {
        icon = new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41]
        });
    } else {
        icon = new L.Icon.Default();
    }

    const marker = L.marker(e.latlng, {icon})
        .addTo(map)
        .bindTooltip(idx === 0 ? '🏠 Kho (P0)' : `P${idx}`, {permanent: true});

    markers.push(marker);

    document.getElementById('status').textContent = `${points.length} điểm`;
    document.getElementById('result').innerHTML = '';
});

// =============================
// GET REAL ROUTE
// =============================

async function getRealRoute(p1, p2) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    try {
        const url = `https://router.project-osrm.org/route/v1/driving/${p1[1]},${p1[0]};${p2[1]},${p2[0]}?overview=full&geometries=geojson`;

        const res = await fetch(url, {signal: controller.signal});
        const data = await res.json();

        if (data.routes && data.routes[0]) {
            return {
                distance: data.routes[0].distance,
                geometry: data.routes[0].geometry
            };
        }
    } catch (e) {
        console.log('OSRM ERROR', e);
        return null;
    } finally {
        clearTimeout(timeoutId);
    }
}

// =============================
// RUN GA
// =============================

async function runGA() {
    if (points.length < 3) {
        const modal = new bootstrap.Modal(document.getElementById('warningModal'));
        modal.show();
        return;
    }

    const btn = document.getElementById('btn-run');
    const result = document.getElementById('result');

    btn.disabled = true;
    result.innerHTML = '';

    currentPolylines.forEach(p => p.remove());
    currentPolylines = [];

    try {
        const res = await fetch('/optimize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({points})
        });

        const data = await res.json();

        if (data.error) {
            throw new Error(data.error);
        }

        console.log('Response data:', data);

        const distKm = (data.best_distance / 1000).toFixed(2);
        const routeStr = data.best_route.map(i => `P${i}`).join(' → ') + ` → P${data.best_route[0]}`;
        const pointsCount = data.points_count || data.best_route.length;

        const legs = (data.route_distances || []).map((d, idx) => {
            const from = `P${data.best_route[idx]}`;
            const to = `P${data.best_route[(idx + 1) % data.best_route.length]}`;
            return `<li class="mb-1">${from} → ${to}: <strong>${(d/1000).toFixed(2)} km</strong></li>`;
        }).join('');

        result.innerHTML = `
            <div class="d-flex align-items-start gap-3">
                <div style="font-size:1.6rem;">✅</div>
                <div>
                    <div class="fw-semibold mb-2">Hoàn thành</div>
                    <div class="small text-muted">Tổng quan</div>
                    <ul class="list-unstyled mt-2 mb-2">
                        <li>Số điểm: <strong>${pointsCount}</strong></li>
                        <li>Tổng khoảng cách: <strong>${distKm} km</strong></li>
                    </ul>
                    <div class="map-note small text-muted mb-1">Lộ trình</div>
                    <div class="mb-2">${routeStr}</div>
                    <div class="map-note small text-muted mb-1">Khoảng cách từng đoạn</div>
                    <ul class="ps-3 small">${legs}</ul>
                </div>
            </div>
        `;

        drawRealRoads(data.best_route).catch(err => console.log('DRAW ERROR', err));

    } catch (err) {
        result.innerHTML = `❌ Lỗi: ${err.message}`;
    } finally {
        btn.disabled = false;
    }
}

// =============================
// DRAW ROAD
// =============================

async function drawRealRoads(route) {
    const colors = ['#2196F3', '#E91E63', '#FF9800', '#4CAF50', '#9C27B0'];

    for (let i = 0; i < route.length; i++) {
        const from = points[route[i]];
        const to = points[route[(i + 1) % route.length]];
        const color = colors[i % colors.length];

        const routeData = await getRealRoute(from, to);

        if (routeData && routeData.geometry) {
            const coords = routeData.geometry.coordinates.map(c => [c[1], c[0]]);
            const poly = L.polyline(coords, {color, weight: 6, opacity: 0.85}).addTo(map);
            currentPolylines.push(poly);
        } else {
            const poly = L.polyline([from, to], {color: 'red', dashArray: '8,6'}).addTo(map);
            currentPolylines.push(poly);
        }
    }

    if (currentPolylines.length > 0) {
        const group = L.featureGroup(currentPolylines);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

// =============================
// CLEAR
// =============================

function clearAll() {
    points = [];
    markers.forEach(m => m.remove());
    currentPolylines.forEach(p => p.remove());
    markers = [];
    currentPolylines = [];

    document.getElementById('status').textContent = '0 điểm';
    document.getElementById('result').innerHTML = '';
}
