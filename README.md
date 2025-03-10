# Juego del Ahorcado - Cliente

Este es un cliente para el juego del ahorcado implementado en Python. Utiliza `socket` para la comunicación con un servidor y `tkinter` para la interfaz gráfica.

## Requisitos

Asegúrate de tener Python 3 instalado en tu sistema. También necesitas las siguientes bibliotecas (incluidas en la instalación estándar de Python):

- `socket`
- `threading`
- `tkinter`

## Instalación

1. Clona este repositorio o descarga el archivo `client.py`.
2. Asegúrate de tener el servidor del juego ejecutándose en la misma red o en `localhost`.
3. Ejecuta el cliente con el siguiente comando:

   ```bash
   python client.py
   ```

## Uso

1. Al iniciar el cliente, este intentará conectarse al servidor en `localhost` y puerto `12345`.
2. Una vez conectado, recibirás tu rol dentro del juego (ADIVINADOR).
3. Si eres el adivinador, ingresa una letra en el cuadro de texto y presiona "Enviar".
4. El cliente mostrará los aciertos y errores, actualizando la palabra en pantalla.
5. Cuando el juego termine, se mostrará un mensaje con el ganador y el programa se cerrará automáticamente.

## Notas

- Asegúrate de que el servidor esté activo antes de ejecutar el cliente.
- Si la conexión falla, verifica la dirección IP y el puerto configurados en el código.

## Autor

Desarrollado por Yeimy Juliana Guarin

