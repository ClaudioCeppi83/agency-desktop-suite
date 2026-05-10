# Agency Desktop Suite (Native Ubuntu)

Una potente consola visual para gestionar, personalizar y orquestar a más de 180 agentes de IA de la biblioteca "The Agency", integrada nativamente en Gemini CLI y Ubuntu 24.04.

## ✨ Características Principales

- **Gestión Visual:** Explora más de 180 expertos especializados con una interfaz GTK4 moderna.
- **Orquestación Física (Drag-and-Drop):** Crea escuadrones de agentes simplemente arrastrándolos a tu mesa de trabajo.
- **Personalización Segura:** Edita las reglas de cualquier agente. El sistema prioriza tus cambios pero mantiene siempre la versión de fábrica disponible.
- **Sincronización Inteligente:** Actualiza la biblioteca desde GitHub y recibe notificaciones visuales (Badges) solo de los agentes que realmente cambiaron.
- **Integración Nativa:** Acceso directo desde el menú de aplicaciones de Ubuntu y look-and-feel oficial (Libadwaita).

## 🚀 Instalación (Equipos Nuevos)

Para desplegar la suite completa en un equipo nuevo con Ubuntu, simplemente clona este repositorio y ejecuta el instalador maestro:

```bash
chmod +x install.sh
./install.sh
```

El script se encargará de instalar las dependencias de GTK4, configurar los directorios de Gemini CLI, descargar los agentes originales y crear el lanzador de escritorio.

## 🛠️ Estructura del Proyecto

- `src/main.py`: Núcleo de la aplicación (Python/GTK4).
- `scripts/`: Herramientas de soporte para generación de manifiestos y sincronización.
- `assets/`: Datos dinámicos y manifiesto de expertos.
- `install.sh`: Script de despliegue automatizado.

## 📖 Instrucciones de Uso

1. **Explorar:** Usa la lista lateral izquierda para seleccionar agentes. Verás sus reglas técnicas en el panel central.
2. **Editar:** Modifica el texto en el editor central y pulsa el botón **Guardar** (Disco). Verás la etiqueta **"Editado"** en la lista.
3. **Reset:** Si quieres volver a las reglas originales, pulsa el botón **Revertir** (Icono rojo de reset).
4. **Armar Squads:** Arrastra agentes desde la lista izquierda y suéltalos en el panel **"Mi Squad"** (Derecha). Pulsa el botón de guardado del Squad para persistir tu equipo.
5. **Sincronizar:** Usa el botón de refresco arriba del catálogo para buscar actualizaciones en GitHub. Solo los agentes actualizados mostrarán la etiqueta azul.

---
*Desarrollado como MVP profesional para la gestión avanzada de agentes de IA.*

## 🤝 Créditos y Reconocimientos

Esta aplicación es una **suite de gestión y orquestación**, pero el "cerebro" técnico reside en los agentes.

- **Autor de los Agentes:** [msitarzewski](https://github.com/msitarzewski)
- **Repositorio Original:** [agency-agents](https://github.com/msitarzewski/agency-agents)

**Nota Importante:** Todos los perfiles de agentes disponibles de fábrica en esta suite son propiedad intelectual del repositorio `agency-agents`. Esta suite está diseñada únicamente para facilitar su manipulación visual, personalización y uso en entornos como Gemini CLI. Agradecemos profundamente a msitarzewski por su increíble trabajo al crear y mantener esta biblioteca de más de 180 expertos.
