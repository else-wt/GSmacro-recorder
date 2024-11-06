import customtkinter as ctk
import webbrowser
import threading
import keyboard
import time
import sys
import os
import json  # Importar el módulo json para exportar e importar
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from PIL import Image


def resource_path(relative_path):
    # Obtiene la ruta correcta para archivos empaquetados o para desarrollo.
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MacroRecorder:
    def __init__(self, root):
        global color_theme
        color_theme = "blue"
        ctk.set_default_color_theme(color_theme) 
        icon_path = resource_path('raton.ico')
        self.root = root
        self.root.iconbitmap(icon_path)
        self.root.title("GSmacro-recorder")
        self.interval_factor = 1 
        self.recording = False
        self.playing = False
        self.loop_playback = False
        self.keys_pressed = []
        self.times_pressed = []
        self.start_time = None
        self.last_key = None
        grabar_key = "F1"
        reproducir_key = "F6"
 


        # Marco principal
        frame = ctk.CTkFrame(master=root)
        frame.pack(pady=25, padx=83, fill="both", expand=True)

        # Iconos
        self.icon_eng = ctk.CTkImage(Image.open(resource_path("mengranaje.png")), size=(27, 27)) # engranaje
        self.logo_image = ctk.CTkImage(Image.open(resource_path("logo.png")), size=(50, 50)) # Logo del raton
        self.import_logo = ctk.CTkImage(Image.open(resource_path("import.png")), size=(30, 30))  # logo import
        self.temp_icon = ctk.CTkImage(Image.open(resource_path("temp.png")), size=(30, 30)) # icono de temporizador
        self.save_icon = ctk.CTkImage(Image.open(resource_path("save.png")), size=(21, 21)) # Icono de disquete - guardar
        self.github_icon = ctk.CTkImage(Image.open(resource_path("github.png")), size=(30, 30)) # Logo github
        self.game_icon = ctk.CTkImage(Image.open(resource_path("game.png")), size=(30, 30)) # Icono gamepad


        # Ratoncito en el texto de gsmacro
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
        self.interval_slider = ctk.CTkSlider(root, from_=0.0, to=2, number_of_steps=20, command=self.update_interval)
        self.interval_slider.set(1)
        self.interval_slider.pack(pady=10)
        if self.interval_factor == 1:
            self.interval_label = ctk.CTkLabel(root, text=f"Velocidad de intervalo: Original")
        else:
            self.interval_label = ctk.CTkLabel(root, text=f"Velocidad de intervalo: {self.interval_factor}")
        self.interval_label.pack()

        # Botón de Créditos y Configuración
        self.credits_button = ctk.CTkButton(root, text="Créditos", command=self.show_credits, width=10)
        self.credits_button.pack(side="bottom", pady=10)

        # Botón para abrir la ventana de cuenta regresiva
        self.countdown_button = ctk.CTkButton(root, text="", image=self.temp_icon, command=self.show_countdown_window, width=30, height=30)
        self.countdown_button.place(relx=0.05, rely=0.84, anchor="sw")  
        
        # Botón apartado de juegos
        self.settings_button = ctk.CTkButton(root, text="", image=self.game_icon, command=self.open_comingsoon, width=47, height=39)
        self.settings_button.place(relx=0.95, rely=0.84, anchor="se")
        
        # Botón de configuración
        self.settings_button = ctk.CTkButton(root, text="", image=self.icon_eng, command=self.open_settings, width=47, height=39)
        self.settings_button.place(relx=0.95, rely=0.95, anchor="se")

        # Botón de Exportar/Importar en la esquina inferior izquierda
        self.export_import_button = ctk.CTkButton(root, text="", image=self.import_logo, command=self.open_export_import_window, width=30, height=30)
        self.export_import_button.place(relx=0.05, rely=0.95, anchor="sw")

        # Configurar listeners de teclas F1 y F6
        root.bind('<F1>', lambda event: self.toggle_recording())
        root.bind('<F6>', lambda event: self.start_playing_with_countdown())
        
        # Listener de todas las teclas
        keyboard.on_press(self.record_key)

            # Dentro de __init__, agrega esta opción en la interfaz
        self.countdown_var = ctk.BooleanVar()

        # Función para el contador antes de reproducir
        def countdown(self, seconds):
            for i in range(seconds, 0, -1):
                print(f"Iniciando en {i}...")
                self.interval_label.configure(text=f"Iniciando en {i}...")
                time.sleep(1)
            self.interval_label.configure(text="Iniciando ahora...")

        # Modifica la función `start_playing` para que incluya el contador
        def start_playing(self):
            if not self.keys_pressed:
                print("No hay teclas grabadas para reproducir.")
                return

            # Si la casilla está marcada, ejecuta el contador de 3 segundos
            if self.countdown_var.get():
                self.countdown(3)

            print("Reproduciendo macro...")
            self.playing = True
            self.play_button.configure(state="disabled")
            self.stop_button.configure(state="normal")

            # Ejecutar reproducción en un hilo
            Thread(target=self.play_macro).start()



    def update_interval(self, value):
        self.interval_factor = float(value)
        self.interval_label.configure(text=f"Ajuste de Intervalo: {self.interval_factor:.2f}")

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.keys_pressed.clear()
        self.times_pressed.clear()
        self.start_time = time.time()
        self.last_key = None
        self.start_button.configure(text="Detener Grabación (F1)")
        print("Grabación iniciada")

    def stop_recording(self):
        self.recording = False
        self.start_button.configure(text="Iniciar Grabación (F1)")
        print("Grabación detenida")
        
    def play_macro(self):
        # Minimizar la ventana si "Dejar en primer plano" está desactivado
        if not self.always_on_top_var.get():
            self.root.iconify()

        # Reproducir la macro con los intervalos grabados
        while self.playing:
            for key, interval in zip(self.keys_pressed, self.times_pressed):
                if not self.playing:  # Salir del bucle si se detiene
                    break
                keyboard.press(key)
                time.sleep(interval / self.interval_factor)  # Controlar el tiempo usando el intervalo grabado ajustado por el slider
                keyboard.release(key)
                print(f"Tocado: {key}. Intervalo ajustado: {interval / self.interval_factor:.2f} seg")

            if not self.loop_var.get():
                break

        if not self.always_on_top_var.get():
            self.root.deiconify()

        self.stop_playing()  # Reset al terminar reproducción


    def start_playing(self):
        """Reproduce la macro almacenada."""
        if not self.keys_pressed:
            messagebox.showerror(message="No hay teclas o comandos que reproducir.\nError: N/A", title="Error")
            print("No hay teclas grabadas para reproducir.")
            return

        print("Reproduciendo macro...")
        self.playing = True
        self.play_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Ejecutar la reproducción en un hilo
        Thread(target=self.play_macro).start()


    def stop_playing(self):
        self.playing = False
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
    def start_playing_with_countdown(self):
        """Inicia la reproducción con una cuenta regresiva opcional."""
        # Obtener el tiempo de cuenta regresiva desde el slider
        try:
            countdown_time = int(self.countdown_slider.get())
        except:
            countdown_time = 2  # Valor por defecto si no se define el slider

        # Mostrar y realizar la cuenta regresiva
        for i in range(countdown_time, 0, -1):
            self.countdown_label.configure(text=f"Iniciando en {i}...")
            self.root.update()
            time.sleep(1)

        # Iniciar la reproducción de la macro
        self.start_playing()

    def start_playing(self):
        """Reproduce la macro almacenada."""
        if not self.keys_pressed:
            messagebox.showerror(message="No hay teclas o comandos que reproducir.\nError: N/A", title="Error")
            print("No hay teclas grabadas para reproducir.")
            return

        print("Reproduciendo macro...")
        self.playing = True
        self.play_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Ejecutar la reproducción en un hilo
        Thread(target=self.play_macro).start()                               



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
            
    def toggle_countdown_always_on_top(self):
        self.countdown_window.attributes('-topmost', self.countdown_always_on_top_var.get())

    def show_countdown_window(self):
        # Ventana de cuenta regresiva
        self.countdown_window = ctk.CTkToplevel(self.root)  # Guardar en self para acceder globalmente
        self.countdown_window.title("Cuenta Regresiva")
        
        frame = ctk.CTkFrame(master=self.countdown_window)
        frame.pack(pady=25, padx=20, fill="both", expand=True)
        
        label = ctk.CTkLabel(master=frame, text="Cuenta regresiva", font=("Arial", 15))
        label.pack(side="top", padx=10)

        # Slider vertical para la cuenta regresiva
        self.countdown_slider = ctk.CTkSlider(self.countdown_window, from_=1, to=60, number_of_steps=60, command=self.update_countdown_label, orientation="vertical", button_hover_color="green yellow")
        self.countdown_slider.set(1)
        self.countdown_slider.pack(pady=20)

        # Etiqueta para mostrar el tiempo de cuenta regresiva
        self.countdown_label = ctk.CTkLabel(self.countdown_window, text="Tiempo: 1")
        self.countdown_label.pack(pady=10)
        
        # Casilla para dejar en primer plano siempre
        self.countdown_always_on_top_var = ctk.BooleanVar()
        self.countdown_always_on_top_check = ctk.CTkCheckBox(self.countdown_window, hover_color="spring green", text="Primer plano siempre", variable=self.countdown_always_on_top_var, command=self.toggle_countdown_always_on_top)
        self.countdown_always_on_top_check.pack()

        # Botón para iniciar la reproducción
        start_button = ctk.CTkButton(self.countdown_window, text="Iniciar Reproducción", command=self.start_playing_with_countdown, hover_color="DeepSkyBlue4")
        start_button.pack(pady=10)

    def update_countdown_label(self, value):
        self.countdown_label.configure(text=f"Tiempo: {int(float(value))}s")



    def abrir_github(self):
        url = "https://www.github.com/else-wt/GSmacro"  # Coloca aquí el enlace que deseas abrir
        webbrowser.open(url)

    def show_credits(self):
        
        credits_window = ctk.CTkToplevel(self.root)
        credits_window.title("Créditos")

        credits_text = ctk.CTkTextbox(credits_window, width=330, height=236, scrollbar_button_color="green yellow")
        credits_text.pack(pady=10)
        credits_text.insert("0.0", "Desarrollado por @else_. (Discord) | else-wt (Github) \na petición de @sword0ntop.\n-------------------------------------\nTerminos de uso, tutorial, explicación de las funciones y mas en: https://github.com/else-wt/GSmacro \n-------------------------------------\nGSmacro-recorder es una app/herramienta con interfaz amigable e intuitiva para todos los usuarios. Su funcion es grabar todas las teclas que toques y luego reproducirlas según como quieras, modificando el intervalo en el que fueron reproducidas, reproduciendolas en bucle, y con muchas herramientas más.  a sido creada por una sola persona gracias a la biblioteca de python 'Customtkinter'  \n\nTe invito a hablarme por discord ante cualquier cosa. Gracias por leer ❤️‍🔥")
        credits_text.configure(state="disabled")
        boton = ctk.CTkButton(credits_window, image=self.github_icon, text="abrir pagina del proyecto.", command=self.abrir_github).pack(pady=(13, 13))
        

    def open_settings(self):
        # Crear ventana de configuración
            settings_window = ctk.CTkToplevel(self.root)
            settings_window.title("Configuración")
            settings_window.geometry("400x300")
            settings_window.transient(self.root)  # Mantener encima de la ventana principal
            settings_window.grab_set()            # Deshabilitar la ventana principal mientras está abierta

            # Crear el tabview
            tabview = ctk.CTkTabview(settings_window, width=380, height=280)
            tabview.pack(padx=10, pady=10)

            # Tab 1: Cambiar teclas de asignación para grabar y reproducir
            tab1 = tabview.add("Teclas")
            ctk.CTkLabel(tab1, text="Tecla para Grabar:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
            grabar_entry = ctk.CTkEntry(tab1, placeholder_text="Ej. F1")
            grabar_entry.grid(row=0, column=1, padx=20, pady=(20, 5))
            ctk.CTkLabel(tab1, text="Tecla para Reproducir:").grid(row=1, column=0, padx=20, pady=(5, 20), sticky="w")
            reproducir_entry = ctk.CTkEntry(tab1, placeholder_text="Ej. F6")
            reproducir_entry.grid(row=1, column=1, padx=20, pady=(5, 20))

            # Tab 2: Cambiar el fondo del programa por una imagen
            tab2 = tabview.add("Fondo")
            ctk.CTkLabel(tab2, text="Seleccionar imagen para fondo:").pack(pady=(20, 5))
            ctk.CTkButton(tab2, text="Elegir Imagen", command=self.seleccionar_imagen).pack(pady=(5, 20))

        # Tab 3: Cambiar el tema del programa
            tab3 = tabview.add("Tema")

            # Etiqueta para seleccionar el tema
            tema_label = ctk.CTkLabel(tab3, text="Selecciona el tema:")
            tema_label.pack(pady=(20, 5))

            # Función para cambiar el tema
            def cambiar_tema(tema):
                threading.Thread(target=lambda: ctk.set_appearance_mode(tema.capitalize()), daemon=True).start()
                if tema == "Light":
                    ctk.set_default_color_theme("green") 

            # Menú de opciones para cambiar el tema del programa
            tema_opcion = ctk.CTkOptionMenu(
                tab3,
                values=["Light", "Dark", "System"],
                command=cambiar_tema 
            )
            tema_opcion.pack(pady=(5, 20))
            
            self.scaling_label = ctk.CTkLabel(tab3, text="Tamaño de la interfaz:", anchor="w")
            self.scaling_optionemenu = ctk.CTkOptionMenu(tab3, values=["150", "120%", "110%", "100%", "90%", "80%", "70%", "65%", "35%" ], command=self.change_scaling_event)
            self.scaling_optionemenu.set("100%")
            self.scaling_label.pack(pady=(20,5))   
            self.scaling_optionemenu.pack(pady=(5,20))

            # Configura el tema predeterminado al iniciar
            tema_opcion.set("System")
            
    def open_comingsoon(self):
        coming_window = ctk.CTkToplevel(self.root)
        coming_window.title("Pronto!")
        coming_window.geometry("300x100")
        coming_window.transient(self.root)
        coming_window.grab_set() 
        
        frame = ctk.CTkFrame(master=coming_window)
        frame.pack(pady=25, padx=10, fill="both", expand=False)
         
        coming_label = ctk.CTkLabel(master=frame, text="Apartado de videojuegos proximamente (1.4.0)")
        coming_label.pack(pady=10)

        
            
    def open_games(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Configuración")
        settings_window.geometry("400x300")
        settings_window.transient(self.root) 
        settings_window.grab_set()  
            

    def seleccionar_imagen(self):
            archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
            if hasattr(self, archivo):
                self.bg_image_label.destroy()  # Elimina el widget anterior de la imagen

                # Cargar la nueva imagen y asignarla al fondo
                self.bg_image = ctk.CTkImage(Image.open(archivo), size=(410, 470))
                self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
                
                # Ajuste en la colocación de la imagen de fondo
                self.y.grid(row=0, column=0, rowspan=10, columnspan=10, sticky="nsew")
                
                

    def open_export_import_window(self):
        export_import_window = ctk.CTkToplevel(self.root)
        export_import_window.title("Exportar/Importar Macros")
        
        
        frame = ctk.CTkFrame(master=export_import_window)
        frame.pack(pady=1, padx=5, fill="both", expand=False)

        ctk.CTkLabel(frame, text="Exportar/Importar macros", font=("Arial", 15)).pack(pady=10)

        # Botón de Exportar
        export_button = ctk.CTkButton(export_import_window, text="Exportar Macro", image=self.save_icon, command=self.export_macro, height=39)
        export_button.pack(pady=5)

        # Botón de Importar
        import_button = ctk.CTkButton(export_import_window, text="Importar Macro", image=self.import_logo, command=self.import_macro)
        import_button.pack(pady=5)

        
    def export_macro(self):
        try:
            archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            
            # Verifica que el usuario haya seleccionado un archivo
            if archivo:
                # Guarda los datos de la macro en el archivo seleccionado
                with open(archivo, "w") as f:
                    json.dump({"keys": self.keys_pressed, "times": self.times_pressed}, f)
                print("Macro exportada correctamente.")
                messagebox.showinfo(message="Macro exportada correctamente", title="Éxito")
            else:
                print("Exportación cancelada.")
            
            
        except Exception as e: 
            print(f"Error al exportar macro: {e}")
            messagebox.showerror(message="Error al exportar la macro", title="Error al exportar macro")

    def import_macro(self):
        try:
            archivo = filedialog.askopenfilename(filetypes=[("Archivos .json", "*.json")])
            with open(archivo, "r") as f:
                data = json.load(f)
                self.keys_pressed = data["keys"]
                self.times_pressed = data["times"]
            print("Macro importada correctamente.")
            messagebox.showinfo(message="Macro importada correctamente.", title="Exito al importar macro.")

        except Exception as e:
            print(f"Error al importar macro: {e}")
            messagebox.showerror(message=f"Error al importar la macro, compruebe si hay macros existentes.\nerror 404: archivo no encontrado. {e}", title="Error al importar macro")
            
    def change_scaling_event(self, new_scaling: str):
        selected_value = self.scaling_optionemenu.get()
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        if selected_value == "70%":
            self.scaling_label.configure(text="Ventana tamaño mini:")
        elif selected_value == "80%":
            self.scaling_label.configure(text="Mira el ratoncito tan chiquito.")
        elif selected_value == "65%":
            self.scaling_label.configure(text="Ok, bastante pequeño.")
        elif selected_value == "35%":
            self.scaling_label.configure(text="¡¿Por qué tan pequeño?!")
        elif selected_value == "120%":
            self.scaling_label.configure(text="Tamaño de la interfaz: (grandota, eh)")
        else:
            self.scaling_label.configure(text="Tamaño de la interfaz:")

if __name__ == "__main__":
    app = ctk.CTk()
    my_app = MacroRecorder(app)
    app.mainloop()