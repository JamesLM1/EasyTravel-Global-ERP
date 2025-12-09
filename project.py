import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
import json
import datetime
import random

# ==========================================
# 🎨 TEMA UI
# ==========================================
THEME = {
    "bg_dark": "#1e272e",      
    "bg_main": "#f5f6fa",      
    "primary": "#575fcf",      
    "secondary": "#ff3f34",    
    "success": "#0be881",      
    "text_light": "#d2dae2",
    "text_dark": "#2d3436"
}

# ==========================================
# 🌍 BASE DE DATOS MUNDIAL (DATA SEED)
# ==========================================
WORLD_DB = {
    "Perú": {
        "cities": {
            "Lima": (0.28, 0.45), "Cusco": (0.32, 0.40), "Arequipa": (0.30, 0.35), 
            "Trujillo": (0.25, 0.55), "Ica": (0.28, 0.42), "Piura": (0.22, 0.60),
            "Tacna": (0.33, 0.30), "Iquitos": (0.35, 0.60), "Pucallpa": (0.30, 0.50), "Juliaca": (0.34, 0.35)
        },
        "routes": [
            ("Lima", "Cusco", 60, 1.2), ("Lima", "Arequipa", 50, 1.5), ("Lima", "Trujillo", 40, 1.0),
            ("Lima", "Iquitos", 70, 1.8), ("Cusco", "Arequipa", 40, 0.8), ("Trujillo", "Piura", 30, 3.0),
            ("Lima", "Ica", 20, 4.0), ("Arequipa", "Tacna", 25, 5.0), ("Arequipa", "Juliaca", 20, 4.0)
        ]
    },
    "USA": {
        "cities": {
            "New York": (0.25, 0.85), "Los Angeles": (0.10, 0.80), "Miami": (0.28, 0.75), 
            "Chicago": (0.22, 0.82), "Las Vegas": (0.12, 0.81), "San Francisco": (0.09, 0.83)
        },
        "routes": [
            ("New York", "Los Angeles", 200, 5.5), ("New York", "Miami", 120, 3.0),
            ("Los Angeles", "Las Vegas", 50, 1.0), ("Chicago", "New York", 90, 2.5),
            ("San Francisco", "Los Angeles", 60, 1.2)
        ]
    },
    "España": {
        "cities": {
            "Madrid": (0.55, 0.82), "Barcelona": (0.58, 0.84), "Sevilla": (0.54, 0.79), "Valencia": (0.57, 0.81)
        },
        "routes": [("Madrid", "Barcelona", 80, 1.0), ("Madrid", "Sevilla", 60, 0.9), ("Barcelona", "Valencia", 40, 2.0)]
    },
    "Brasil": {
        "cities": {
            "Sao Paulo": (0.45, 0.35), "Rio de Janeiro": (0.48, 0.37), "Brasilia": (0.44, 0.45), "Salvador": (0.50, 0.50)
        },
        "routes": [("Sao Paulo", "Rio de Janeiro", 50, 1.0), ("Brasilia", "Sao Paulo", 70, 1.5)]
    },
    "México": {
        "cities": {
            "CDMX": (0.15, 0.65), "Cancún": (0.22, 0.68), "Guadalajara": (0.12, 0.66), "Monterrey": (0.16, 0.72)
        },
        "routes": [("CDMX", "Cancún", 100, 2.0), ("CDMX", "Guadalajara", 50, 1.0), ("Monterrey", "CDMX", 60, 1.5)]
    },
    "Japón": {
        "cities": {
            "Tokyo": (0.85, 0.80), "Osaka": (0.82, 0.78), "Kyoto": (0.83, 0.79), "Hiroshima": (0.80, 0.77)
        },
        "routes": [("Tokyo", "Osaka", 130, 2.5), ("Osaka", "Kyoto", 15, 0.5), ("Tokyo", "Hiroshima", 150, 4.0)]
    },
    "Italia": {
        "cities": {
            "Roma": (0.62, 0.80), "Milán": (0.60, 0.85), "Venecia": (0.63, 0.86), "Nápoles": (0.63, 0.78)
        },
        "routes": [("Roma", "Milán", 90, 3.0), ("Roma", "Venecia", 85, 3.5), ("Roma", "Nápoles", 40, 1.2)]
    },
    "Francia": {
        "cities": {
            "París": (0.52, 0.88), "Lyon": (0.53, 0.84), "Marsella": (0.54, 0.81), "Niza": (0.55, 0.82)
        },
        "routes": [("París", "Lyon", 70, 2.0), ("París", "Marsella", 100, 3.2), ("Marsella", "Niza", 30, 2.5)]
    },
    "Reino Unido": {
        "cities": {
            "Londres": (0.50, 0.90), "Manchester": (0.49, 0.93), "Liverpool": (0.48, 0.92), "Edimburgo": (0.48, 0.96)
        },
        "routes": [("Londres", "Manchester", 60, 2.0), ("Manchester", "Liverpool", 15, 0.8), ("Londres", "Edimburgo", 90, 4.5)]
    },
    "Alemania": {
        "cities": {
            "Berlín": (0.60, 0.90), "Múnich": (0.58, 0.86), "Frankfurt": (0.56, 0.88), "Hamburgo": (0.58, 0.93)
        },
        "routes": [("Berlín", "Múnich", 80, 4.0), ("Frankfurt", "Berlín", 75, 3.5), ("Hamburgo", "Berlín", 40, 2.0)]
    }
}

# Rutas Internacionales (Conectando el grafo global)
INTERNATIONAL_ROUTES = [
    ("Lima", "Miami", 400, 5.5), ("Lima", "Madrid", 900, 11.0), ("Lima", "CDMX", 350, 6.0),
    ("Lima", "Sao Paulo", 300, 4.5), ("Lima", "Santiago", 200, 3.5),
    ("New York", "Londres", 600, 7.0), ("Madrid", "París", 100, 2.0), ("Londres", "París", 80, 2.5),
    ("Madrid", "Roma", 120, 2.5), ("Los Angeles", "Tokyo", 800, 11.0), ("Sao Paulo", "Madrid", 850, 10.0)
]

# ==========================================
# 🧠 BACKEND
# ==========================================
class TransportCore:
    def __init__(self):
        self.G = nx.DiGraph()
        self.sales_history = []
        self.city_country_map = {} # Diccionario para saber a qué país pertenece cada ciudad
        self._init_world_data()

    def _init_world_data(self):
        # Cargar Paises
        for country, data in WORLD_DB.items():
            for city, pos in data['cities'].items():
                self.add_node(city, pos, country)
            
            for u, v, p, t in data['routes']:
                self.add_route(u, v, p, t)
        
        # Cargar Rutas Internacionales
        for u, v, p, t in INTERNATIONAL_ROUTES:
            self.add_route(u, v, p, t, is_international=True)

    def add_node(self, name, pos=None, country="Desconocido"):
        if not pos: pos = (random.random(), random.random())
        self.G.add_node(name, pos=pos, country=country)
        self.city_country_map[name] = country

    def add_route(self, u, v, price, time, is_international=False):
        # Capacidad: Si es internacional, aviones grandes (300), si no, buses/trenes (50)
        cap = 300 if is_international else 50
        if u in self.G.nodes and v in self.G.nodes:
            self.G.add_edge(u, v, price=price, time=time, capacity=cap, type="intl" if is_international else "dom")
            return True
        return False

    def get_cities_by_country(self, country_name):
        if country_name == "Mundo / Internacional":
            return sorted(list(self.G.nodes))
        
        # Filtrar nodos que tengan el atributo country igual al seleccionado
        return sorted([n for n, attr in self.G.nodes(data=True) if attr.get('country') == country_name])

    def find_best_route(self, start, end, criteria='price'):
        try:
            path = nx.dijkstra_path(self.G, start, end, weight=criteria)
            total_price = sum(self.G[path[i]][path[i+1]]['price'] for i in range(len(path)-1))
            total_time = sum(self.G[path[i]][path[i+1]]['time'] for i in range(len(path)-1))
            return path, total_price, total_time
        except nx.NetworkXNoPath:
            return None, 0, 0

    def register_sale(self, origin, dest, price):
        self.sales_history.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "origin": origin, "dest": dest, "amount": price
        })

    def get_analytics(self):
        total = sum(x['amount'] for x in self.sales_history)
        return total, len(self.sales_history)

    def save_db(self, filename):
        data = nx.node_link_data(self.G)
        with open(filename, 'w') as f: json.dump({"graph": data, "sales": self.sales_history}, f)

    def load_db(self, filename):
        with open(filename, 'r') as f: data = json.load(f)
        self.G = nx.node_link_graph(data['graph'])
        self.sales_history = data['sales']
        # Reconstruir mapa de ciudades
        self.city_country_map = {n: attr.get('country', 'Desconocido') for n, attr in self.G.nodes(data=True)}

# ==========================================
# 🖥️ FRONTEND
# ==========================================
class UltimateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EasyTravel GLOBAL SYSTEM | v6.0 World Edition")
        self.geometry("1400x900")
        self.state('zoomed')
        self.core = TransportCore()
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=THEME['bg_main'], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 5])
        style.map("TNotebook.Tab", background=[("selected", THEME['primary'])], foreground=[("selected", "white")])
        
        self._init_layout()

    def _init_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=THEME['bg_dark'], width=300)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y); self.sidebar.pack_propagate(False)
        self._build_sidebar()
        
        # Main
        self.main_area = tk.Frame(self, bg=THEME['bg_main'])
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(self.main_area)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab_map = tk.Frame(self.notebook, bg="white"); self.notebook.add(self.tab_map, text="🗺️ Mapa Global")
        self._build_map_tab()
        
        self.tab_booking = tk.Frame(self.notebook, bg="white"); self.notebook.add(self.tab_booking, text="✈️ Booking & Reservas")
        self._build_booking_tab()
        
        self.tab_bi = tk.Frame(self.notebook, bg="white"); self.notebook.add(self.tab_bi, text="📊 Analytics")
        self._build_bi_tab()
        
        self.tab_db = tk.Frame(self.notebook, bg="white"); self.notebook.add(self.tab_db, text="💾 Data")
        self._build_db_tab()

        # Inicializar vistas
        self.refresh_map()

    # --- SIDEBAR ---
    def _build_sidebar(self):
        tk.Label(self.sidebar, text="EasyTravel\nGLOBAL", font=("Montserrat", 24, "bold"), bg=THEME['bg_dark'], fg="white").pack(pady=(30, 5))
        tk.Label(self.sidebar, text="International Logistics", font=("Arial", 9, "italic"), bg=THEME['bg_dark'], fg=THEME['primary']).pack(pady=(0, 30))
        
        self._lbl_sep("ADMINISTRACIÓN DE RUTAS")
        
        # Selector de País para Admin
        tk.Label(self.sidebar, text="Filtrar País:", bg=THEME['bg_dark'], fg="white").pack(fill=tk.X, padx=20)
        self.cb_admin_country = ttk.Combobox(self.sidebar, values=["Mundo / Internacional"] + list(WORLD_DB.keys()), state="readonly")
        self.cb_admin_country.pack(fill=tk.X, padx=20, pady=5)
        self.cb_admin_country.current(0)
        self.cb_admin_country.bind("<<ComboboxSelected>>", self._update_admin_combos)

        # Origen / Destino Admin
        self.cb_adm_orig = self._sidebar_combo("Origen:")
        self.cb_adm_dest = self._sidebar_combo("Destino:")
        self.entry_price = self._sidebar_entry("Precio ($):")
        
        tk.Button(self.sidebar, text="🔗 Crear Conexión", bg=THEME['primary'], fg="white", bd=0, pady=8, command=self.action_add_route).pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(self.sidebar, text="Dev: James Lucas Moreto", font=("Arial", 8), bg=THEME['bg_dark'], fg="#636e72").pack(side=tk.BOTTOM, pady=10)

    # --- MAP TAB ---
    def _build_map_tab(self):
        # Control de Filtro de Mapa
        ctrl_frame = tk.Frame(self.tab_map, bg="white", pady=10)
        ctrl_frame.pack(fill=tk.X, padx=20)
        tk.Label(ctrl_frame, text="Visualizar País:", bg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        
        self.cb_map_filter = ttk.Combobox(ctrl_frame, values=["Mundo / Internacional"] + list(WORLD_DB.keys()), state="readonly", width=20)
        self.cb_map_filter.current(0)
        self.cb_map_filter.pack(side=tk.LEFT, padx=10)
        self.cb_map_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_map())

        self.fig_map, self.ax_map = plt.subplots(figsize=(6, 5))
        self.canvas_map = FigureCanvasTkAgg(self.fig_map, master=self.tab_map)
        self.canvas_map.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # --- BOOKING TAB ---
    def _build_booking_tab(self):
        top_panel = tk.Frame(self.tab_booking, bg=THEME['bg_main'], pady=20)
        top_panel.pack(fill=tk.X)
        
        # Selector de País Booking
        tk.Label(top_panel, text="País:", bg=THEME['bg_main'], font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10)
        self.cb_book_country = ttk.Combobox(top_panel, values=["Mundo / Internacional"] + list(WORLD_DB.keys()), state="readonly", width=18)
        self.cb_book_country.current(0)
        self.cb_book_country.pack(side=tk.LEFT, padx=5)
        self.cb_book_country.bind("<<ComboboxSelected>>", self._update_booking_combos)

        tk.Label(top_panel, text="|  De:", bg=THEME['bg_main']).pack(side=tk.LEFT, padx=10)
        self.cb_b_orig = ttk.Combobox(top_panel, width=15); self.cb_b_orig.pack(side=tk.LEFT)
        
        tk.Label(top_panel, text="A:", bg=THEME['bg_main']).pack(side=tk.LEFT, padx=10)
        self.cb_b_dest = ttk.Combobox(top_panel, width=15); self.cb_b_dest.pack(side=tk.LEFT)
        
        tk.Button(top_panel, text="✈️ BUSCAR VUELO/VIAJE", bg=THEME['secondary'], fg="white", font=("Arial", 10, "bold"), bd=0, padx=15, command=self.action_quote).pack(side=tk.LEFT, padx=20)

        # Ticket Area
        self.ticket_frame = tk.Frame(self.tab_booking, bg="white", bd=1, relief=tk.SOLID)
        self.ticket_frame.pack(pady=30, ipadx=50, ipady=30)
        self.lbl_ticket = tk.Label(self.ticket_frame, text="Seleccione destino...", font=("Courier New", 14), bg="white")
        self.lbl_ticket.pack(pady=10)
        self.btn_buy = tk.Button(self.ticket_frame, text="CONFIRMAR COMPRA", bg=THEME['success'], fg="white", font=("Arial", 12, "bold"), state="disabled", command=self.action_buy)
        self.btn_buy.pack(fill=tk.X, padx=20)

    # --- BI & DB TABS (Standard) ---
    def _build_bi_tab(self):
        self.fig_bi, self.ax_bi = plt.subplots(figsize=(6, 4))
        self.canvas_bi = FigureCanvasTkAgg(self.fig_bi, master=self.tab_bi)
        self.canvas_bi.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def _build_db_tab(self):
        f = tk.Frame(self.tab_db, bg="white"); f.pack(expand=True)
        tk.Button(f, text="💾 GUARDAR DB", bg=THEME['primary'], fg="white", font=("Arial", 12), width=25, pady=10, command=self.action_save).pack(pady=10)
        tk.Button(f, text="📂 CARGAR DB", bg="#34495e", fg="white", font=("Arial", 12), width=25, pady=10, command=self.action_load).pack(pady=10)

    # ==========================================
    # 🧠 LÓGICA DE EVENTOS
    # ==========================================
    
    def _update_admin_combos(self, event=None):
        country = self.cb_admin_country.get()
        cities = self.core.get_cities_by_country(country)
        self.cb_adm_orig['values'] = cities
        self.cb_adm_dest['values'] = cities
        self.cb_adm_orig.set(''); self.cb_adm_dest.set('')

    def _update_booking_combos(self, event=None):
        country = self.cb_book_country.get()
        cities = self.core.get_cities_by_country(country)
        self.cb_b_orig['values'] = cities
        self.cb_b_dest['values'] = cities
        self.cb_b_orig.set(''); self.cb_b_dest.set('')

    def refresh_map(self, highlight_path=None):
        self.ax_map.clear()
        
        # Filtro de país
        filter_country = self.cb_map_filter.get()
        
        if filter_country == "Mundo / Internacional":
            nodes_to_draw = self.core.G.nodes
        else:
            nodes_to_draw = [n for n, attr in self.core.G.nodes(data=True) if attr.get('country') == filter_country]

        subgraph = self.core.G.subgraph(nodes_to_draw)
        pos = nx.get_node_attributes(subgraph, 'pos')
        
        # Diseño de Nodos Grandes
        nx.draw_networkx_nodes(subgraph, pos, ax=self.ax_map, node_size=1300, node_color=THEME['primary'], edgecolors='black', alpha=0.9)
        nx.draw_networkx_labels(subgraph, pos, ax=self.ax_map, font_size=8, font_color="white", font_weight="bold")
        nx.draw_networkx_edges(subgraph, pos, ax=self.ax_map, edge_color="#bdc3c7", arrows=True, arrowsize=15, width=1.5)
        
        # Resaltar ruta
        if highlight_path:
            # Filtrar ruta para que solo se dibuje si los nodos están visibles
            visible_path = [n for n in highlight_path if n in nodes_to_draw]
            if len(visible_path) > 1:
                path_edges = [(visible_path[i], visible_path[i+1]) for i in range(len(visible_path)-1) if visible_path[i+1] in subgraph[visible_path[i]]]
                nx.draw_networkx_edges(subgraph, pos, edgelist=path_edges, ax=self.ax_map, edge_color=THEME['secondary'], width=4)
                nx.draw_networkx_nodes(subgraph, pos, nodelist=visible_path, ax=self.ax_map, node_color=THEME['secondary'], node_size=1400)

        self.ax_map.set_title(f"Vista: {filter_country}", fontsize=12)
        self.ax_map.axis("off")
        self.canvas_map.draw()
        
        # Actualizar combos iniciales
        self._update_admin_combos()
        self._update_booking_combos()

    def action_add_route(self):
        try:
            u, v = self.cb_adm_orig.get(), self.cb_adm_dest.get()
            p = float(self.entry_price.get())
            if self.core.add_route(u, v, p, p/50):
                self.refresh_map()
                messagebox.showinfo("OK", "Ruta Creada")
            else: messagebox.showerror("Error", "Error al crear ruta")
        except: messagebox.showerror("Error", "Datos inválidos")

    def action_quote(self):
        u, v = self.cb_b_orig.get(), self.cb_b_dest.get()
        if not u or not v: return
        path, price, time = self.core.find_best_route(u, v)
        
        if path:
            self.lbl_ticket.config(text=f"Ruta: {' -> '.join(path)}\n\nPrecio: ${price:.2f} | Tiempo: {time:.1f}h", fg="black")
            self.btn_buy.config(state="normal")
            self.current_quote = (u, v, price)
            self.refresh_map(highlight_path=path)
        else:
            self.lbl_ticket.config(text="🚫 Ruta no disponible", fg="red")

    def action_buy(self):
        if hasattr(self, 'current_quote'):
            u, v, p = self.current_quote
            self.core.register_sale(u, v, p)
            messagebox.showinfo("Vendido", "Pasaje comprado exitosamente")
            self.btn_buy.config(state="disabled")
            self._update_bi()

    def _update_bi(self):
        tot, count = self.core.get_analytics()
        self.ax_bi.clear()
        self.ax_bi.bar(["Ventas Totales", "Tickets"], [tot, count], color=[THEME['success'], THEME['primary']])
        self.canvas_bi.draw()

    def action_save(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if f: self.core.save_db(f)

    def action_load(self):
        f = filedialog.askopenfilename()
        if f: 
            self.core.load_db(f)
            self.refresh_map()
            messagebox.showinfo("Cargado", "Base de datos actualizada")

    # Helpers UI
    def _sidebar_entry(self, label):
        tk.Label(self.sidebar, text=label, bg=THEME['bg_dark'], fg="white").pack(anchor="w", padx=20)
        e = tk.Entry(self.sidebar); e.pack(fill=tk.X, padx=20, pady=5)
        return e
    
    def _sidebar_combo(self, label):
        tk.Label(self.sidebar, text=label, bg=THEME['bg_dark'], fg="white").pack(anchor="w", padx=20)
        cb = ttk.Combobox(self.sidebar); cb.pack(fill=tk.X, padx=20, pady=5)
        return cb
    
    def _lbl_sep(self, text):
        tk.Label(self.sidebar, text=text, bg=THEME['bg_dark'], fg="gray", font=("Arial", 8, "bold")).pack(fill=tk.X, padx=20, pady=(20, 5))

if __name__ == "__main__":
    app = UltimateApp()
    app.mainloop()