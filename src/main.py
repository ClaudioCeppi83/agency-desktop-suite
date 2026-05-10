import sys
import os
import json
import gi
import threading
import hashlib
import locale

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GObject, GLib, Gdk

# --- CONSTANTES DE CONFIGURACIÓN ---
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
LOCALES_DIR = os.path.join(ASSETS_DIR, "locales")
MANIFEST_PATH = os.path.join(ASSETS_DIR, "manifest.json")
CONFIG_DIR = os.path.expanduser("~/.config/agency-manager")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")
SQUADS_PATH = os.path.join(CONFIG_DIR, "squads.json")
STATE_PATH = os.path.join(CONFIG_DIR, "state.json")
AGENTS_BASE_DIR = os.path.expanduser("~/.gemini/extensions/agency-agents")
CUSTOM_DIR = os.path.join(AGENTS_BASE_DIR, "custom")

class AgencyApp(Adw.Application):
	def __init__(self, **kwargs):
		super().__init__(application_id='com.erceppi.AgencyDesktop',
						 flags=Gio.ApplicationFlags.FLAGS_NONE,
						 **kwargs)
		self._init_directories()
		self.agents = []
		self.agent_rows = {}
		self.current_agent = None
		self.current_squad = []
		self.updated_agents = set()
		
		# Carga de configuraciones
		self.settings = self._load_json(SETTINGS_PATH)
		self.agent_hashes = self._load_json(STATE_PATH)
		self.squads_data = self._load_json(SQUADS_PATH)
		
		# Sistema de Idiomas (i18n)
		self.lang = self._detect_language()
		self.i18n = self._load_locales(self.lang)

	def _init_directories(self):
		for d in [CONFIG_DIR, CUSTOM_DIR, ASSETS_DIR]:
			os.makedirs(d, exist_ok=True)

	def _load_json(self, path):
		if os.path.exists(path):
			try:
				with open(path, 'r') as f: return json.load(f)
			except: return {}
		return {}

	def _detect_language(self):
		"""Detecta el idioma del sistema. Prioridad: settings > sistema > 'en'."""
		if "language" in self.settings:
			return self.settings["language"]
		
		try:
			# Método moderno para Python 3.11+
			sys_lang = locale.getlocale()[0] or locale.getdefaultlocale()[0]
			if sys_lang and sys_lang.lower().startswith("es"):
				return "es"
		except Exception:
			pass
		
		return "en" # Inglés por defecto (principal)

	def _load_locales(self, lang):
		path = os.path.join(LOCALES_DIR, f"{lang}.json")
		if not os.path.exists(path):
			path = os.path.join(LOCALES_DIR, "en.json")
		return self._load_json(path)

	def t(self, key, **kwargs):
		"""Traduce una clave con soporte para variables."""
		text = self.i18n.get(key, key)
		return text.format(**kwargs)

	def do_activate(self):
		self.load_manifest()
		self.window = Adw.ApplicationWindow(application=self, title=self.t("app_title"))
		self.window.set_default_size(1200, 800)

		self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.main_box.append(self._create_catalog_panel())
		self.main_box.append(self._create_editor_panel())
		self.main_box.append(self._create_squad_panel())

		self.window.set_content(self.main_box)
		self.window.present()

	def load_manifest(self):
		self.agents = self._load_json(MANIFEST_PATH)

	def _create_catalog_panel(self):
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		box.set_size_request(320, -1)
		box.add_css_class("background")
		
		header = Adw.HeaderBar()
		header.set_title_widget(Adw.WindowTitle(title=self.t("catalog_title")))
		
		self.sync_stack = Gtk.Stack()
		self.sync_btn = Gtk.Button(icon_name="view-refresh-symbolic")
		self.sync_btn.set_tooltip_text(self.t("sync_tooltip"))
		self.sync_btn.connect("clicked", self.on_sync_clicked)
		self.sync_stack.add_named(self.sync_btn, "button")
		
		self.sync_spinner = Gtk.Spinner()
		self.sync_stack.add_named(self.sync_spinner, "spinner")
		header.pack_start(self.sync_stack)

		about_btn = Gtk.Button(icon_name="help-about-symbolic")
		about_btn.set_tooltip_text(self.t("about_tooltip"))
		about_btn.connect("clicked", self.on_about_clicked)
		header.pack_end(about_btn)
		
		box.append(header)

		self.agent_list = Gtk.ListBox()
		self.agent_list.add_css_class("navigation-sidebar")
		self.agent_list.connect("row-selected", self.on_agent_selected)
		
		for agent in self.agents:
			self._add_agent_row(agent)

		scrolled = Gtk.ScrolledWindow()
		scrolled.set_vexpand(True)
		scrolled.set_child(self.agent_list)
		box.append(scrolled)
		return box

	def _add_agent_row(self, agent):
		row = Adw.ActionRow(title=GLib.markup_escape_text(agent['name']))
		row.agent_data = agent
		badge_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		row.badge_box = badge_box
		row.add_prefix(badge_box)
		self.update_badges(row)
		drag_source = Gtk.DragSource.new()
		drag_source.connect("prepare", self.on_drag_prepare, agent)
		row.add_controller(drag_source)
		self.agent_list.append(row)
		self.agent_rows[agent['id']] = row

	def _create_editor_panel(self):
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		box.set_hexpand(True)
		box.add_css_class("view")
		header = Adw.HeaderBar()
		self.save_rules_btn = Gtk.Button(icon_name="document-save-symbolic")
		self.save_rules_btn.set_tooltip_text(self.t("save_rules_tooltip"))
		self.save_rules_btn.set_sensitive(False)
		self.save_rules_btn.connect("clicked", self.on_save_custom_rules)
		header.pack_end(self.save_rules_btn)
		self.reset_btn = Gtk.Button(icon_name="edit-clear-all-symbolic")
		self.reset_btn.set_tooltip_text(self.t("reset_rules_tooltip"))
		self.reset_btn.set_sensitive(False); self.reset_btn.add_css_class("error")
		self.reset_btn.connect("clicked", self.on_factory_reset)
		header.pack_end(self.reset_btn)
		box.append(header)
		self.details_stack = Gtk.Stack()
		self.details_stack.add_named(Adw.StatusPage(title=self.t("welcome_title"), icon_name="avatar-default-symbolic", description=self.t("welcome_desc")), "empty")
		editor_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
		self._set_margins(editor_box, 12)
		self.agent_info_label = Gtk.Label(xalign=0); self.agent_info_label.add_css_class("title-2")
		editor_box.append(self.agent_info_label)
		self.rules_text_view = Gtk.TextView(); self.rules_text_view.set_vexpand(True); self.rules_text_view.add_css_class("monospace")
		scrolled_editor = Gtk.ScrolledWindow(); scrolled_editor.set_child(self.rules_text_view); scrolled_editor.add_css_class("card")
		editor_box.append(scrolled_editor)
		self.details_stack.add_named(editor_box, "editor")
		box.append(self.details_stack)
		return box

	def _create_squad_panel(self):
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		box.set_size_request(280, -1); box.add_css_class("background")
		header = Adw.HeaderBar(); header.set_title_widget(Adw.WindowTitle(title=self.t("my_squad_title")))
		save_btn = Gtk.Button(icon_name="media-floppy-symbolic")
		save_btn.set_tooltip_text(self.t("save_squad_tooltip"))
		save_btn.connect("clicked", self.on_save_squad)
		header.pack_end(save_btn); box.append(header)
		self.squad_list = Gtk.ListBox(); self.squad_list.add_css_class("navigation-sidebar")
		drop_target = Gtk.DropTarget.new(GObject.TYPE_STRING, Gdk.DragAction.COPY)
		drop_target.connect("drop", self.on_drop_received); self.squad_list.add_controller(drop_target)
		scrolled = Gtk.ScrolledWindow(); scrolled.set_vexpand(True); scrolled.set_child(self.squad_list); box.append(scrolled)
		clear_btn = Gtk.Button(label=self.t("clear_squad_btn")); clear_btn.add_css_class("destructive-action")
		self._set_margins(clear_btn, 12); clear_btn.connect("clicked", self.on_clear_squad); box.append(clear_btn)
		return box

	def _set_margins(self, widget, val):
		widget.set_margin_top(val); widget.set_margin_bottom(val)
		widget.set_margin_start(val); widget.set_margin_end(val)

	def update_badges(self, row):
		while child := row.badge_box.get_first_child(): row.badge_box.remove(child)
		agent = row.agent_data
		if os.path.exists(os.path.join(CUSTOM_DIR, f"{agent['id']}.md")):
			self._add_badge(row.badge_box, self.t("status_edited"), "warning")
		elif agent['id'] in self.updated_agents:
			self._add_badge(row.badge_box, self.t("status_updated"), "accent")
		elif agent['id'] not in self.agent_hashes:
			self._add_badge(row.badge_box, self.t("status_new"), "success")
		else:
			self._add_badge(row.badge_box, self.t("status_factory"), "dim-label")

	def _add_badge(self, box, text, css_class):
		l = Gtk.Label(label=text); l.add_css_class(css_class); l.add_css_class("pill"); box.append(l)

	def on_agent_selected(self, listbox, row):
		if not row: return
		self.current_agent = row.agent_data
		if self.current_agent['id'] in self.updated_agents:
			self.updated_agents.remove(self.current_agent['id'])
			self.update_badges(row)
		custom_path = os.path.join(CUSTOM_DIR, f"{self.current_agent['id']}.md")
		original_path = os.path.join(self.current_agent['path'], "SKILL.md")
		active_path = custom_path if os.path.exists(custom_path) else original_path
		try:
			with open(active_path, 'r') as f: self.rules_text_view.get_buffer().set_text(f.read())
		except: pass
		self.agent_info_label.set_markup(f"<b>{self.current_agent['name']}</b>")
		self.save_rules_btn.set_sensitive(True)
		self.reset_btn.set_sensitive(os.path.exists(custom_path))
		self.details_stack.set_visible_child_name("editor")

	def on_save_custom_rules(self, btn):
		buffer = self.rules_text_view.get_buffer()
		content = buffer.get_text(*buffer.get_bounds(), True)
		with open(os.path.join(CUSTOM_DIR, f"{self.current_agent['id']}.md"), 'w') as f: f.write(content)
		self.update_badges(self.agent_rows[self.current_agent['id']])
		self.reset_btn.set_sensitive(True)

	def on_factory_reset(self, btn):
		path = os.path.join(CUSTOM_DIR, f"{self.current_agent['id']}.md")
		if os.path.exists(path):
			os.remove(path)
			self.update_badges(self.agent_rows[self.current_agent['id']])
			self.on_agent_selected(None, self.agent_rows[self.current_agent['id']])

	def on_sync_clicked(self, btn):
		self.sync_stack.set_visible_child_name("spinner")
		self.sync_spinner.start()
		threading.Thread(target=self.run_sync).start()

	def run_sync(self):
		new_updates = []
		for agent in self.agents:
			path = os.path.join(agent['path'], "SKILL.md")
			h = hashlib.md5(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None
			if self.agent_hashes.get(agent['id']) and h != self.agent_hashes.get(agent['id']):
				new_updates.append(agent['id'])
			self.agent_hashes[agent['id']] = h
		self.updated_agents.update(new_updates)
		with open(STATE_PATH, 'w') as f: json.dump(self.agent_hashes, f, indent=4)
		GLib.idle_add(self.on_sync_finished, len(new_updates))

	def on_sync_finished(self, count):
		self.sync_spinner.stop(); self.sync_stack.set_visible_child_name("button")
		for aid in self.updated_agents:
			if aid in self.agent_rows: self.update_badges(self.agent_rows[aid])
		msg = self.t("sync_dialog_msg", count=count) if count > 0 else self.t("sync_dialog_no_changes")
		d = Adw.MessageDialog(transient_for=self.window, heading=self.t("sync_dialog_title"), body=msg)
		d.add_response("ok", "OK"); d.present()

	def on_drag_prepare(self, source, x, y, agent):
		return Gdk.ContentProvider.new_for_value(GObject.Value(GObject.TYPE_STRING, agent['id']))

	def on_drop_received(self, target, value, x, y):
		agent = next((a for a in self.agents if a['id'] == value), None)
		if agent and agent not in self.current_squad:
			self.current_squad.append(agent)
			row = Adw.ActionRow(title=agent['name'])
			btn = Gtk.Button(icon_name="list-remove-symbolic"); btn.add_css_class("flat")
			btn.connect("clicked", lambda b: self._remove_from_squad(agent, row))
			row.add_suffix(btn); self.squad_list.append(row)
			return True
		return False

	def _remove_from_squad(self, agent, row):
		self.current_squad.remove(agent); self.squad_list.remove(row)

	def on_clear_squad(self, btn):
		self.current_squad = []
		while row := self.squad_list.get_first_child(): self.squad_list.remove(row)

	def on_save_squad(self, btn):
		if not self.current_squad: return
		self.squads_data["Default_Squad"] = [a['id'] for a in self.current_squad]
		with open(SQUADS_PATH, 'w') as f: json.dump(self.squads_data, f, indent=4)
		d = Adw.MessageDialog(transient_for=self.window, heading=self.t("save_dialog_title"), body=self.t("save_dialog_msg"))
		d.add_response("ok", "OK"); d.present()

	def on_about_clicked(self, btn):
		dialog = Adw.MessageDialog(transient_for=self.window, heading=self.t("about_dialog_title"), body=self.t("about_dialog_body"))
		dialog.set_body_use_markup(True)
		dialog.add_response("repo", self.t("about_dialog_repo_btn"))
		dialog.add_response("close", self.t("about_dialog_close_btn"))
		def on_response(d, response_id):
			if response_id == "repo":
				Gtk.UriLauncher.new("https://github.com/msitarzewski/agency-agents").launch(self.window, None, None)
		dialog.connect("response", on_response); dialog.present()

if __name__ == '__main__':
	app = AgencyApp()
	app.run(sys.argv)
