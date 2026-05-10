import os
import json
import yaml

SKILLS_DIR = os.path.expanduser("~/.gemini/extensions/agency-agents/skills")
OUTPUT_FILE = "/home/erceppi/Documentos/proyectos/agency-desktop/assets/manifest.json"

def scan_agents():
	agents = []
	if not os.path.exists(SKILLS_DIR):
		print(f"Error: {SKILLS_DIR} no existe.")
		return

	for agent_name in sorted(os.listdir(SKILLS_DIR)):
		agent_path = os.path.join(SKILLS_DIR, agent_name)
		skill_file = os.path.join(agent_path, "SKILL.md")
		
		if os.path.isdir(agent_path) and os.path.exists(skill_file):
			try:
				with open(skill_file, "r") as f:
					content = f.read()
					# Extraer Frontmatter (YAML) si existe
					if content.startswith("---"):
						parts = content.split("---")
						if len(parts) >= 3:
							metadata = yaml.safe_load(parts[1])
							description = metadata.get("description", "Sin descripción")
							display_name = metadata.get("name", agent_name)
						else:
							display_name = agent_name
							description = "Especialista técnico"
					else:
						display_name = agent_name
						description = "Especialista técnico"
					
					agents.append({
						"id": agent_name,
						"name": display_name,
						"description": description,
						"path": agent_path
					})
			except Exception as e:
				print(f"Error procesando {agent_name}: {e}")

	with open(OUTPUT_FILE, "w") as f:
		json.dump(agents, f, indent=4)
	print(f"Manifiesto generado con {len(agents)} agentes en {OUTPUT_FILE}")

if __name__ == "__main__":
	scan_agents()
