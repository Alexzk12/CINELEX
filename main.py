import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import serial
import serial.tools.list_ports

class CINELEX:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("CINELEX")
        self.ventana.geometry("500x400")
        self.ventana.resizable(True, True)
        self.ventana.configure(background='#7c1324')
        self.personas_restantes = 15
        self.cajas_disponibles = [True, True, True, True]

        self.label_estado = tk.Label(ventana, text="PERSONAS POR ATENDER: 15", font=("Arial", 14))
        self.label_estado.pack(pady=10)

        self.barra = ttk.Progressbar(ventana, length=300, maximum=15)
        self.barra.pack(pady=10)

        self.boton_inicio = tk.Button(ventana, text="Empezar a atender", command=self.iniciar_simulacion)
        self.boton_inicio.pack(pady=10)


        self.texto_log = tk.Text(ventana, height=10, width=60)
        self.texto_log.pack(pady=10)
        self.texto_log.insert(tk.END, "Esperando inicio...\n")
        self.texto_log.config(state=tk.DISABLED)
        self.serial_port = self.conectar_esp32()

    def conectar_esp32(self):
        puertos = serial.tools.list_ports.comports()
        for puerto in puertos:
            try:
                s = serial.Serial(puerto.device, 115200, timeout=1)
                print(f"Conectado a {puerto.device}")
                return s
            except:
                continue
        print("No se encontró ESP32.")
        return None

    def iniciar_simulacion(self):
        if not self.serial_port or not self.serial_port.is_open:
            return
        self.boton_inicio.config(state="disabled")
        threading.Thread(target=self.simular_fila, daemon=True).start()

    def simular_fila(self):
        while self.personas_restantes > 0:
            for i in range(4):
                if self.cajas_disponibles[i] and self.personas_restantes > 0:
                    self.cajas_disponibles[i] = False
                    threading.Thread(target=self.atender_persona, args=(i,), daemon=True).start()
                    self.personas_restantes -= 1
                    self.actualizar_interfaz()
            time.sleep(0.2)
    def atender_persona(self, caja_id):
        tiempo = random.randint(5, 10)  
        self.log(f"Caja {caja_id} atendiendo por {tiempo} segundos...")
        self.serial_port.write(f"{caja_id}:1\n".encode())
        time.sleep(tiempo)
        self.serial_port.write(f"{caja_id}:0\n".encode())
        self.log(f"Caja {caja_id} libre (persona atendida en {tiempo} segundos).")
        self.cajas_disponibles[caja_id] = True
        self.barra["value"] += 1
        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        self.label_estado.config(text=f"Personas por atender: {self.personas_restantes}")
        self.ventana.update_idletasks()

    def log(self, mensaje):
        self.texto_log.config(state=tk.NORMAL)
        self.texto_log.insert(tk.END, mensaje + "\n")
        self.texto_log.see(tk.END)
        self.texto_log.config(state=tk.DISABLED)
ventana = tk.Tk()
app = CINELEX(ventana)
ventana.mainloop()
