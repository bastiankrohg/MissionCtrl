import socket
import threading
from queue import Queue

# Configuration for TCP communication
TCP_IP = "127.0.0.1"  # Replace with the Coral board's IP if needed
TCP_PORT = 50055

# Shared queue for telemetry data
telemetry_queue = Queue()

def start_tcp_listener():
    """Start a TCP listener for incoming telemetry messages."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((TCP_IP, TCP_PORT))
        server_socket.listen(1)
        print(f"TCP server listening on {TCP_IP}:{TCP_PORT}")

        conn, addr = server_socket.accept()  # Accept a single connection
        print(f"Connection established with {addr}")

        with conn:
            while True:
                try:
                    data = conn.recv(1024)  # Adjust buffer size as needed
                    if not data:
                        break  # Client disconnected
                    telemetry_data = data.decode("utf-8")
                    telemetry_queue.put(telemetry_data)  # Add to the queue
                    print(f"Received telemetry: {telemetry_data}")
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break
        print("Connection closed.")