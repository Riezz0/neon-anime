#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango
import os

def get_pywal_colors():
    """Load Pywal color scheme"""
    colors = {}
    with open(f"{os.environ['HOME']}/.cache/wal/colors") as f:
        for i, line in enumerate(f):
            colors[f'color{i}'] = line.strip()
    return colors

class PixelPerfectShortcuts(Gtk.Window):
    def __init__(self):
        super().__init__(title="HyprBinds")
        colors = get_pywal_colors()
        
        # Window configuration
        self.set_default_size(300, 300)  # Slightly wider for perfect alignment
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        
        # Apply Pywal styling
        self.apply_styles(colors)
        
        # Main container with perfect columns
        self.create_layout(colors)

    def apply_styles(self, colors):
        """Apply CSS styling from Pywal colors"""
        css_provider = Gtk.CssProvider()
        css = f"""
        * {{
            font-family: 'Fira Code', monospace;
        }}
        window {{
            background-color: {colors['color0']};
        }}
        .category {{
            color: {colors['color2']};
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 15px;
            margin-bottom: 5px;
            margin-left: 20px;
        }}
        .header {{
            color: {colors['color3']};
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .keybind {{
            color: {colors['color4']};
            font-weight: bold;
            min-width: 250px;  /* Fixed width for keybinds */
        }}
        .description {{
            color: {colors['color7']};
            min-width: 400px;  /* Fixed width for descriptions */
        }}
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_layout(self, colors):
        """Create perfectly aligned layout"""
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(scrolled)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        scrolled.add(main_box)

        # Get categorized binds
        categorized_binds = self.get_categorized_binds()

        # Category display order
        category_order = [
            'workspaces',
            'window management',
            'apps',
            'scratchpads',
            'system',
            'other'
        ]

        for category in category_order:
            if category in categorized_binds and categorized_binds[category]:
                # Category header
                lbl_category = Gtk.Label(label=category.upper())
                lbl_category.set_xalign(0)
                lbl_category.get_style_context().add_class("category")
                main_box.pack_start(lbl_category, False, False, 0)

                # Create a grid for perfect alignment
                grid = Gtk.Grid()
                grid.set_column_spacing(30)
                grid.set_row_spacing(3)  # Tighter row spacing
                grid.set_margin_start(20)
                grid.set_margin_end(20)
                grid.set_margin_bottom(10)
                main_box.pack_start(grid, False, False, 0)

                # Column headers
                key_header = Gtk.Label(label="KEYBIND")
                key_header.set_xalign(0)
                key_header.get_style_context().add_class("header")
                
                desc_header = Gtk.Label(label="DESCRIPTION")
                desc_header.set_xalign(0)
                desc_header.get_style_context().add_class("header")
                
                grid.attach(key_header, 0, 0, 1, 1)
                grid.attach(desc_header, 1, 0, 1, 1)

                # Add all binds for this category
                for i, (keybind, description) in enumerate(categorized_binds[category], start=1):
                    # Keybind label with fixed width
                    lbl_key = Gtk.Label(label=keybind)
                    lbl_key.set_xalign(0)
                    lbl_key.get_style_context().add_class("keybind")
                    lbl_key.set_halign(Gtk.Align.START)
                    
                    # Description label with fixed width
                    lbl_desc = Gtk.Label(label=description)
                    lbl_desc.set_xalign(0)
                    lbl_desc.get_style_context().add_class("description")
                    lbl_desc.set_halign(Gtk.Align.START)
                    lbl_desc.set_line_wrap(True)
                    
                    grid.attach(lbl_key, 0, i, 1, 1)
                    grid.attach(lbl_desc, 1, i, 1, 1)

        # Apply monospace font to everything
        font_desc = Pango.FontDescription("Jetbrains Mono Nerd Font 12")
        def apply_font(widget):
            if isinstance(widget, Gtk.Label):
                widget.override_font(font_desc)
                widget.set_ellipsize(Pango.EllipsizeMode.END)
            elif hasattr(widget, 'get_children'):
                for child in widget.get_children():
                    apply_font(child)
        apply_font(main_box)

    def get_categorized_binds(self):
        """Parse and categorize binds.conf with perfect alignment in mind"""
        categories = {
            'workspaces': [],
            'window management': [],
            'apps': [],
            'scratchpads': [],
            'system': [],
            'other': []
        }

        try:
            with open(f"{os.environ['HOME']}/.config/hypr/binds.conf") as f:
                for line in f:
                    if line.startswith(('bind', 'binde', 'bindm')):
                        # Skip empty/commented binds
                        if not line.strip() or line.strip().startswith('#'):
                            continue
                            
                        parts = line.split('#', 1)
                        if len(parts) < 2:
                            continue
                            
                        cmd_part = parts[0].split('=', 1)[1].strip()
                        description = parts[1].strip()
                        
                        # Extract key combination (first 2 parts)
                        key_parts = [x.strip() for x in cmd_part.split(',')[:2]]
                        keybind = ', '.join(key_parts)
                        
                        # Standardize description capitalization
                        description = description[0].upper() + description[1:]
                        
                        # Categorize based on description
                        desc_lower = description.lower()
                        if 'window' in desc_lower:
                            categories['window management'].append((keybind, description))
                        elif 'launch' in desc_lower:
                            categories['apps'].append((keybind, description))
                        elif 'workspace' in desc_lower:
                            categories['workspaces'].append((keybind, description))
                        elif 'scratchpad' in desc_lower:
                            categories['scratchpads'].append((keybind, description))
                        elif 'hyprland' in desc_lower:
                            categories['system'].append((keybind, description))
                        else:
                            categories['other'].append((keybind, description))
                            
        except Exception as e:
            print(f"Error loading binds: {e}")
        
        return categories

if __name__ == "__main__":
    win = PixelPerfectShortcuts()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
