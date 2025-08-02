#!/usr/bin/env python3

import gi
import subprocess
import json
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class PowerMenu(Gtk.Window):
    def __init__(self):
        super().__init__(title="Power Menu")
        
        # Load pywal colors
        self.pywal_colors = self.load_pywal_colors()
        
        # Window setup
        self.set_default_size(400, 100)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_skip_taskbar_hint(False)
        
        # Apply styles
        self.apply_styles()
        
        # Create main container
        self.box = Gtk.Box(spacing=10)
        self.box.set_homogeneous(True)
        self.box.set_margin_top(10)
        self.box.set_margin_bottom(10)
        self.box.set_margin_left(10)
        self.box.set_margin_right(10)
        self.add(self.box)
        
        # Create buttons
        self.create_button("", "Lock", self.on_lock_clicked)
        self.create_button("", "Logout", self.on_logout_clicked)
        self.create_button("", "Shutdown", self.on_shutdown_clicked)
        self.create_button("", "Reboot", self.on_reboot_clicked)
    
    def load_pywal_colors(self):
        """Load colors from pywal"""
        colors_path = os.path.expanduser("~/.cache/wal/colors.json")
        try:
            with open(colors_path) as f:
                colors = json.load(f)
            return {
                'background': colors['special']['background'],
                'foreground': colors['special']['foreground'],
                'color0': colors['colors']['color0'],
                'color1': colors['colors']['color1'],
                'color2': colors['colors']['color2'],
                'color3': colors['colors']['color3'],
            }
        except:
            # Fallback colors if pywal isn't available
            return {
                'background': '#282a36',
                'foreground': '#f8f8f2',
                'color0': '#21222c',
                'color1': '#ff5555',
                'color2': '#50fa7b',
                'color3': '#ffb86c',
            }
    
    def apply_styles(self):
        """Apply CSS styling with pywal colors"""
        css = f"""
        window {{
            background-color: {self.pywal_colors['background']};
            border-radius: 5px;
            border: 10px solid {self.pywal_colors['color0']};
        }}
        
        button {{
            background-color: {self.pywal_colors['color0']};
            color: {self.pywal_colors['foreground']};
            border-radius: 5px;
            border: 2px;
            padding: 10px;
            font-family: "Font Awesome 6 Free", sans-serif;
        }}
        
        button:hover {{
            background-color: {self.pywal_colors['color3']};
            color: {self.pywal_colors['background']};
        }}
        
        .danger:hover {{
            background-color: {self.pywal_colors['color3']};
            color: {self.pywal_colors['background']};
        }}
        
        .success:hover {{
            background-color: {self.pywal_colors['color3']};
            color: {self.pywal_colors['background']};
        }}
        """
        
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode())
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_button(self, icon, label, callback):
        """Create a styled button with icon and label"""
        btn = Gtk.Button()
        btn.set_tooltip_text(label)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        icon_label = Gtk.Label(label=icon)
        icon_label.set_name("icon-label")
        text_label = Gtk.Label(label=label)
        
        box.pack_start(icon_label, True, True, 0)
        box.pack_start(text_label, True, True, 0)
        btn.add(box)
        
        # Add danger class to shutdown and reboot
        if label in ["Shutdown", "Reboot"]:
            btn.get_style_context().add_class("danger")
        elif label == "Logout":
            btn.get_style_context().add_class("danger")
        else:
            btn.get_style_context().add_class("success")
        
        btn.connect("clicked", callback)
        self.box.pack_start(btn, True, True, 0)
    
    def on_lock_clicked(self, widget):
        subprocess.Popen(["hyprlock"])
        self.destroy()
    
    def on_logout_clicked(self, widget):
        subprocess.Popen(["hyprctl", "dispatch", "exit"])
        self.destroy()
    
    def on_shutdown_clicked(self, widget):
        subprocess.Popen(["systemctl", "poweroff"])
        self.destroy()
    
    def on_reboot_clicked(self, widget):
        subprocess.Popen(["systemctl", "reboot"])
        self.destroy()

def main():
    win = PowerMenu()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
