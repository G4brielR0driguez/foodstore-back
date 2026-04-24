"""
Script de test completo para la FoodStore API.
Testea todos los endpoints CRUD de Categorías, Ingredientes y Productos.
"""
import httpx
import sys

BASE = "http://127.0.0.1:8000"
PASS = "✅"
FAIL = "❌"
errors = []

def check(label, response, expected_status):
    ok = response.status_code == expected_status
    icon = PASS if ok else FAIL
    print(f"  {icon} {label} → HTTP {response.status_code}", end="")
    if not ok:
        print(f" (esperado {expected_status}) | body: {response.text[:120]}")
        errors.append(label)
    else:
        try:
            data = response.json()
            if isinstance(data, dict):
                print(f" | id={data.get('id', '?')} nombre={data.get('nombre', '')}")
            elif isinstance(data, list):
                print(f" | {len(data)} elemento(s)")
            else:
                print()
        except Exception:
            print()
    return response

client = httpx.Client(base_url=BASE, timeout=10)

# ─────────────────────────────────────────────
print("\n📦 CATEGORÍAS")
print("─" * 50)

# Crear categoría raíz
r = check("POST /categorias (pizza)", client.post("/categorias", json={
    "nombre": "Pizzas",
    "descripcion": "Pizzas artesanales",
    "imagen_url": "https://example.com/pizza.jpg"
}), 201)
cat_id = r.json().get("id") if r.status_code == 201 else None

# Crear subcategoría
r2 = check("POST /categorias (subcategoría)", client.post("/categorias", json={
    "nombre": "Pizzas Vegetarianas",
    "parent_id": cat_id
}), 201)
subcat_id = r2.json().get("id") if r2.status_code == 201 else None

# Listar
check("GET /categorias", client.get("/categorias"), 200)
check("GET /categorias?solo_raiz=true", client.get("/categorias?solo_raiz=true"), 200)
check("GET /categorias?nombre=pizza", client.get("/categorias?nombre=pizza"), 200)

# Obtener por ID
if cat_id:
    check(f"GET /categorias/{cat_id}", client.get(f"/categorias/{cat_id}"), 200)

# Actualizar
if cat_id:
    check(f"PATCH /categorias/{cat_id}", client.patch(f"/categorias/{cat_id}", json={
        "descripcion": "Pizzas artesanales actualizadas"
    }), 200)

# Error 404
check("GET /categorias/99999 (404)", client.get("/categorias/99999"), 404)

# Error nombre duplicado
check("POST /categorias duplicada (400)", client.post("/categorias", json={
    "nombre": "Pizzas"
}), 400)

# ─────────────────────────────────────────────
print("\n🌿 INGREDIENTES")
print("─" * 50)

r = check("POST /ingredientes (mozzarella)", client.post("/ingredientes", json={
    "nombre": "Mozzarella",
    "descripcion": "Queso mozzarella fresco",
    "es_alergeno": False
}), 201)
ing1_id = r.json().get("id") if r.status_code == 201 else None

r = check("POST /ingredientes (gluten)", client.post("/ingredientes", json={
    "nombre": "Gluten",
    "descripcion": "Proteína del trigo",
    "es_alergeno": True
}), 201)
ing2_id = r.json().get("id") if r.status_code == 201 else None

check("GET /ingredientes", client.get("/ingredientes"), 200)
check("GET /ingredientes?solo_alergenos=true", client.get("/ingredientes?solo_alergenos=true"), 200)
check("GET /ingredientes?nombre=moz", client.get("/ingredientes?nombre=moz"), 200)

if ing1_id:
    check(f"GET /ingredientes/{ing1_id}", client.get(f"/ingredientes/{ing1_id}"), 200)
    check(f"PATCH /ingredientes/{ing1_id}", client.patch(f"/ingredientes/{ing1_id}", json={
        "descripcion": "Queso mozzarella premium"
    }), 200)

check("GET /ingredientes/99999 (404)", client.get("/ingredientes/99999"), 404)
check("POST /ingredientes duplicado (400)", client.post("/ingredientes", json={
    "nombre": "Mozzarella"
}), 400)

# ─────────────────────────────────────────────
print("\n🍕 PRODUCTOS")
print("─" * 50)

categoria_ids = [cat_id] if cat_id else []
ingrediente_ids = [i for i in [ing1_id, ing2_id] if i]

r = check("POST /productos", client.post("/productos", json={
    "nombre": "Pizza Margherita",
    "descripcion": "Clásica pizza con tomate y mozzarella",
    "precio_base": "12.50",
    "imagenes_url": ["https://example.com/margherita.jpg"],
    "stock_cantidad": 50,
    "disponible": True,
    "categoria_ids": categoria_ids,
    "ingrediente_ids": ingrediente_ids
}), 201)
prod_id = r.json().get("id") if r.status_code == 201 else None

r2 = check("POST /productos (segundo)", client.post("/productos", json={
    "nombre": "Pizza Napolitana",
    "precio_base": "14.00",
    "categoria_ids": categoria_ids,
}), 201)
prod2_id = r2.json().get("id") if r2.status_code == 201 else None

check("GET /productos", client.get("/productos"), 200)
check("GET /productos?disponible=true", client.get("/productos?disponible=true"), 200)
check("GET /productos?nombre=pizza", client.get("/productos?nombre=pizza"), 200)
check("GET /productos?precio_min=10&precio_max=13", client.get("/productos?precio_min=10&precio_max=13"), 200)
check("GET /productos?skip=0&limit=1", client.get("/productos?skip=0&limit=1"), 200)

if prod_id:
    check(f"GET /productos/{prod_id}", client.get(f"/productos/{prod_id}"), 200)
    check(f"PATCH /productos/{prod_id} (stock)", client.patch(f"/productos/{prod_id}", json={
        "stock_cantidad": 45,
        "disponible": True
    }), 200)

check("GET /productos/99999 (404)", client.get("/productos/99999"), 404)
check("POST /productos sin categoria (422 validacion)", client.post("/productos", json={
    "nombre": "Sin categoria",
    "precio_base": "5.00",
    "categoria_ids": []
}), 422)
check("POST /productos categoria inexistente (404)", client.post("/productos", json={
    "nombre": "Error cat",
    "precio_base": "5.00",
    "categoria_ids": [99999]
}), 404)

# ─────────────────────────────────────────────
print("\n🗑  ELIMINACIONES (limpieza)")
print("─" * 50)

if prod2_id:
    check(f"DELETE /productos/{prod2_id}", client.delete(f"/productos/{prod2_id}"), 204)
if prod_id:
    check(f"DELETE /productos/{prod_id}", client.delete(f"/productos/{prod_id}"), 204)
if ing1_id:
    check(f"DELETE /ingredientes/{ing1_id}", client.delete(f"/ingredientes/{ing1_id}"), 204)
if ing2_id:
    check(f"DELETE /ingredientes/{ing2_id}", client.delete(f"/ingredientes/{ing2_id}"), 204)
if subcat_id:
    check(f"DELETE /categorias/{subcat_id}", client.delete(f"/categorias/{subcat_id}"), 204)
if cat_id:
    check(f"DELETE /categorias/{cat_id}", client.delete(f"/categorias/{cat_id}"), 204)

check("DELETE /categorias/99999 (404)", client.delete("/categorias/99999"), 404)

# ─────────────────────────────────────────────
print()
print("=" * 50)
if errors:
    print(f"❌ {len(errors)} test(s) fallaron:")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)
else:
    print(f"✅ Todos los tests pasaron correctamente")
