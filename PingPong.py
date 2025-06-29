# Creación del juego arcade Pong
from tkinter import *
import turtle
import time
import pygame
from tkinter import messagebox

# Función para iniciar el juego y configurar el entorno principal
def Comenzar_juego():
    """
    Configura el entorno principal del juego utilizando Turtle,
    crea los elementos necesarios (raquetas, pelota, marcador),
    maneja eventos de teclado y controla el bucle principal del juego.
    """
    # Configuración de la ventana del juego con Turtle
    root = turtle.Screen()
    root.title("Arcade Pong de Matus")
    root.bgcolor("black")
    root.setup(width=800, height=600)
    root.tracer(0)  # Desactiva la actualización automática de la ventana para mayor fluidez

    # Línea central discontinua
    linea_centro = turtle.Turtle()
    linea_centro.color("White")
    linea_centro.penup()  # Levanta el lápiz para no dibujar al moverse
    linea_centro.goto(0, 300)  # Posición inicial
    linea_centro.setheading(270)  # Apunta hacia abajo
    linea_centro.pensize(2)
    # Dibujar segmentos de línea discontinua
    for _ in range(15):
        linea_centro.pendown()  # Baja el lápiz para dibujar
        linea_centro.forward(20)
        linea_centro.penup()  # Levanta el lápiz para dejar espacio
        linea_centro.forward(20)
    linea_centro.hideturtle()  # Oculta la "tortuga"

    # Creación de las raquetas (izquierda y derecha)
    # Raqueta izquierda
    raqueta_izq = turtle.Turtle()
    raqueta_izq.speed(0)  # Sin animación
    raqueta_izq.shape("square")
    raqueta_izq.shapesize(stretch_wid=6, stretch_len=1)  # Tamaño personalizado
    raqueta_izq.color("blue")
    raqueta_izq.penup()
    raqueta_izq.goto(-350, 0)  # Posición inicial

    # Raqueta derecha
    raqueta_drch = turtle.Turtle()
    raqueta_drch.speed(0)
    raqueta_drch.shape("square")
    raqueta_drch.shapesize(stretch_wid=6, stretch_len=1)
    raqueta_drch.color("green")
    raqueta_drch.penup()
    raqueta_drch.goto(350, 0)

    # Creación de la pelota
    pelota = turtle.Turtle()
    pelota.speed(0)
    pelota.shape("circle")
    pelota.color("white")
    pelota.penup()
    pelota.goto(0, 0)  # Centro inicial

    # Inicialización de sonidos (Pygame)
    pygame.mixer.init()
    sonido_rebote = pygame.mixer.Sound("rebote.mp3")
    sonido_punto = pygame.mixer.Sound("punto.mp3")

    # Marcador inicial
    marcador = turtle.Turtle()
    marcador.speed(0)
    marcador.shape("square")
    marcador.color("white")
    marcador.penup()
    marcador.hideturtle()
    marcador.goto(-15, 250)
    marcador.write("Jugador Izquierda: 0  Jugador Derecha: 0", align="center", font=("Courier", 20, "normal"))

    # Variables para los puntos
    puntos_derecha = 0
    puntos_izquierda = 0

    # Función para actualizar el marcador
    def Actualizar_marcador():
        """
        Limpia y actualiza el marcador en pantalla con los puntos actuales de ambos jugadores.
        """
        marcador.clear()
        marcador.write(f"Jugador Izquierda: {puntos_izquierda}  Jugador Derecha: {puntos_derecha}",
                       align="center", font=("Courier", 20, "normal"))

    # Velocidad inicial de la pelota
    pelota_dx = 3  # Movimiento horizontal
    pelota_dy = 3  # Movimiento vertical

    # Manejo de las teclas presionadas (para resolver problemas de movimientos simultáneos)
    teclas_presionadas = {
        "w": False,  # Arriba raqueta izquierda
        "s": False,  # Abajo raqueta izquierda
        "Up": False,  # Arriba raqueta derecha
        "Down": False  # Abajo raqueta derecha
    }

    def Tecla_presionada(tecla):
        """
        Marca una tecla como presionada en el diccionario.
        """
        teclas_presionadas[tecla] = True

    def Tecla_suelta(tecla):
        """
        Marca una tecla como soltada en el diccionario.
        """
        teclas_presionadas[tecla] = False

    # Asignar controles a las raquetas
    root.onkeypress(lambda: Tecla_presionada("w"), "w")
    root.onkeypress(lambda: Tecla_presionada("s"), "s")
    root.onkeyrelease(lambda: Tecla_suelta("w"), "w")
    root.onkeyrelease(lambda: Tecla_suelta("s"), "s")
    root.onkeypress(lambda: Tecla_presionada("Up"), "Up")
    root.onkeypress(lambda: Tecla_presionada("Down"), "Down")
    root.onkeyrelease(lambda: Tecla_suelta("Up"), "Up")
    root.onkeyrelease(lambda: Tecla_suelta("Down"), "Down")

    root.listen()  # Escuchar eventos del teclado

    # Bucle principal del juego
    while True:
        # Movimiento de las raquetas según las teclas presionadas
        if teclas_presionadas["w"] and raqueta_izq.ycor() < 250:
            raqueta_izq.sety(raqueta_izq.ycor() + 20)
        if teclas_presionadas["s"] and raqueta_izq.ycor() > -250:
            raqueta_izq.sety(raqueta_izq.ycor() - 20)
        if teclas_presionadas["Up"] and raqueta_drch.ycor() < 250:
            raqueta_drch.sety(raqueta_drch.ycor() + 20)
        if teclas_presionadas["Down"] and raqueta_drch.ycor() > -250:
            raqueta_drch.sety(raqueta_drch.ycor() - 20)

        # Movimiento de la pelota
        pelota.setx(pelota.xcor() + pelota_dx)
        pelota.sety(pelota.ycor() + pelota_dy)

        # Rebotes en los bordes superiores e inferiores
        if pelota.ycor() > 290:
            pelota.sety(290)
            pelota_dy *= -1
        if pelota.ycor() < -290:
            pelota.sety(-290)
            pelota_dy *= -1

        # Rebotes en las raquetas
        if (340 < pelota.xcor() < 350) and (raqueta_drch.ycor() - 50 < pelota.ycor() < raqueta_drch.ycor() + 50):
            pelota.setx(340)
            pelota_dx *= -1.5
            pelota_dy *= 1.5
            pygame.mixer.Sound.play(sonido_rebote)
        if (-350 < pelota.xcor() < -340) and (raqueta_izq.ycor() - 50 < pelota.ycor() < raqueta_izq.ycor() + 50):
            pelota.setx(-340)
            pelota_dx *= -1.5
            pelota_dy *= 1.5
            pygame.mixer.Sound.play(sonido_rebote)

        # Comprobación de goles
        if pelota.xcor() > 390:
            puntos_izquierda += 1
            Actualizar_marcador()
            pelota.goto(0, 0)
            pelota_dx, pelota_dy = 2, 2
        if pelota.xcor() < -390:
            puntos_derecha += 1
            Actualizar_marcador()
            pelota.goto(0, 0)
            pelota_dx, pelota_dy = -2, 2

        root.update()
        time.sleep(0.02)


def Cuenta_atras():
    """
    Realiza una cuenta regresiva visual desde 3 hasta 1
    y luego muestra un mensaje de inicio. Utiliza Turtle
    para mostrar los números en el centro de la pantalla.
    """
    contador = turtle.Turtle()
    contador.color("white")
    contador.hideturtle()
    contador.penup()
    contador.goto(0,0) # Centramos la cuenta atras 
    for i in range(4, 0, -1): # Cuenta atras desde 3
        contador.clear() # Limpiamos el contador 
        contador.write(i, align="center", font=("Courier", 48, "bold"))
        time.sleep(1) # Mostramos por un segundo el numero correspondiente 
    contador.clear()
    contador.write("¡Comienza!", align="center", font=("Courier", 36, "bold"))
    time.sleep(1)  # Mostramos por un segundo el cartel de comienzo 
    contador.clear()

def Jugar():
    """
    Destruye la pantalla inicial del menú y lanza
    la cuenta regresiva antes de iniciar el juego.
    """
    pantalla_inicial.destroy()
    Cuenta_atras()
    Comenzar_juego()

def Normas():
    """
    Muestra las normas del juego en una ventana emergente utilizando tkinter.
    """
    normas = """Reglas del juego:
1. Usa 'W' y 'S' para mover la raqueta izquierda.
2. Usa 'Arriba' y 'Abajo' para mover la raqueta derecha.
3. Anotas un punto cuando la pelota cruza el lado contrario.
4. El primer jugador en llegar a 5 puntos gana.
5. El punto 4 es mentira, aun no se hacer eso, me dan errores y no se como hacer que no se buguee"""
    from tkinter import messagebox
    messagebox.showinfo("Normas del juego", normas)
    
def Salir():
    """
    Cierra la pantalla inicial y finaliza el programa.
    """
    pantalla_inicial.destroy()
    exit()

#Pantall inicial 
pantalla_inicial= Tk()
pantalla_inicial.title("Menu primcipal")
pantalla_inicial.geometry("400x300")
pantalla_inicial.configure(bg= "black")

#Texto principal 
Label(pantalla_inicial, text="PONG DE MATUS.", font=("Courier", 24), bg= "black", fg="white").pack(pady=20)

#Los botones con las tres opciones que tenemos 
Button(pantalla_inicial, text="JUGAR", font=("Courier", 16), bg= "black", fg="white", command= Jugar).pack(pady=20)
Button(pantalla_inicial, text="NORMAS", font=("Courier", 16), bg= "black", fg="white", command= Normas).pack(pady=20)
Button(pantalla_inicial, text="SALIR", font=("Courier", 16), bg= "black", fg="white", command= Salir).pack(pady=20)

#Mostrar pantalla inicial 
pantalla_inicial.mainloop()


#GAna el jugador que llegue a 5 puntos o eso queria pero no me sale 
# el tema de reiniciar me va fatal.