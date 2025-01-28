import subprocess
import paramiko
import time

def ping_host(ip_address, count=1, timeout=1):
    """
    Ping the host to check if it is reachable.
    """
    try:
        command = ["ping", "-c", str(count), "-W", str(timeout), ip_address]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"🟢 Host {ip_address} is reachable via ping.")
            return True
        else:
            print(f"🔴 Host {ip_address} is not reachable via ping.")
            return False
    except Exception as e:
        print(f"Error pinging host {ip_address}: {e}")
        return False

def check_ssh(ip_address, username="rover2", password="rover2", port=22):
    """
    Check if the host is reachable via SSH.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password, port=port, timeout=5)
        print(f"🟢 Host {ip_address} is reachable via SSH.")
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print(f"🔴 SSH authentication failed for host {ip_address}.")
        return False
    except Exception as e:
        print(f"🔴 Error connecting to {ip_address} via SSH: {e}")
        return False

def main():
    host = "192.168.0.169"
    retry_interval_unreachable = 10  # Seconds between retries when unreachable
    retry_interval_reachable = 60  # Seconds between retries when reachable

    while True:
        print(f"Checking host {host}...")
        
        # Step 1: Check if host is reachable via ping
        reachable = ping_host(host)
        
        # Step 2: Check if host is reachable via SSH (if ping was successful)
        if reachable:
            if check_ssh(host):
                print(f"Host {host} is fully reachable. Retrying in {retry_interval_reachable} seconds.")
                time.sleep(retry_interval_reachable)
                continue
        else:
            print(f"Host {host} is not reachable. Retrying in {retry_interval_unreachable} seconds.")
        
        time.sleep(retry_interval_unreachable)

if __name__ == "__main__":
    main()