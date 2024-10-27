import customtkinter as ctk
import keyboard
import time
import os
import json  # Importar el módulo json para exportar e importar
from threading import Thread
from tkinter import font
from PIL import Image


class MacroRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("GSmacro")
        self.root.iconbitmap("raton.ico")
        self.recording = False
        self.playing = False
        self.loop_playback = False
        self.keys_pressed = []
        self.times_pressed = []
        self.start_time = None
        self.last_key = None
        grabar_key = "F1"
        reproducir_key = "F6"
        self.interval_factor = 1  # Factor del slider

        # Configurar fondo personalizado
        self.set_custom_background()
        

        # Marco principal
        frame = ctk.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Iconos
        self.icon_eng = ctk.CTkImage(Image.open("mengranaje.png"), size=(30, 30))
        self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(50, 50))
        self.import_logo = ctk.CTkImage(Image.open("import.png"), size=(30, 30))  # Nuevo logo para importar/exportar

        # Logo en la esquina superior derecha
        logo_label = ctk.CTkLabel(master=frame, text=" ", image=self.logo_image)
        logo_label.pack(side="right", padx=(0, 5))

        # Título
        label = ctk.CTkLabel(master=frame, text="GSmacro", font=("Arial", 20))
        label.pack(side="left", padx=10)

        # Botones de inicio y reproducción
        self.start_button = ctk.CTkButton(root, text=f"Iniciar Grabación ({grabar_key})", command=self.toggle_recording)
        self.start_button.pack(pady=5)

        self.play_button = ctk.CTkButton(root, text=f"Reproducir Macro ({reproducir_key})", command=self.start_playing)
        self.play_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(root, text="Detener Reproducción", command=self.stop_playing, state="disabled")
        self.stop_button.pack(pady=5)

        # Opciones de bucle y siempre en primer plano
        self.loop_var = ctk.BooleanVar()
        self.loop_check = ctk.CTkCheckBox(root, text="Reproducir en Bucle", variable=self.loop_var)
        self.loop_check.pack()

        self.always_on_top_var = ctk.BooleanVar()
        self.always_on_top_check = ctk.CTkCheckBox(root, text="Dejar en primer plano siempre", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.always_on_top_check.pack()

        # Slider para el intervalo de reproducción
        self.interval_slider = ctk.CTkSlider(root, from_=0.5, to=2, command=self.update_interval)
        self.interval_slider.set(1)
        self.interval_slider.pack(pady=10)
        self.interval_label = ctk.CTkLabel(root, text=f"Ajuste de Intervalo: {self.interval_factor}")
        self.interval_label.pack()

        # Botón de Créditos y Configuración
        self.credits_button = ctk.CTkButton(root, text="Créditos", command=self.show_credits, width=10)
        self.credits_button.pack(side="bottom", pady=10)

        self.settings_button = ctk.CTkButton(root, text="", image=self.icon_eng, command=self.open_settings, width=30, height=30)
        self.settings_button.place(relx=0.95, rely=0.95, anchor="se")

        # Botón de Exportar/Importar en la esquina inferior izquierda
        self.export_import_button = ctk.CTkButton(root, text="", image=self.import_logo, command=self.open_export_import_window, width=30, height=30)
        self.export_import_button.place(relx=0.05, rely=0.95, anchor="sw")

        # Configurar listeners de teclas F1 y F6
        root.bind('<F1>', lambda event: self.toggle_recording())
        root.bind('<F6>', lambda event: self.start_playing())

        # Listener de todas las teclas
        keyboard.on_press(self.record_key)

    def set_custom_background(self):
        # Cargar fondo personalizado si el archivo existe y no excede el tamaño
        for ext in ("background.jpg", "background.png"):
            if os.path.exists(ext) and os.path.getsize(ext) <= 5 * 1024 * 1024:  # Límite de 5 MB
                bg_image = ctk.CTkImage(Image.open(ext))
                self.root.configure(background_image=bg_image)
                break

    def update_interval(self, value):
        self.interval_factor = float(value)
        self.interval_label.configure(text=f"Ajuste de Intervalo: {self.interval_factor:.2f}")

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        global grabar_key
        self.recording = True
        self.keys_pressed.clear()
        self.times_pressed.clear()
        self.start_time = time.time()
        self.last_key = None
        self.start_button.configure(text=f"Detener Grabación (F1)")
        print("Grabación iniciada")

    def stop_recording(self):
        self.recording = False
        self.start_button.configure(text="Iniciar Grabación (F1)")
        print("Grabación detenida")

    def start_playing(self):
        if not self.keys_pressed:
            print("No hay teclas grabadas para reproducir.")
            return

        print("Reproduciendo macro...")
        self.playing = True
        self.play_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Ejecutar reproducción en un hilo
        Thread(target=self.play_macro).start()

    def stop_playing(self):
        self.playing = False
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def play_macro(self):
        # Minimizar la ventana si "Dejar en primer plano" está desactivado
        if not self.always_on_top_var.get():
            self.root.iconify()

        while self.playing:
            for key in self.keys_pressed:
                if not self.playing:  # Salir del bucle si se detiene
                    break
                keyboard.press(key)
                time.sleep(0.1 / self.interval_factor)  # Controlar el tiempo de presión de cada tecla ajustado por el slider
                keyboard.release(key)
                print(f"Tocado: {key}")

            if not self.loop_var.get():
                break

        if not self.always_on_top_var.get():
            self.root.deiconify()

        self.stop_playing()  # Reset al terminar reproducción

    def toggle_always_on_top(self):
        self.root.attributes('-topmost', self.always_on_top_var.get())

    def record_key(self, event):
        # Ignorar F1 y F6
        if not self.recording or event.name in ('f1', 'f6'):
            return

        # Registrar la tecla si es diferente a la última registrada para evitar duplicados
        elapsed = time.time() - self.start_time
        if event.name != self.last_key or elapsed > 0.1:
            self.keys_pressed.append(event.name)
            self.times_pressed.append(elapsed)
            self.start_time = time.time()
            self.last_key = event.name
            print(f"Grabado: {event.name} en {elapsed:.2f} seg")

    def show_credits(self):
        credits_window = ctk.CTkToplevel(self.root)
        credits_window.title("Créditos")

        credits_text = ctk.CTkTextbox(credits_window, width=300, height=100)
        credits_text.pack(pady=10)
        credits_text.insert("0.0", "Desarrollado por @else_. (Discord)\na petición de @sword0ntop.\n*Los derechos de uso de este programa son libres, agradecería que me dieras créditos. \nTe invito a hablarme por discord ante cualquier cosa. Gracias por leer ❤️‍🔥")
        credits_text.configure(state="disabled")

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Configuración")

        ctk.CTkLabel(settings_window, text="Personaliza las teclas:").pack(pady=10)

        ctk.CTkLabel(settings_window, text="Tecla para grabar:").pack(pady=5)
        self.record_key_entry = ctk.CTkEntry(settings_window)
        self.record_key_entry.pack(pady=5)

        ctk.CTkLabel(settings_window, text="Tecla para reproducir:").pack(pady=5)
        self.play_key_entry = ctk.CTkEntry(settings_window)
        self.play_key_entry.pack(pady=5)

        ctk.CTkButton(settings_window, text="Aceptar", command=self.set_custom_keys).pack(pady=10)

    def set_custom_keys(self):
        # Configurar las nuevas teclas de grabación y reproducción
        self.record_key = self.record_key_entry.get()
        self.play_key = self.play_key_entry.get()
        print(f"Nueva tecla de grabación: {self.record_key}, Nueva tecla de reproducción: {self.play_key}")

    def open_export_import_window(self):
        
        export_import_window = ctk.CTkToplevel(self.root)
        export_import_window.title("Agregar/Importar Macros")  # Cambiar título aquí
        
        frame = ctk.CTkFrame(master=export_import_window)
        frame.pack(pady=10, padx=30, fill="both", expand=False)
        
        # Etiqueta con el texto "Guardar y cargar macros"
        label = ctk.CTkLabel(master=frame, text="Guardar y cargar macros", font=("Arial", 15))
        label.pack(pady=10)

        ctk.CTkButton(export_import_window, text="Exportar Macro", command=self.export_macro).pack(pady=5)
        ctk.CTkButton(export_import_window, text="Importar Macro", command=self.import_macro).pack(pady=5)
        ctk.CTkLabel(label,  )

    def export_macro(self):
        with open("macro.json", "w") as f:
            json.dump({"keys": self.keys_pressed, "times": self.times_pressed}, f)
        print("Macro exportada como 'macro.json'")

    def import_macro(self):
        if os.path.exists("macro.json"):
            with open("macro.json", "r") as f:
                data = json.load(f)
            self.keys_pressed = data.get("keys", [])
            self.times_pressed = data.get("times", [])
            print("Macro importada desde 'macro.json'")
        else:
            print("No se encontró 'macro.json'")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = MacroRecorder(root)
    root.mainloop()
