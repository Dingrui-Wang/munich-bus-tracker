import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from datetime import datetime, timedelta
from mvg import MvgApi, TransportType
import json
import math

class MunichBusTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Munich Bus Tracker - Cyberpunk Edition")
        # Adjusted window size to fit font content better
        self.root.geometry("1600x1200")
        self.root.configure(bg='#000000')
        self.root.resizable(True, True)
        
        # Cyberpunk neon color scheme - vivid and dynamic
        self.colors = {
            'bg': '#000000',                    # Pure black background
            'primary': '#00FFFF',               # Neon cyan
            'primary_light': '#40FFFF',         # Lighter cyan
            'primary_dark': '#00CCCC',          # Darker cyan
            'secondary': '#FF00FF',             # Neon magenta
            'secondary_light': '#FF40FF',       # Lighter magenta
            'secondary_dark': '#CC00CC',        # Darker magenta
            'accent': '#00FF00',                # Neon green
            'accent_light': '#40FF40',          # Lighter green
            'accent_dark': '#00CC00',           # Darker green
            'warning': '#FFFF00',               # Neon yellow
            'warning_light': '#FFFF40',         # Lighter yellow
            'warning_dark': '#CCCC00',          # Darker yellow
            'danger': '#FF0040',                # Neon red-pink
            'danger_light': '#FF4060',          # Lighter red-pink
            'danger_dark': '#CC0030',           # Darker red-pink
            'success': '#00FF80',               # Neon green-blue
            'success_light': '#40FF90',         # Lighter green-blue
            'success_dark': '#00CC60',          # Darker green-blue
            'text': '#FFFFFF',                  # Pure white
            'text_secondary': '#E0E0E0',        # Light gray
            'text_tertiary': '#C0C0C0',         # Medium gray
            'dark': '#0A0A0A',                  # Very dark gray
            'darker': '#050505',                # Almost black
            'card_bg': '#111111',               # Dark card background
            'card_bg_light': '#222222',         # Lighter card background
            'border': '#333333',                # Border color
            'border_light': '#555555',          # Lighter border
            'highlight': '#FF8000',             # Neon orange
            'highlight_light': '#FF9040',       # Lighter orange
            'shadow': '#000000',                # Pure black shadow
            'electric_blue': '#0080FF',         # Electric blue
            'electric_purple': '#8000FF',       # Electric purple
            'laser_red': '#FF0080',             # Laser red
            'matrix_green': '#00FF40',          # Matrix green
        }
        
        # Keep font sizes the same as requested
        self.fonts = {
            'title': ('Helvetica', 96, 'bold'),
            'subtitle': ('Helvetica', 36, 'italic'),
            'header': ('Helvetica', 48, 'bold'),
            'subheader': ('Helvetica', 44, 'bold'),
            'large': ('Helvetica', 40, 'bold'),
            'medium': ('Helvetica', 36, 'normal'),
            'body': ('Helvetica', 32, 'bold'),
            'small': ('Helvetica', 28, 'normal'),
            'countdown': ('Helvetica', 72, 'bold'),
            'alert': ('Helvetica', 144, 'bold'),
            'monospace': ('Courier New', 32, 'normal')
        }
        
        # Simplified icons - removing problematic emojis for better compatibility
        self.icons = {
            'bus': '▶',
            'check': '✓',
            'cross': '✗',
            'refresh': '⟲',
            'warning': '⚠',
            'alert': '⚡',
            'clock': '⏰',
            'location': '⬢',
            'status_red': '●',
            'status_yellow': '●',
            'status_green': '●',
            'matrix': '█',
            'cyber': '▣',
            'neon': '◈',
            'electric': '⚡',
            'laser': '◆',
            'digital': '▲',
            'circuit': '◯',
            'data': '▬',
            'signal': '▌',
            'power': '▓'
        }
        
        # Enhanced animation variables for cyberpunk effects
        self.animation_frame = 0
        self.last_update = 0
        self.update_interval = 10  # seconds
        self.animation_speed = 50  # Faster animations for cyberpunk feel
        self.pulse_intensity = 0.0
        self.color_cycle_position = 0.0
        self.matrix_effect_active = False
        
        # MVG API setup
        self.station = None
        self.mvgapi = None
        self.target_destination = 'Garching, Forschungszentrum (U)'
        self.walk_time_minutes = 5
        
        # Alert state
        self.leave_now_active = False
        
        self.setup_ui()
        self.setup_mvg_api()
        self.start_monitoring()
        
    def create_cyberpunk_frame(self, parent, bg_color, border_color, thickness=2):
        """Create a cyberpunk-style frame with neon border effect"""
        outer_frame = tk.Frame(parent, bg=border_color, relief=tk.RAISED, bd=1)
        middle_frame = tk.Frame(outer_frame, bg=bg_color, relief=tk.FLAT, bd=0)
        inner_frame = tk.Frame(middle_frame, bg=bg_color)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=thickness, pady=thickness)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        return outer_frame, inner_frame
        
    def create_neon_glow_frame(self, parent, bg_color, glow_color, thickness=3):
        """Create a frame with neon glow effect"""
        # Multiple layers for glow effect
        glow_frame = tk.Frame(parent, bg=glow_color)
        shadow_frame = tk.Frame(glow_frame, bg=bg_color)
        content_frame = tk.Frame(shadow_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=thickness, pady=thickness)
        shadow_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        return glow_frame, content_frame
        
    def safe_icon(self, icon_name, fallback_text=""):
        """Get icon with cyberpunk fallback"""
        try:
            return self.icons.get(icon_name, fallback_text)
        except:
            return fallback_text or "▶"
        
    def setup_ui(self):
        # Main container with cyberpunk styling
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title section with neon glow effect
        title_outer, title_frame = self.create_neon_glow_frame(
            main_frame, self.colors['card_bg'], self.colors['primary'], 3
        )
        title_outer.pack(fill=tk.X, pady=(0, 15))
        
        # Enhanced title with cyberpunk styling
        title_container = tk.Frame(title_frame, bg=self.colors['card_bg'])
        title_container.pack(pady=(15, 10))
        
        # Cyberpunk bus icon
        self.bus_icon_label = tk.Label(title_container, 
                                      text=self.safe_icon('cyber', '◈'), 
                                      font=('Helvetica', 80, 'bold'),
                                      fg=self.colors['electric_blue'], 
                                      bg=self.colors['card_bg'])
        self.bus_icon_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Main title - cyberpunk style
        self.title_label = tk.Label(title_container, text="MUNICH BUS TRACKER", 
                                   font=self.fonts['title'],
                                   fg=self.colors['primary'], bg=self.colors['card_bg'])
        self.title_label.pack(side=tk.LEFT)
        
        # Subtitle with neon effect
        self.subtitle_label = tk.Label(title_frame, text=">>> CYBERPUNK TRANSIT INTERFACE <<<", 
                                      font=self.fonts['subtitle'],
                                      fg=self.colors['secondary'], bg=self.colors['card_bg'])
        self.subtitle_label.pack(pady=(0, 15))
        
        # Status panel with electric styling
        status_outer, status_frame = self.create_neon_glow_frame(
            main_frame, self.colors['card_bg'], self.colors['matrix_green'], 2
        )
        status_outer.pack(fill=tk.X, pady=(0, 15))
        
        status_container = tk.Frame(status_frame, bg=self.colors['card_bg'])
        status_container.pack(pady=12)
        
        # Status with electric icon
        self.status_icon = tk.Label(status_container, 
                                   text=self.safe_icon('electric', '⚡'), 
                                   font=('Helvetica', 28, 'bold'),
                                   fg=self.colors['matrix_green'], 
                                   bg=self.colors['card_bg'])
        self.status_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(status_container, text=">>> INITIALIZING NEURAL LINK <<<", 
                                    font=self.fonts['body'],
                                    fg=self.colors['matrix_green'], bg=self.colors['card_bg'])
        self.status_label.pack(side=tk.LEFT)
        
        # Destination info with laser styling
        dest_outer, dest_frame = self.create_neon_glow_frame(
            main_frame, self.colors['card_bg'], self.colors['laser_red'], 2
        )
        dest_outer.pack(fill=tk.X, pady=(0, 15))
        
        dest_header = tk.Frame(dest_frame, bg=self.colors['card_bg'])
        dest_header.pack(pady=(12, 5))
        
        # Location with laser icon
        location_icon = tk.Label(dest_header, 
                                text=self.safe_icon('laser', '◆'), 
                                font=('Helvetica', 35, 'bold'),
                                fg=self.colors['laser_red'], 
                                bg=self.colors['card_bg'])
        location_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(dest_header, text=">>> TARGET DESTINATION <<<", 
                font=self.fonts['subheader'],
                fg=self.colors['text'], bg=self.colors['card_bg']).pack(side=tk.LEFT)
        
        tk.Label(dest_frame, text=self.target_destination, 
                font=self.fonts['header'],
                fg=self.colors['laser_red'], bg=self.colors['card_bg']).pack(pady=(0, 12))
        
        # LEAVE NOW alert panel - cyberpunk style
        self.leave_now_frame = tk.Frame(main_frame, bg=self.colors['danger'], 
                                       relief=tk.RAISED, bd=6)
        self.leave_now_label = tk.Label(self.leave_now_frame, text="", 
                                       font=self.fonts['alert'],
                                       fg=self.colors['text'], bg=self.colors['danger'])
        self.leave_now_label.pack(pady=30)
        
        # Next departure countdown with electric glow
        countdown_outer, self.countdown_frame = self.create_neon_glow_frame(
            main_frame, self.colors['card_bg'], self.colors['electric_purple'], 3
        )
        countdown_outer.pack(fill=tk.X, pady=(0, 15))
        
        countdown_header = tk.Frame(self.countdown_frame, bg=self.colors['card_bg'])
        countdown_header.pack(pady=(12, 5))
        
        # Clock with digital icon
        clock_icon = tk.Label(countdown_header, 
                             text=self.safe_icon('digital', '▲'), 
                             font=('Helvetica', 35, 'bold'),
                             fg=self.colors['electric_purple'], 
                             bg=self.colors['card_bg'])
        clock_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(countdown_header, text=">>> NEXT DEPARTURE <<<", 
                font=self.fonts['subheader'],
                fg=self.colors['electric_purple'], bg=self.colors['card_bg']).pack(side=tk.LEFT)
        
        self.next_bus_label = tk.Label(self.countdown_frame, text="", 
                                      font=self.fonts['medium'],
                                      fg=self.colors['text'], bg=self.colors['card_bg'])
        self.next_bus_label.pack(pady=5)
        
        # Departure time display - same font size
        self.countdown_label = tk.Label(self.countdown_frame, text="", 
                                       font=self.fonts['countdown'],
                                       fg=self.colors['primary'], bg=self.colors['card_bg'])
        self.countdown_label.pack(pady=8)
        
        # Leave time display with cyberpunk warning
        leave_time_container = tk.Frame(self.countdown_frame, bg=self.colors['card_bg'])
        leave_time_container.pack(pady=(0, 12))
        
        self.leave_time_icon = tk.Label(leave_time_container, 
                                       text=self.safe_icon('alert', '⚡'), 
                                       font=('Helvetica', 30, 'bold'),
                                       fg=self.colors['warning'], 
                                       bg=self.colors['card_bg'])
        self.leave_time_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.leave_time_label = tk.Label(leave_time_container, text="", 
                                        font=self.fonts['large'],
                                        fg=self.colors['warning'], bg=self.colors['card_bg'])
        self.leave_time_label.pack(side=tk.LEFT)
        
        # Departures list with matrix-style design
        departures_outer, departures_frame = self.create_neon_glow_frame(
            main_frame, self.colors['card_bg'], self.colors['matrix_green'], 2
        )
        departures_outer.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        departures_header = tk.Frame(departures_frame, bg=self.colors['card_bg'])
        departures_header.pack(pady=(12, 8))
        
        # Matrix-style list icon
        list_icon = tk.Label(departures_header, 
                            text=self.safe_icon('matrix', '█'), 
                            font=('Helvetica', 35, 'bold'),
                            fg=self.colors['matrix_green'], 
                            bg=self.colors['card_bg'])
        list_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(departures_header, text=">>> DATA STREAM <<<", 
                font=self.fonts['header'],
                fg=self.colors['matrix_green'], bg=self.colors['card_bg']).pack(side=tk.LEFT)
        
        # Enhanced matrix-style departures list
        list_container = tk.Frame(departures_frame, bg=self.colors['darker'],
                                 relief=tk.SUNKEN, bd=3)
        list_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        
        # Cyberpunk scrollbar styling
        scrollbar = tk.Scrollbar(list_container, bg=self.colors['card_bg'], 
                                troughcolor=self.colors['darker'],
                                activebackground=self.colors['primary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.departures_listbox = tk.Listbox(list_container, 
                                            font=self.fonts['small'],
                                            bg=self.colors['darker'], 
                                            fg=self.colors['matrix_green'],
                                            selectbackground=self.colors['primary'],
                                            selectforeground=self.colors['bg'],
                                            borderwidth=0, 
                                            highlightthickness=0,
                                            activestyle='none',
                                            yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.departures_listbox.yview)
        self.departures_listbox.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Enhanced cyberpunk control buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X)
        
        # Refresh button with electric glow
        refresh_outer = tk.Frame(button_frame, bg=self.colors['primary'], 
                               relief=tk.RAISED, bd=3)
        refresh_outer.pack(side=tk.LEFT, padx=(0, 10))
        
        self.refresh_button = tk.Button(refresh_outer, 
                                       text=f"{self.safe_icon('refresh', '⟲')} REFRESH", 
                                       font=self.fonts['body'],
                                       bg=self.colors['primary'], 
                                       fg=self.colors['bg'],
                                       activebackground=self.colors['primary_light'], 
                                       activeforeground=self.colors['bg'],
                                       borderwidth=0,
                                       padx=20, pady=12,
                                       command=self.manual_refresh)
        self.refresh_button.pack(fill=tk.BOTH, expand=True)
        
        # Exit button with danger glow
        exit_outer = tk.Frame(button_frame, bg=self.colors['danger'], 
                            relief=tk.RAISED, bd=3)
        exit_outer.pack(side=tk.RIGHT)
        
        self.exit_button = tk.Button(exit_outer, 
                                    text=f"{self.safe_icon('cross', '✗')} EXIT", 
                                    font=self.fonts['body'],
                                    bg=self.colors['danger'], 
                                    fg=self.colors['text'],
                                    activebackground=self.colors['danger_light'], 
                                    activeforeground=self.colors['text'],
                                    borderwidth=0,
                                    padx=20, pady=12,
                                    command=self.root.quit)
        self.exit_button.pack(fill=tk.BOTH, expand=True)
        
        # Start enhanced cyberpunk animation
        self.animate_cyberpunk_ui()
    
    def setup_mvg_api(self):
        """Initialize MVG API connection with cyberpunk status messages"""
        try:
            self.status_label.config(text=">>> ESTABLISHING NEURAL LINK <<<")
            self.status_icon.config(text=self.safe_icon('electric', '⚡'))
            self.station = MvgApi.station('Parkring Süd')
            if self.station:
                self.mvgapi = MvgApi(self.station['id'])
                self.status_label.config(text=">>> NEURAL LINK ESTABLISHED <<<", fg=self.colors['success'])
                self.status_icon.config(text=self.safe_icon('check', '✓'), fg=self.colors['success'])
            else:
                self.status_label.config(text=">>> STATION NOT FOUND <<<", fg=self.colors['danger'])
                self.status_icon.config(text=self.safe_icon('cross', '✗'), fg=self.colors['danger'])
        except Exception as e:
            self.status_label.config(text=f">>> CONNECTION ERROR: {str(e)[:20]}... <<<", fg=self.colors['danger'])
            self.status_icon.config(text=self.safe_icon('cross', '✗'), fg=self.colors['danger'])
    
    def get_departures(self):
        """Fetch departures from MVG API with optimization"""
        if not self.mvgapi:
            return []
        
        try:
            # Fetch departures efficiently
            departures = self.mvgapi.departures(
                limit=10,
                offset=0,
                transport_types=[TransportType.REGIONAL_BUS]
            )
            
            # Filter for target destination
            filtered_departures = [
                dep for dep in departures 
                if dep['destination'] == self.target_destination
            ]
            
            return filtered_departures
            
        except Exception as e:
            self.status_label.config(text=f">>> DATA FETCH ERROR: {str(e)[:15]}... <<<", fg=self.colors['danger'])
            self.status_icon.config(text=self.safe_icon('cross', '✗'), fg=self.colors['danger'])
            return []
    
    def format_time(self, timestamp):
        """Convert timestamp to readable time"""
        return datetime.fromtimestamp(timestamp).strftime('%H:%M')
    
    def calculate_leave_time(self, departure_timestamp):
        """Calculate when to leave office"""
        departure_time = datetime.fromtimestamp(departure_timestamp)
        leave_time = departure_time - timedelta(minutes=self.walk_time_minutes)
        return leave_time
    
    def update_departures(self):
        """Update the departures display with cyberpunk styling"""
        departures = self.get_departures()
        
        # Clear previous entries
        self.departures_listbox.delete(0, tk.END)
        
        if not departures:
            self.departures_listbox.insert(tk.END, f"{self.safe_icon('warning', '⚠')} >>> NO DATA STREAMS TO TARGET <<<")
            self.next_bus_label.config(text=">>> NO UPCOMING TRANSPORTS <<<")
            self.countdown_label.config(text="--:--")
            self.leave_time_label.config(text="")
            self.leave_time_icon.config(text=self.safe_icon('warning', '⚠'), fg=self.colors['warning'])
            return
        
        current_time = datetime.now()
        
        # Process next departure for countdown
        next_departure = departures[0]
        departure_time = datetime.fromtimestamp(next_departure['time'])
        leave_time = self.calculate_leave_time(next_departure['time'])
        
        time_until_departure = departure_time - current_time
        time_until_leave = leave_time - current_time
        
        minutes_until_departure = max(0, int(time_until_departure.total_seconds() / 60))
        minutes_until_leave = max(0, int(time_until_leave.total_seconds() / 60))
        
        # Update next bus info with cyberpunk styling
        self.next_bus_label.config(text=f">>> TRANSPORT {next_departure['line']} → {next_departure['destination'][:30]}... <<<")
        
        # Update countdown display
        if minutes_until_departure <= 0:
            self.countdown_label.config(text=">>> DEPARTED <<<", fg=self.colors['danger'])
        else:
            self.countdown_label.config(text=f">>> {minutes_until_departure} MIN REMAINING <<<", 
                                       fg=self.colors['primary'])
        
        # Update leave time display with cyberpunk alerts
        if minutes_until_leave <= 0 and minutes_until_departure > 0:
            # Enhanced LEAVE NOW alert
            alert_text = f">>> LEAVE NOW! LEAVE NOW! <<<\n>>> TRANSPORT {next_departure['line']} IN {minutes_until_departure} MIN <<<"
            self.show_leave_now_alert(alert_text)
            self.leave_time_label.config(text=f">>> LEAVE NOW! LEAVE NOW! <<<", fg=self.colors['danger'])
            self.leave_time_icon.config(text=self.safe_icon('alert', '⚡'), fg=self.colors['danger'])
        elif minutes_until_leave <= 2:
            self.leave_time_label.config(text=f">>> PREPARE TO LEAVE IN {minutes_until_leave} MIN <<<", 
                                        fg=self.colors['warning'])
            self.leave_time_icon.config(text=self.safe_icon('warning', '⚠'), fg=self.colors['warning'])
            self.hide_leave_now_alert()
        else:
            self.leave_time_label.config(text=f">>> DEPARTURE IN {minutes_until_leave} MINUTES <<<", 
                                        fg=self.colors['success'])
            self.leave_time_icon.config(text=self.safe_icon('check', '✓'), fg=self.colors['success'])
            self.hide_leave_now_alert()
        
        # Update departures list with cyberpunk matrix-style formatting
        for i, dep in enumerate(departures):
            departure_time = datetime.fromtimestamp(dep['time'])
            leave_time = self.calculate_leave_time(dep['time'])
            
            time_until_departure = departure_time - current_time
            time_until_leave = leave_time - current_time
            
            minutes_until_departure = max(0, int(time_until_departure.total_seconds() / 60))
            minutes_until_leave = max(0, int(time_until_leave.total_seconds() / 60))
            
            # Cyberpunk status indicators
            if minutes_until_departure <= 0:
                status_icon = self.safe_icon('status_red', '●')
                status = "DEPARTED"
            elif minutes_until_leave <= 0:
                status_icon = self.safe_icon('alert', '⚡')
                status = "LEAVE NOW!"
            elif minutes_until_leave <= 2:
                status_icon = self.safe_icon('warning', '⚠')
                status = f"PREP {minutes_until_leave}MIN"
            elif minutes_until_leave <= 5:
                status_icon = self.safe_icon('status_yellow', '●')
                status = f"WAIT {minutes_until_leave}MIN"
            else:
                status_icon = self.safe_icon('status_green', '●')
                status = f"STANDBY {minutes_until_leave}MIN"
            
            display_text = f"{status_icon} LINE{dep['line']} | {self.format_time(dep['time'])} | {status} | ETA-{minutes_until_departure}MIN"
            
            self.departures_listbox.insert(tk.END, display_text)
        
        # Update status with cyberpunk timestamp
        self.status_label.config(text=f">>> LAST SYNC: {current_time.strftime('%H:%M:%S')} <<<", 
                                fg=self.colors['success'])
        self.status_icon.config(text=self.safe_icon('check', '✓'), fg=self.colors['success'])
    
    def show_leave_now_alert(self, message):
        """Show prominent cyberpunk leave now alert"""
        if not self.leave_now_active:
            self.leave_now_active = True
            self.leave_now_label.config(text=message)
            self.leave_now_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
            # Start cyberpunk flashing effect
            self.flash_cyberpunk_alert()
    
    def hide_leave_now_alert(self):
        """Hide the leave now alert"""
        if self.leave_now_active:
            self.leave_now_active = False
            self.leave_now_frame.pack_forget()
    
    def flash_cyberpunk_alert(self):
        """Flash the alert with cyberpunk color cycling"""
        if not self.leave_now_active:
            return
            
        # Cycle through cyberpunk colors
        colors = [self.colors['danger'], self.colors['laser_red'], 
                 self.colors['warning'], self.colors['electric_purple']]
        color_index = (self.animation_frame // 8) % len(colors)
        current_color = colors[color_index]
        
        self.leave_now_frame.config(bg=current_color)
        self.leave_now_label.config(bg=current_color)
        
        # Continue flashing
        self.root.after(200, self.flash_cyberpunk_alert)
    
    def animate_cyberpunk_ui(self):
        """Enhanced cyberpunk UI animation with multiple effects"""
        self.animation_frame = (self.animation_frame + 1) % 360
        self.color_cycle_position = (self.color_cycle_position + 0.02) % 1.0
        
        # Enhanced pulsing effect for title
        if self.animation_frame % 3 == 0:  # Update every 3 frames
            self.pulse_intensity = 0.5 + 0.3 * math.sin(self.animation_frame * 0.1)
            
            # Cyberpunk title color cycling
            if hasattr(self, 'title_label'):
                # Cycle through neon colors
                cycle_pos = self.color_cycle_position
                if cycle_pos < 0.25:
                    title_color = self.colors['primary']
                elif cycle_pos < 0.5:
                    title_color = self.colors['electric_blue']
                elif cycle_pos < 0.75:
                    title_color = self.colors['secondary']
                else:
                    title_color = self.colors['electric_purple']
                self.title_label.config(fg=title_color)
            
            # Animate cyberpunk bus icon with rapid color cycling
            if hasattr(self, 'bus_icon_label'):
                # Faster color cycling for more dynamic effect
                icon_cycle = (self.animation_frame * 0.1) % 1.0
                if icon_cycle < 0.2:
                    icon_color = self.colors['electric_blue']
                elif icon_cycle < 0.4:
                    icon_color = self.colors['matrix_green']
                elif icon_cycle < 0.6:
                    icon_color = self.colors['laser_red']
                elif icon_cycle < 0.8:
                    icon_color = self.colors['electric_purple']
                else:
                    icon_color = self.colors['highlight']
                self.bus_icon_label.config(fg=icon_color)
        
        # Animate subtitle with matrix-style effect
        if self.animation_frame % 20 == 0 and hasattr(self, 'subtitle_label'):
            # Alternate between different cyberpunk messages
            messages = [
                ">>> CYBERPUNK TRANSIT INTERFACE <<<",
                ">>> NEURAL LINK ACTIVE <<<",
                ">>> MATRIX TRANSPORT MONITOR <<<",
                ">>> DIGITAL DEPARTURE SYSTEM <<<"
            ]
            message_index = (self.animation_frame // 20) % len(messages)
            self.subtitle_label.config(text=messages[message_index])
        
        # Animate status icon with electric pulse
        if self.animation_frame % 15 == 0 and hasattr(self, 'status_icon'):
            base_size = 28
            pulse_size = base_size + int(4 * self.pulse_intensity)
            self.status_icon.config(font=('Helvetica', pulse_size, 'bold'))
        
        # Matrix-style effect for departures list background
        if self.animation_frame % 60 == 0 and hasattr(self, 'departures_listbox'):
            # Subtle background color shifting
            bg_colors = [self.colors['darker'], self.colors['dark'], self.colors['card_bg']]
            bg_index = (self.animation_frame // 60) % len(bg_colors)
            self.departures_listbox.config(bg=bg_colors[bg_index])
        
        # Animate button glow effects
        if self.animation_frame % 10 == 0:
            if hasattr(self, 'refresh_button'):
                # Pulse the refresh button
                glow_colors = [self.colors['primary'], self.colors['primary_light'], self.colors['electric_blue']]
                glow_index = (self.animation_frame // 10) % len(glow_colors)
                self.refresh_button.config(bg=glow_colors[glow_index])
        
        # Continue cyberpunk animation
        self.root.after(self.animation_speed, self.animate_cyberpunk_ui)
    
    def manual_refresh(self):
        """Manual refresh with cyberpunk visual feedback"""
        self.update_departures()
        
        # Enhanced button feedback with color cycling
        original_bg = self.refresh_button.cget('bg')
        feedback_colors = [self.colors['success'], self.colors['matrix_green'], self.colors['accent']]
        
        def cycle_feedback(index=0):
            if index < len(feedback_colors):
                self.refresh_button.config(bg=feedback_colors[index])
                self.root.after(100, lambda: cycle_feedback(index + 1))
            else:
                self.refresh_button.config(bg=original_bg)
        
        cycle_feedback()
    
    def start_monitoring(self):
        """Start the monitoring thread with better error handling"""
        def monitor_loop():
            while True:
                try:
                    # Schedule UI update on main thread
                    self.root.after(0, self.update_departures)
                    time.sleep(self.update_interval)
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(30)  # Wait longer on error
        
        # Start monitoring in background thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        # Initial update after UI setup
        self.root.after(2000, self.update_departures)

def main():
    root = tk.Tk()
    app = MunichBusTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main() 