import PySIP
import pyaudio
import tkinter as tk

# Configuraciones básicas (ajusta según tu entorno)
SIP_SERVER = "172.28.96.240"
SIP_USER = "Lab02py"
SIP_PASSWORD = "sseguro"

# Crear un usuario SIP
user = PySIP.User(f"sip:{SIP_USER}@{SIP_SERVER}", SIP_PASSWORD)

# Crear un agente SIP
agent = PySIP.UA(user)

# Registrar el agente en el servidor
agent.register()

# Variable global para almacenar la llamada activa
current_call = None

# Configuración de PyAudio (se realiza una sola vez)
p = pyaudio.PyAudio()

def audio_callback(in_data, frame_count, time_info, status):
    """Callback para manejar la transmisión y recepción de audio."""
    global current_call

    # Enviamos los datos de audio al otro extremo
    current_call.write(in_data)

    # Leemos los datos de audio del otro extremo
    out_data = current_call.read(frame_count)

    return (out_data, pyaudio.paContinue)

def on_incoming_call(call):
    global current_call
    print("Llamada entrante de", call.remote_uri)
    call.accept()

    # Configuramos el stream de audio (se hace por cada llamada)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    frames_per_buffer=1024,
                    output=True,
                    input=True)

    # Iniciamos la sesión de audio
    call.audio_factory = PySIP.AudioFactory()
    call.audio_factory.set_audio_callback(audio_callback)
    call.audio_factory.start()

    current_call = call

    # Esperamos a que la llamada termine
    while current_call.state == PySIP.CallState.InProgress:
        # Aquí puedes agregar lógica adicional, como mostrar el estado de la llamada
        pass

    # Detenemos la sesión de audio
    call.audio_factory.stop()
    stream.stop_stream()
    stream.close()
    current_call = None
    print("Llamada finalizada")

def make_call(extension):
    global current_call
    if current_call:
        print("Ya hay una llamada en curso")
        return

    call = agent.make_call(f"sip:{extension}@{SIP_SERVER}")
    current_call = call

    # Configuramos el stream de audio (se hace por cada llamada)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    frames_per_buffer=1024,
                    output=True,
                    input=True)

    # Iniciamos la sesión de audio
    call.audio_factory = PySIP.AudioFactory()
    call.audio_factory.set_audio_callback(audio_callback)
    call.audio_factory.start()

    # Esperamos a que la llamada termine
    while current_call.state == PySIP.CallState.InProgress:
        # Aquí puedes agregar lógica adicional, como mostrar el estado de la llamada
        pass

    # Detenemos la sesión de audio
    call.audio_factory.stop()
    stream.stop_stream()
    stream.close()
    current_call = None
    print("Llamada finalizada")

def hangup_call():
    global current_call
    if current_call:
        current_call.terminate()
        current_call = None
        print("Llamada colgada")
    else:
        print("No hay ninguna llamada activa")

# Interfaz gráfica simple
root = tk.Tk()
entry = tk.Entry(root)
call_button = tk.Button(root, text="Llamar", command=lambda: make_call(entry.get()))
hangup_button = tk.Button(root, text="Colgar", command=hangup_call)
# ... (configurar la interfaz)
root.mainloop()

agent.on_new_call = on_incoming_call
agent.run()
