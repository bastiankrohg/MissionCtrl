import socket
import threading
from queue import Queue

# Configuration for TCP communication (Coral board → Mission Control)
TCP_IP = "127.0.0.1"  # Replace with the Coral board's IP if needed
TCP_PORT = 60066

# Configuration for local UDP retransmission (Mission Control → Dashboard/Local services)
LOCAL_UDP_IP = "127.0.0.1"
LOCAL_UDP_PORT = 60000

# Shared queue for telemetry data
telemetry_queue = Queue()

def retransmit_to_local_udp(data):
    """Retransmit data to the local UDP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        try:
            udp_socket.sendto(data.encode("utf-8"), (LOCAL_UDP_IP, LOCAL_UDP_PORT))
            print(f"Retransmitted data to {LOCAL_UDP_IP}:{LOCAL_UDP_PORT}")
        except Exception as e:
            print(f"Error retransmitting data: {e}")

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

                    # Retransmit data to local UDP
                    retransmit_to_local_udp(telemetry_data)

                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break
        print("Connection closed.")