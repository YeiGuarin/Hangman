import socket
import threading
import tkinter as tk
from tkinter import messagebox


class HangmanClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.role = None
        self.current_display = []  # Almacena el estado actual de la palabra adivinada
        self.letter_labels = []  # Referencias a los labels gráficos
        self.root = tk.Tk()
        self.root.title("Juego del Ahorcado")
        self.setup_ui()
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.word_frame = tk.Frame(self.main_frame)
        self.word_frame.pack()

        self.input_label = tk.Label(self.main_frame, text="Ingresa una letra:")
        self.input_label.pack()

        self.letter_entry = tk.Entry(self.main_frame)
        self.letter_entry.pack()

        self.submit_button = tk.Button(self.main_frame, text="Enviar", command=self.send_letter)
        self.submit_button.pack(pady=10)
        self.submit_button.config(state='disabled')  # Deshabilitar hasta que sea el turno

        self.log_frame = tk.Frame(self.root)
        self.log_frame.pack(pady=20)

        self.log_text = tk.Text(self.log_frame, height=10, width=50, state='disabled')
        self.log_text.pack()

    def connect_to_server(self):
        try:
            self.conn.connect((self.host, self.port))
            self.log_message("Conectado al servidor.")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.log_message(f"Error de conexión: {e}")
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
            self.root.quit()

    def initialize_word_display(self):
        """
        Inicializa los labels para representar la palabra a adivinar.
        """
        for widget in self.word_frame.winfo_children():
            widget.destroy()

        self.letter_labels = []
        for char in self.current_display:
            label = tk.Label(self.word_frame, text=char, font=("Arial", 18), width=2)
            label.pack(side=tk.LEFT, padx=5)
            self.letter_labels.append(label)

    def update_word_display(self):
        """
        Actualiza los labels con el estado actual de la palabra adivinada.
        """
        for i, char in enumerate(self.current_display):
            self.letter_labels[i].config(text=char)

    def send_letter(self):
        """
        Envía la letra ingresada al servidor.
        """
        letter = self.letter_entry.get().strip().upper()
        self.letter_entry.delete(0, tk.END)
        if letter and len(letter) == 1 and letter.isalpha():
            self.conn.send(letter.encode())
            self.submit_button.config(state='disabled')  # Deshabilitar hasta recibir respuesta
        else:
            self.log_message("Entrada inválida. Ingresa una sola letra.")

    def log_message(self, message):
        """
        Muestra un mensaje en el área de logs de la interfaz.
        """
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def receive_messages(self):
        """
        Recibe mensajes del servidor y los procesa.
        """
        try:
            while True:
                message = self.conn.recv(1024).decode()
                if not message:  # Si no hay mensaje, la conexión se ha cerrado
                    self.log_message("El servidor ha cerrado la conexión.")
                    break

                if message.startswith("Rol:"):
                    self.role = message.split(":")[1].strip()
                    self.log_message(f"Tu rol es: {self.role}")
                    if self.role == "ADIVINADOR":
                        self.submit_button.config(state='normal')

                elif message.startswith("Palabra:"):
                    length = int(message.split(":")[1].strip())
                    self.current_display = ["_"] * length
                    self.initialize_word_display()

                elif message.startswith("Correcto:"):
                    parts = message.split(":")
                    letter = parts[1].strip()
                    indices = list(map(int, parts[2].split(",")))
                    for index in indices:
                        self.current_display[index] = letter
                    self.update_word_display()
                    self.log_message(f"¡Correcto! La letra '{letter}' está en la palabra.")
                    self.submit_button.config(state='normal')

                elif message.startswith("Incorrecto:"):
                    attempts = message.split(":")[1].strip()
                    self.log_message(f"¡Incorrecto! Intentos restantes: {attempts}")
                    self.submit_button.config(state='normal')

                elif message.startswith("Fin:"):
                    winner = message.split(":")[1].strip()
                    messagebox.showinfo("Fin del juego", f"El ganador es: {winner}")
                    self.root.quit()

                else:
                    self.log_message(message)
        except Exception as e:
            self.log_message(f"Error al recibir mensaje: {e}")
        finally:
            self.conn.close()
            self.root.quit()


if __name__ == "__main__":
    client = HangmanClient()
    client.root.mainloop()
