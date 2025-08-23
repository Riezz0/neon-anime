#!/usr/bin/env python3

# Sunnah PyGObject App
# This application fetches a random Hadith from sunnah.com and displays it using PyGObject.
# It uses the requests and BeautifulSoup libraries for web scraping.

import gi
import sys
import requests
from bs4 import BeautifulSoup
import random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class SunnahApp(Gtk.ApplicationWindow):
    """
    Main application window for the Sunnah app.
    Handles UI setup and data fetching/display.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.set_title("Sunnah App")

        # Create the main vertical box container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(15)
        vbox.set_margin_bottom(15)
        vbox.set_margin_start(15)
        vbox.set_margin_end(15)
        self.add(vbox)

        # Create a scrollable window for the Hadith text
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        vbox.pack_start(scrolled_window, True, True, 0)

        # Labels for the Hadith
        self.hadith_label = Gtk.Label(label="Fetching Hadith...")
        self.hadith_label.set_line_wrap(True)
        self.hadith_label.set_justify(Gtk.Justification.LEFT)
        self.hadith_label.set_halign(Gtk.Align.START)
        self.hadith_label.get_style_context().add_class("hadith-text")

        # Add the label to a viewport and then to the scrolled window
        viewport = Gtk.Viewport()
        viewport.add(self.hadith_label)
        scrolled_window.add(viewport)

        # Button to fetch a new Hadith
        self.fetch_button = Gtk.Button(label="Fetch New Hadith")
        self.fetch_button.connect("clicked", self.on_fetch_clicked)
        vbox.pack_start(self.fetch_button, False, False, 0)

        # Status bar label for feedback
        self.status_label = Gtk.Label(label="")
        self.status_label.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(self.status_label, False, False, 0)

        # Apply custom CSS
        style_provider = Gtk.CssProvider()
        css = b"""
        .hadith-text {
            font-size: 16px;
            font-family: serif;
            line-height: 1.6;
        }
        .hadith-info {
            font-style: italic;
            font-size: 14px;
            color: #555;
        }
        """
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gtk.Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Initial fetch
        self.fetch_hadith()

    def on_fetch_clicked(self, widget):
        """Callback for the 'Fetch New Hadith' button."""
        self.fetch_hadith()

    def fetch_hadith(self):
        """
        Fetches and displays a random Hadith from sunnah.com.
        This is an I/O operation and should ideally be done in a separate thread.
        For this example, we'll keep it simple and assume the app won't freeze for long.
        """
        self.hadith_label.set_text("Fetching Hadith...")
        self.status_label.set_text("Connecting to sunnah.com...")
        GLib.idle_add(self.do_fetch_hadith_async)

    def do_fetch_hadith_async(self):
        """
        Worker function to perform the web scraping.
        """
        try:
            # We will fetch a random Hadith from the Sahih al-Bukhari collection.
            # We choose a random chapter to get a random Hadith.
            book_number = 1
            start_hadith = 1
            end_hadith = 7563 # Last Hadith in Sahih al-Bukhari
            hadith_number = random.randint(start_hadith, end_hadith)
            url = f"https://sunnah.com/bukhari:{hadith_number}"

            self.status_label.set_text(f"Fetching from {url}...")
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for bad status codes

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the Hadith text and its source information
            english_text = soup.find('div', class_='hadith_text')
            
            # Find all relevant elements and combine them
            content_parts = []
            
            # Find the main English Hadith text
            hadith_english = soup.find('div', class_='english_hadith_full')
            if hadith_english:
                # Append the English text content, stripping the 'hadith_text' class
                text_to_append = ""
                for p in hadith_english.find_all('p'):
                    if p.parent and 'hadith_text' in p.parent.get('class', []):
                         text_to_append += p.get_text() + "\n"
                    
                # Find the reference information (e.g., Book of Revelation, Hadith 1)
                reference_info = soup.find('div', class_='hadith_reference')
                if reference_info:
                    info_text = reference_info.get_text(separator=' ', strip=True)
                    text_to_append += "\n\n" + info_text

                self.hadith_label.set_label(text_to_append)
                self.status_label.set_text(f"Fetched Hadith {hadith_number}")

            else:
                self.hadith_label.set_label("Could not find Hadith content.")
                self.status_label.set_text("Failed to parse page.")

        except requests.exceptions.RequestException as e:
            self.hadith_label.set_label("Error: Could not connect to sunnah.com. Please check your internet connection.")
            self.status_label.set_text(f"Connection error: {e}")
        except Exception as e:
            self.hadith_label.set_label("An unexpected error occurred while fetching the Hadith.")
            self.status_label.set_text(f"Error: {e}")

        return False # Return False to stop the GLib.idle_add loop

def main():
    """Entry point of the application."""
    app = Gtk.Application(application_id="com.example.SunnahApp")
    app.connect("activate", lambda app: SunnahApp(application=app).show_all())
    app.run(sys.argv)

if __name__ == "__main__":
    main()


