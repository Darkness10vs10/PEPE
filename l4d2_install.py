import os
import requests
import time



# Función para ejecutar comandos en la terminal
def run_command(command):
    print(f"Ejecutando: {command}")
    os.system(command)
    time.sleep(2)

# 1. Preparar el Sistema
def prepare_system():
    print("Preparando el sistema para L4D2...")
    run_command("dpkg --add-architecture i386")  # Habilitar soporte para 32-bit
    run_command("apt-get update && apt-get upgrade -y")  # Actualizar el sistema
    run_command("apt-get install libc6:i386 lib32z1 screen -y")  # Instalar dependencias necesarias

# 2. Crear el Usuario 'steam'
def create_user():
    print("Creando el usuario 'steam'...")
    run_command("adduser --disabled-password --gecos '' steam")  # Crear el usuario sin contraseña
    run_command("adduser steam sudo")  # Dar permisos de sudo al usuario
    run_command("su - steam")  # Iniciar sesión como el usuario 'steam'

# 3. Instalar SteamCMD y el Servidor L4D2
def install_steamcmd_and_l4d2():
    print("Instalando SteamCMD...")

    # Descargar SteamCMD
    run_command("wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz")
    # Extraer SteamCMD
    run_command("tar -xvzf steamcmd_linux.tar.gz")

    print("Instalando L4D2 usando SteamCMD...")
    
    # Usamos echo y un heredoc para enviar comandos a steamcmd automáticamente
    run_command('echo "login anonymous" | ./steamcmd.sh')
    run_command('echo "force_install_dir ./Steam/steamapps/common/l4d2" | ./steamcmd.sh')
    run_command('echo "app_update 222860 validate" | ./steamcmd.sh')
    run_command('echo "quit" | ./steamcmd.sh')

# 4. Configurar Archivos del Servidor
def configure_server():
    print("Configurando el servidor L4D2...")

    # Crear archivos de configuración necesarios
    server_cfg = """
    // Configuración básica del servidor L4D2
    hostname "Mi Servidor L4D2"
    rcon_password "mi_contraseña_rcon"
    sv_password "contraseña_del_servidor"
    sv_lan 0
    """

    # Guardar archivo de configuración del servidor
    with open("/home/steam/Steam/steamapps/common/l4d2/left4dead2/cfg/server.cfg", "w") as f:
        f.write(server_cfg)

    # Crear archivo de inicio del servidor
    start_script = """#!/bin/bash
    cd /home/steam/Steam/steamapps/common/l4d2
    ./srcds_run -game left4dead2 +map c1m1_hotel -maxplayers 8 -autoupdate
    """

    # Guardar archivo de inicio
    with open("/home/steam/start_l4d2.sh", "w") as f:
        f.write(start_script)

    # Dar permisos de ejecución al archivo de inicio
    run_command("chmod +x /home/steam/start_l4d2.sh")

# 5. Ejecutar el Servidor
def start_server():
    print("Iniciando el servidor L4D2...")
    run_command("screen -dmS l4d2_server /home/steam/start_l4d2.sh")  # Ejecutar el servidor en una nueva pantalla

# Función principal que ejecuta todo el proceso
def main():
    print("Comenzando la instalación de L4D2 en el servidor Linux...")
    prepare_system()  # Paso 1: Preparar el sistema
    create_user()  # Paso 2: Crear el usuario 'steam'
    install_steamcmd_and_l4d2()  # Paso 3: Instalar SteamCMD y L4D2
    configure_server()  # Paso 4: Configurar el servidor
    start_server()  # Paso 5: Iniciar el servidor L4D2

    print("¡Instalación y configuración completas! El servidor L4D2 está en funcionamiento.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()

