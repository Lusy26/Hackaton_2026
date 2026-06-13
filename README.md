# Hackaton_2026

## Descripción

Este proyecto es un juego de laberinto cooperativo que se inicia desde dos ordenadores diferentes:
- `computer1.py`: servidor de chat y lanzador del juego `main1.py`.
- `computer2.py`: cliente de chat y lanzador del juego `main2.py`.

Ambos ordenadores deben acordar un `seed` antes de iniciar el laberinto. El valor del seed controla la generación del mismo laberinto en ambos equipos.

## Cómo usar

1. En el primer ordenador, ejecuta `computer1.py`.
   - Espera a que el cliente se conecte.
   - El programa muestra la IP local del ordenador para que pueda ser usada por el segundo ordenador.

2. En el segundo ordenador, ejecuta `computer2.py`.
   - Introduce la IP del ordenador 1 en el campo "IP ordenador 1:".
   - Pulsa el botón `Conectar`.
   - Si la conexión automática funciona, se intentará conectar sin introducir IP.

3. Negocia el `seed` en el chat:
   - En cualquiera de los dos ordenadores puedes escribir `/seed <valor>` para proponer un seed.
   - El otro ordenador puede responder con `/agree` para aceptar la propuesta.
   - También se puede iniciar directamente con `/start <valor>` si ambos están de acuerdo.

4. Una vez acordado el seed, el juego arranca automáticamente con el mismo laberinto en ambos equipos.

## Comandos de chat

- `/seed <valor>`: propone un seed para el laberinto.
- `/agree`: acepta la propuesta de seed recibida y arranca el juego.
- `/start <valor>`: arranca el juego inmediatamente con el seed indicado.

## Notas importantes

- El laberinto se genera con la misma lógica en `main1.py` y `main2.py` usando el mismo seed.
- Si no se puede detectar la IP local, el programa recomienda usar `ipconfig` en CMD.
- El juego se ejecuta en una ventana de Pygame que muestra el laberinto y el jugador.
