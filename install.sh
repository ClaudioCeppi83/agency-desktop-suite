#!/bin/bash

# Agency Desktop - Master Installer
# Diseñado para Ubuntu 24.04+ (GTK4/Libadwaita)

set -e

echo "🚀 Iniciando instalación de Agency Desktop..."

# 1. Instalar dependencias del sistema
echo "📦 Instalando dependencias de Python y GTK4..."
sudo apt update
sudo apt install -y python3-gi python3-yaml python3-pip libadwaita-1-0 gir1.2-adw-1

# 2. Configurar estructura de directorios
echo "📂 Configurando directorios de Gemini CLI..."
mkdir -p ~/.gemini/extensions/agency-agents/{skills,custom}
mkdir -p ~/.config/agency-manager

# 3. Clonar y preparar agentes de The Agency
if [ ! -d "/tmp/agency-agents-temp" ]; then
    echo "📥 Descargando biblioteca de agentes (The Agency)..."
    git clone https://github.com/msitarzewski/agency-agents.git /tmp/agency-agents-temp
fi

echo "⚙️  Convirtiendo agentes para Gemini CLI..."
cd /tmp/agency-agents-temp
chmod +x scripts/*.sh
./scripts/convert.sh --tool gemini-cli
./scripts/install.sh --tool gemini-cli

# 4. Configurar lanzador de escritorio
echo "🖥️  Creando lanzador de aplicaciones..."
mkdir -p ~/.local/share/applications
cat <<EOF > ~/.local/share/applications/agency-desktop.desktop
[Desktop Entry]
Name=The Agency Desktop
Comment=Gestor visual de agentes para Gemini CLI
Exec=python3 /home/erceppi/Documentos/proyectos/agency-desktop/src/main.py
Icon=preferences-desktop-remote
Terminal=false
Type=Application
Categories=Development;GTK;
EOF

# 5. Generar manifiesto inicial
echo "📊 Generando catálogo de expertos..."
python3 /home/erceppi/Documentos/proyectos/agency-desktop/scripts/generate_manifest.py

echo ""
echo "✅ ¡Instalación completada con éxito!"
echo "Puedes abrir 'The Agency Desktop' desde tu menú de aplicaciones."
