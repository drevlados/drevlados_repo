import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, Point, box, MultiPolygon
from shapely.ops import unary_union
import noise
from scipy.spatial import Voronoi
# ------------------------------------------------------------------
# ИМПОРТ ДАННЫХ (с приложения)
# ------------------------------------------------------------------
with open('map_gen_file.txt', 'r', encoding='UTF-8') as file:
    params = file.readlines()
# ------------------------------------------------------------------
# КОНФИГУРАЦИЯ (параметры города)
# ------------------------------------------------------------------
WIDTH, HEIGHT = int(params[0]), int(params[1])
AREA_KM2 = (WIDTH * HEIGHT) / 1e6
TARGET_POPULATION = int(params[2])
PEOPLE_PER_HOUSE_SINGLE = int(params[3])
PEOPLE_PER_HOUSE_MULTI = int(params[4])

N_RINGS = int(params[5])
N_RADIALS = int(params[6])
GRID_SPACING = int(params[7])
STREET_WIDTH_MAIN = 28
STREET_WIDTH_SECOND = 18
STREET_WIDTH_LOCAL = 12
BLOCK_MARGIN = 8

SEED = 42
np.random.seed(SEED)

# ------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ------------------------------------------------------------------
def perlin_shape(center, radius, octaves=4, persistence=0.5, lacunarity=2.0):
    angles = np.linspace(0, 2*np.pi, 120)
    points = []
    scale = 1.0 / (radius * 0.8)
    for a in angles:
        x = center[0] + radius * np.cos(a)
        y = center[1] + radius * np.sin(a)
        val = noise.pnoise2(
            x * scale, y * scale,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            repeatx=2048, repeaty=2048,
            base=SEED
        )
        r_mod = radius * (0.7 + 0.6 * val)
        points.append((center[0] + r_mod * np.cos(a), center[1] + r_mod * np.sin(a)))
    return Polygon(points)

def make_l_house(base_w, base_h, margin=4):
    w, h = base_w, base_h
    cut_w = np.random.uniform(w*0.3, w*0.6)
    cut_h = np.random.uniform(h*0.3, h*0.6)
    pts = [
        (margin, margin),
        (w - margin, margin),
        (w - margin, h - margin),
        (margin + cut_w, h - margin),
        (margin + cut_w, margin + cut_h),
        (margin, margin + cut_h)
    ]
    return Polygon(pts)

def place_houses_in_block(block_poly, n_houses, is_multi=False, margin=BLOCK_MARGIN):
    minx, miny, maxx, maxy = block_poly.bounds
    w_avail = maxx - minx - 2*margin
    h_avail = maxy - miny - 2*margin
    if w_avail < 20 or h_avail < 20:
        return []
    houses = []

    if is_multi:
        base_w_range = (35, 55)
        base_h_range = (40, 70)
        n_houses = max(1, int(n_houses * 1.5))
    else:
        base_w_range = (16, 28)
        base_h_range = (20, 36)

    placed = 0
    attempts = 0
    max_attempts = n_houses * 25
    while placed < n_houses and attempts < max_attempts:
        attempts += 1
        w = np.random.uniform(*base_w_range)
        h = np.random.uniform(*base_h_range)
        x = np.random.uniform(minx+margin, maxx-margin-w)
        y = np.random.uniform(miny+margin, maxy-margin-h)
        cand = Polygon([(x,y), (x+w,y), (x+w,y+h), (x,y+h)])
        if np.random.rand() < 0.25:
            cand = make_l_house(w, h, margin=margin)
        ok = True
        for h_prev in houses:
            if cand.intersects(h_prev.buffer(2)):
                ok = False
                break
        if ok and block_poly.contains(cand.buffer(-0.1)):
            houses.append(cand)
            placed += 1
    return houses

def line_to_thick_poly(line, width):
    return line.buffer(width/2, cap_style=2, join_style=2)

def draw_geometry(geom, ax, **kwargs):
    """Универсальная отрисовка геометрии Shapely"""
    if geom.is_empty:
        return
    if geom.geom_type == 'Polygon':
        ax.fill(*geom.exterior.xy, **kwargs)
        for interior in geom.interiors:
            ax.fill(*interior.coords.xy, color='white', zorder=kwargs.get('zorder', 0) + 0.1)
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            draw_geometry(poly, ax, **kwargs)

# ------------------------------------------------------------------
# ДОРОЖНАЯ СЕТЬ
# ------------------------------------------------------------------
center_x, center_y = WIDTH/2, HEIGHT/2
city_box = box(0, 0, WIDTH, HEIGHT)

street_lines = []
street_polys = []

# Кольцевые
for i in range(1, N_RINGS + 1):
    radius = i * (WIDTH / (2 * (N_RINGS + 1)))
    angles = np.linspace(0, 2*np.pi, 300)
    points = [(center_x + radius * np.cos(a), center_y + radius * np.sin(a)) for a in angles]
    ring = LineString(points)
    street_lines.append(ring)
    street_polys.append(line_to_thick_poly(ring, STREET_WIDTH_MAIN))

# Радиальные
for i in range(N_RADIALS):
    angle = 2 * np.pi * i / N_RADIALS
    dir_x = np.cos(angle)
    dir_y = np.sin(angle)
    x_end = center_x + max(WIDTH, HEIGHT) * dir_x
    y_end = center_y + max(WIDTH, HEIGHT) * dir_y
    radial = LineString([(center_x, center_y), (x_end, y_end)]).intersection(city_box)
    if not radial.is_empty and radial.geom_type == 'LineString':
        street_lines.append(radial)
        street_polys.append(line_to_thick_poly(radial, STREET_WIDTH_MAIN))

# Сетка
for y in range(GRID_SPACING, HEIGHT, GRID_SPACING):
    coords = [(x, y + np.sin(x / 800) * 12) for x in np.linspace(0, WIDTH, 50)]
    curved = LineString(coords)
    street_lines.append(curved)
    street_polys.append(line_to_thick_poly(curved, STREET_WIDTH_SECOND))

for x in range(GRID_SPACING, WIDTH, GRID_SPACING):
    coords = [(x + np.cos(y / 800) * 12, y) for y in np.linspace(0, HEIGHT, 50)]
    curved = LineString(coords)
    street_lines.append(curved)
    street_polys.append(line_to_thick_poly(curved, STREET_WIDTH_SECOND))

# Локальные
block_size = GRID_SPACING
for x in range(block_size // 2, WIDTH, block_size):
    for y in range(block_size // 2, HEIGHT, block_size):
        if np.random.rand() < 0.4:
            length = np.random.uniform(60, 180)
            angle = np.random.uniform(0, 2*np.pi)
            x0 = x + np.random.uniform(-50, 50)
            y0 = y + np.random.uniform(-50, 50)
            x1 = x0 + length * np.cos(angle)
            y1 = y0 + length * np.sin(angle)
            local_line = LineString([(x0, y0), (x1, y1)]).intersection(city_box)
            if not local_line.is_empty and local_line.geom_type == 'LineString':
                street_lines.append(local_line)
                street_polys.append(line_to_thick_poly(local_line, STREET_WIDTH_LOCAL))

streets_union = unary_union(street_polys).intersection(city_box)

# ------------------------------------------------------------------
# КВАРТАЛЫ
# ------------------------------------------------------------------
blocks_raw = city_box.difference(streets_union)
if blocks_raw.geom_type == 'MultiPolygon':
    blocks = list(blocks_raw.geoms)
else:
    blocks = [blocks_raw] if not blocks_raw.is_empty else []
blocks = [b for b in blocks if b.area > 100*100]

# ------------------------------------------------------------------
# ПАРКИ
# ------------------------------------------------------------------
parks = []
central_park = perlin_shape((center_x, center_y), radius=380, octaves=5, persistence=0.6)
central_park = central_park.intersection(city_box)
parks.append(central_park)

for b in blocks:
    if np.random.rand() < 0.08 and b.area > 80*80:
        cx, cy = b.centroid.x, b.centroid.y
        r = min(b.area**0.5 * 0.15, 50)
        square = perlin_shape((cx, cy), radius=r, octaves=3, persistence=0.4)
        square = square.intersection(b)
        if not square.is_empty and square.area > 200:
            parks.append(square)

blocks_res = []
for b in blocks:
    rem = b
    for p in parks:
        rem = rem.difference(p)
    if rem.geom_type == 'MultiPolygon':
        blocks_res.extend(list(rem.geoms))
    elif not rem.is_empty:
        blocks_res.append(rem)
blocks = blocks_res

# ------------------------------------------------------------------
# ВОДОЁМ
# ------------------------------------------------------------------
water_polys = []
water_center = (WIDTH*0.7, HEIGHT*0.25)
water_radius = 250
water_base = perlin_shape(water_center, water_radius, octaves=6, persistence=0.7)
water_base = water_base.intersection(city_box)
water_polys.append(water_base)

if len(water_polys) > 0 and not water_polys[0].is_empty:
    island_center = (water_center[0] + np.random.uniform(-50, 50),
                     water_center[1] + np.random.uniform(-50, 50))
    island_radius = water_radius * 0.2
    island = perlin_shape(island_center, island_radius, octaves=4, persistence=0.5)
    island = island.intersection(water_polys[0])
    if not island.is_empty and island.area > 1000:
        water_polys[0] = water_polys[0].difference(island)

# ------------------------------------------------------------------
# ДОМА
# ------------------------------------------------------------------
houses = []
center_pt = Point(center_x, center_y)
block_dists = [Point(b.centroid.x, b.centroid.y).distance(center_pt) for b in blocks]
sorted_idxs = np.argsort(block_dists)
n_multi = max(1, int(len(blocks) * 0.2))
multi_indices = set(sorted_idxs[:n_multi])

for i, b in enumerate(blocks):
    is_multi = i in multi_indices
    if is_multi:
        n_in_block = int(b.area / (45*55) * 1.2)
    else:
        n_in_block = int(b.area / (22*28) * 0.8)
    n_in_block = max(1, min(n_in_block, 20))
    houses.extend(place_houses_in_block(b, n_in_block, is_multi=is_multi, margin=BLOCK_MARGIN))

total_people_est = 0
for h in houses:
    if h.area > 1800:
        total_people_est += PEOPLE_PER_HOUSE_MULTI
    else:
        total_people_est += PEOPLE_PER_HOUSE_SINGLE

if total_people_est > 0:
    scale_factor = TARGET_POPULATION / total_people_est
    houses = []
    for i, b in enumerate(blocks):
        is_multi = i in multi_indices
        if is_multi:
            n_in_block = int((b.area / (45*55) * 1.2) * scale_factor)
        else:
            n_in_block = int((b.area / (22*28) * 0.8) * scale_factor)
        n_in_block = max(1, min(n_in_block, 28))
        houses.extend(place_houses_in_block(b, n_in_block, is_multi=is_multi, margin=BLOCK_MARGIN))

# ------------------------------------------------------------------
# ОТРИСОВКА
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.set_title(f"Процедурная карта города\n"
             f"Площадь: {AREA_KM2:.1f} км², "
             f"Население: ~{TARGET_POPULATION:,} чел.\n"
             f"Кольцевых: {N_RINGS}, Радиальных: {N_RADIALS}, Сетка: {GRID_SPACING} м",
             fontsize=12)

# Вода
for wp in water_polys:
    if wp.is_valid and not wp.is_empty:
        draw_geometry(wp, ax, color="#4a90e2", zorder=1)

# Парки
for p in parks:
    if p.is_valid and not p.is_empty:
        draw_geometry(p, ax, color="#8bc34a", zorder=3)

# Дороги
if not streets_union.is_empty:
    draw_geometry(streets_union, ax, color="#444444", alpha=0.9, zorder=4)

# Дома
for h in houses:
    if h.is_valid and not h.is_empty:
        face = "#f5f5dc"
        edge = "#cccccc"
        lw = 0.5
        if h.area > 1800:
            face = "#d8d8c8"
            edge = "#999999"
            lw = 0.7
        draw_geometry(h, ax, facecolor=face, edgecolor=edge, linewidth=lw, zorder=5)

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("СТАТИСТИКА ГОРОДА")
print("="*60)
print(f"Площадь территории: {AREA_KM2:.2f} км²")
print(f"Целевое население:  {TARGET_POPULATION:,} чел.")
print(f"Количество кварталов: {len(blocks)}")
print(f"Количество домов:     {len(houses)}")
print(f"Количество парков:    {len(parks)}")
print("="*60)
