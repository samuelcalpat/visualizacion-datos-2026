#!/usr/bin/env bash
# =============================================================================
# crear_conflicto.sh — Sesión 2 · Git y GitHub para Ciencia de Datos
#
# Crea un repositorio de práctica llamado demo_conflicto con dos ramas que
# editan LA MISMA LÍNEA de app.py, para que el estudiante provoque y resuelva
# un conflicto de merge con sus propias manos.
#
# Uso (en Git Bash o Terminal):
#     bash crear_conflicto.sh
#     cd demo_conflicto
#     git merge feature/color-alerta        # ← aquí aparece el conflicto
#
# Si ya existe una carpeta demo_conflicto, la borra y la crea de nuevo.
# =============================================================================
set -e

rm -rf demo_conflicto
mkdir demo_conflicto
cd demo_conflicto

git init -q -b main
# identidad local solo para este repo de práctica (no toca la configuración global)
git config user.name  "Estudiante"
git config user.email "estudiante@ejemplo.com"

# --- commit 1: versión base en main --------------------------------------
cat > app.py <<'EOF'
import streamlit as st

titulo = "PM2.5 por hora"
color = "#028090"

st.title(titulo)
st.write("Color del gráfico:", color)
EOF
git add app.py
git commit -q -m "Agrega app.py con título y color base"

# --- rama feature: cambia el color en la MISMA línea ---------------------
git switch -q -c feature/color-alerta
sed -i 's/color = "#028090"/color = "#F96167"/' app.py
git add app.py
git commit -q -m "Cambia color a rojo de alerta"

# --- de vuelta en main: otro cambio en la MISMA línea --------------------
git switch -q main
sed -i 's/color = "#028090"/color = "#00A896"/' app.py
git add app.py
git commit -q -m "Cambia color a verde agua"

echo
echo "Listo. Repositorio de práctica creado en: $(pwd)"
echo
git log --oneline --all --graph
echo
echo "Ahora ejecuta:"
echo "    cd demo_conflicto"
echo "    git merge feature/color-alerta"
echo
echo "Vas a ver: CONFLICT (content): Merge conflict in app.py"
echo "Abre app.py, decide qué color queda, borra las marcas <<< === >>>, y luego:"
echo "    git add app.py"
echo "    git commit -m \"Resuelve conflicto de color\""
