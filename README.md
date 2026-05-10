# Agency Desktop Suite (Native Ubuntu Edition)

[English](#english) | [Español](#español)

---

<a name="english"></a>
# English

A powerful visual console to manage, customize, and orchestrate over 180 AI agents from "The Agency" library, natively integrated with Gemini CLI and Ubuntu 24.04.

## ✨ Key Features

- **Visual Management:** Explore 180+ specialized experts with a modern GTK4 interface.
- **Physical Orchestration (Drag-and-Drop):** Create agent squads simply by dragging them to your workspace.
- **Safe Customization:** Edit any agent's rules. The system prioritizes your changes while keeping the factory version always available.
- **Smart Synchronization:** Update the library from GitHub and receive visual badges only for agents that actually changed.
- **Native Integration:** Direct access from the Ubuntu applications menu with official look-and-feel (Libadwaita).
- **Bilingual Support:** Automatic language detection (English/Spanish).

## 🚀 Installation (New Systems)

To deploy the full suite on a new Ubuntu system, clone this repository and run the master installer:

```bash
chmod +x install.sh
./install.sh
```

The script will handle GTK4 dependencies, configure Gemini CLI directories, download original agents, and create the desktop launcher.

## 🛠️ Project Structure

- `src/main.py`: Application core (Python/GTK4).
- `assets/locales/`: Translation files (JSON).
- `scripts/`: Support tools for manifest generation and syncing.
- `install.sh`: Automated deployment script.

---

<a name="español"></a>
# Español

Una potente consola visual para gestionar, personalizar y orquestar a más de 180 agentes de IA de la biblioteca "The Agency", integrada nativamente en Gemini CLI y Ubuntu 24.04.

## ✨ Características Principales

- **Gestión Visual:** Explora más de 180 expertos especializados con una interfaz GTK4 moderna.
- **Orquestación Física (Drag-and-Drop):** Crea escuadrones de agentes simplemente arrastrándolos a tu mesa de trabajo.
- **Personalización Segura:** Edita las reglas de cualquier agente. El sistema prioriza tus cambios pero mantiene siempre la versión de fábrica disponible.
- **Sincronización Inteligente:** Actualiza la biblioteca desde GitHub y recibe notificaciones visuales (Badges) solo de los agentes que realmente cambiaron.
- **Integración Nativa:** Acceso directo desde el menú de aplicaciones de Ubuntu y look-and-feel oficial (Libadwaita).
- **Soporte Bilingüe:** Detección automática de idioma (Inglés/Español).

## 🚀 Instalación (Equipos Nuevos)

Para desplegar la suite completa en un equipo nuevo con Ubuntu, simplemente clona este repositorio y ejecuta el instalador maestro:

```bash
chmod +x install.sh
./install.sh
```

El script se encargará de instalar las dependencias de GTK4, configurar los directorios de Gemini CLI, descargar los agentes originales y crear el lanzador de escritorio.

## 🛠️ Estructura del Proyecto

- `src/main.py`: Núcleo de la aplicación (Python/GTK4).
- `assets/locales/`: Archivos de traducción (JSON).
- `scripts/`: Herramientas de soporte para generación de manifiestos y sincronización.
- `install.sh`: Script de despliegue automatizado.

---

## 🤝 Credits and Recognitions / Créditos y Reconocimientos

This application is a **management and orchestration suite**, but the technical "brain" resides in the agents. / Esta aplicación es una **suite de gestión y orquestación**, pero el "cerebro" técnico reside en los agentes.

- **Agents Author / Autor de los Agentes:** [msitarzewski](https://github.com/msitarzewski)
- **Original Repository / Repositorio Original:** [agency-agents](https://github.com/msitarzewski/agency-agents)

**Important Note:** All agent profiles available factory-default in this suite are the intellectual property of the `agency-agents` repository. This suite is designed solely to facilitate their visual manipulation, customization, and use in environments like Gemini CLI. / **Nota Importante:** Todos los perfiles de agentes disponibles de fábrica en esta suite son propiedad intelectual del repositorio `agency-agents`. Esta suite está diseñada únicamente para facilitar su manipulación visual, personalización y uso en entornos como Gemini CLI.
