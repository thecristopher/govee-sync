# 🖥️ Govee Sync Desktop

Sincroniza dinámicamente tus luces Govee con el color promedio de tu monitor en Linux (GNOME + Wayland).

## ⚙️ Requisitos

- Python 3.10+
- `gnome-screenshot`
- Paquetes:
  - `Pillow`
  - `govee-api-laggat`

## 🚀 Uso

1. Clona el repo.
2. Crea un entorno virtual.
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta el script: `python govee_sync_desktop.py`

## 📸 Limitaciones

Por ahora, la sincronización depende de capturas usando `gnome-screenshot`, lo que produce un destello leve. Una futura versión usará PipeWire.

