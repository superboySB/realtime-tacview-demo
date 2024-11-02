import socket
import random
import time
import json

# Tacview telemetry connection information
HOST = 'localhost'  # The address from Tacview telemetry UI
PORT = 5555         # The port from Tacview telemetry UI

# Connect to Tacview telemetry server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("Waiting for Tacview client to connect...")
connection, client_address = sock.accept()
print(f"Tacview client connected: {client_address}")

# Handshake with Tacview client
try:
    handshake_data = "XtraLib.Stream.0\nTacview.RealTimeTelemetry.0\nHost username\n\0"
    connection.sendall(handshake_data.encode('utf-8'))
    client_handshake = connection.recv(1024).decode('utf-8')
    if not client_handshake.startswith("XtraLib.Stream.0"):
        raise ConnectionAbortedError("Handshake failed. Incorrect protocol.")
    print("Handshake successful.")
except Exception as e:
    print(f"Handshake error: {e}")
    connection.close()
    sock.close()
    exit()

# Send ACMI header
header = (
    "FileType=text/acmi/tacview\n"
    "FileVersion=2.2\n"
    "0,ReferenceTime=2017-05-01T05:27:00Z\n"
    "0,RecordingTime=2017-03-09T16:17:49Z\n"
    "0,Title=test simple aircraft\n"
    "0,DataRecorder=DCS2ACMI 1.6.0\n"
    "0,DataSource=DCS 1.5.6.1938\n"
    "0,Author=AuthorName\n"
    "0,ReferenceLongitude=37\n"
    "0,ReferenceLatitude=37\n"
)
connection.sendall(header.encode('utf-8'))

# Function to send telemetry data to Tacview

def send_telemetry_data(frame, aircraft_id, lon, lat, alt, roll, pitch, yaw, name, color):
    try:
        # Format telemetry data according to Tacview ACMI format based on provided example
        data = (
            f"#{frame:.2f}\n"
            f"{aircraft_id},T={lon:.4f}|{lat:.4f}|{alt:.2f}|{roll:.6f}|{pitch:.6f}|{yaw:.1f},Name={name},Color={color}\n"
        )
        connection.sendall(data.encode('utf-8'))
    except (ConnectionAbortedError, BrokenPipeError) as e:
        print(f"Connection lost. Stopping telemetry. Error: {e}")
        raise KeyboardInterrupt

# Define initial positions for red and blue aircrafts
red_aircraft = {'aircraft_id': 'A0100', 'lat': 25.5, 'lon': 123.4, 'alt': 5006.26, 'roll': 0.0, 'pitch': -0.3, 'yaw': 360.0, 'name': 'F16', 'color': 'Red'}
blue_aircraft = {'aircraft_id': 'B0100', 'lat': 26.3993, 'lon': 123.4, 'alt': 5966.52, 'roll': 0.0, 'pitch': -0.2, 'yaw': 180.0, 'name': 'F16', 'color': 'Blue'}

frame = 0.0

try:
    while True:
        # Increment frame
        frame += 1.0

        # Change the position and orientation of red aircraft more significantly
        red_aircraft['lat'] += random.uniform(-0.01, 0.01)
        red_aircraft['lon'] += random.uniform(-0.01, 0.01)
        red_aircraft['alt'] += random.uniform(-50, 50)
        red_aircraft['roll'] += random.uniform(-5, 5)
        red_aircraft['pitch'] += random.uniform(-5, 5)
        red_aircraft['yaw'] += random.uniform(-30, 30)

        # Change the position and orientation of blue aircraft more significantly
        blue_aircraft['lat'] += random.uniform(-0.01, 0.01)
        blue_aircraft['lon'] += random.uniform(-0.01, 0.01)
        blue_aircraft['alt'] += random.uniform(-50, 50)
        blue_aircraft['roll'] += random.uniform(-5, 5)
        blue_aircraft['pitch'] += random.uniform(-5, 5)
        blue_aircraft['yaw'] += random.uniform(-30, 30)

        # Send telemetry data to Tacview
        send_telemetry_data(frame, **red_aircraft)
        send_telemetry_data(frame, **blue_aircraft)

        # Wait before sending the next update
        time.sleep(1.0)

except KeyboardInterrupt:
    print("Telemetry streaming stopped.")
    connection.close()
    sock.close()