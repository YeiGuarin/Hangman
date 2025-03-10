import socket
import threading

class HangmanServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.scores = {1: 0, 2: 0}  # Puntos para los jugadores

    def handle_client(self, conn, addr, player_id):
        """
        Maneja la conexión con un cliente.
        """
        try:
            conn.send(f"Conectado como Jugador {player_id}\n".encode())
            self.clients.append((conn, player_id))
            print(f"Jugador {player_id} conectado desde {addr}")

            if len(self.clients) == 2:
                self.start_game()
        except Exception as e:
            print(f"Error en la conexión con el cliente {player_id}: {e}")
            conn.close()

    def start_game(self):
        """
        Inicia el juego cuando ambos jugadores están conectados.
        """
        conn1, player1 = self.clients[0]
        conn2, player2 = self.clients[1]

        # El primer jugador será el SELECTOR, el segundo será el ADIVINADOR
        threading.Thread(target=self.play_round, args=(conn1, conn2)).start()

    def play_round(self, selector, guesser):
        """
        Maneja una ronda completa del juego.
        """
        try:
            selector.send("Rol: SELECTOR\nIntroduce la palabra a adivinar:\n".encode())
            word = selector.recv(1024).decode().strip().upper()
            selector.send("Palabra registrada. Esperando al adivinador...\n".encode())

            # Ocultar la palabra al adivinador
            spaces = ['_'] * len(word)
            attempts = 3
            guessed_letters = set()

            while attempts > 0:
                current_state = ' '.join(spaces)
                guesser.send(f"Palabra: {current_state}\n".encode())
                guesser.send(f"Intentos restantes: {attempts}\n".encode())
                guesser.send("Introduce una letra:\n".encode())
                letter = guesser.recv(1024).decode().strip().upper()

                if len(letter) != 1 or not letter.isalpha():
                    guesser.send("Entrada inválida. Ingresa solo una letra.\n".encode())
                    continue

                if letter in guessed_letters:
                    guesser.send("Ya intentaste esa letra.\n".encode())
                    continue

                guessed_letters.add(letter)

                if letter in word:
                    indices = [i for i, char in enumerate(word) if char == letter]
                    for i in indices:
                        spaces[i] = letter
                    guesser.send(f"¡Correcto! La letra '{letter}' está en la palabra.\n".encode())

                    if ''.join(spaces) == word:
                        guesser.send(f"¡Ganaste! La palabra era: {word}\n".encode())
                        self.scores[2] += 1
                        return
                else:
                    attempts -= 1
                    guesser.send(f"Incorrecto. Te quedan {attempts} intentos.\n".encode())

            # Si se acaban los intentos
            guesser.send(f"¡Perdiste! La palabra era: {word}\n".encode())
            self.scores[1] += 1
        except Exception as e:
            print(f"Error durante la ronda: {e}")
        finally:
            self.end_game()

    def end_game(self):
        """
        Finaliza el juego y envía los resultados a los jugadores.
        """
        conn1, player1 = self.clients[0]
        conn2, player2 = self.clients[1]
        winner = max(self.scores, key=self.scores.get)
        conn1.send(f"Fin del juego. Ganador: Jugador {winner} con {self.scores[winner]} puntos.\n".encode())
        conn2.send(f"Fin del juego. Ganador: Jugador {winner} con {self.scores[winner]} puntos.\n".encode())
        conn1.close()
        conn2.close()
        self.clients = []  # Reiniciar la lista de clientes para permitir nuevos jugadores

    def run(self):
        """
        Ejecuta el servidor.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(2)
        print("Servidor listo y esperando jugadores...")
        player_id = 1
        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr, player_id)).start()
            player_id += 1


if __name__ == "__main__":
    server = HangmanServer()
    server.run()
