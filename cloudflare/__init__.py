import atexit
import requests
import subprocess
import tarfile
import tempfile
import shutil
import os
import platform
import time
import re
import json
from random import randint
from threading import Timer
from pathlib import Path

CLOUDFLARED_CONFIG = {
    ('Windows', 'AMD64'): {
        'command': 'cloudflared-windows-amd64.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
    },
    ('Windows', 'x86'): {
        'command': 'cloudflared-windows-386.exe',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe'
    },
    ('Linux', 'x86_64'): {
        'command': 'cloudflared-linux-amd64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
    },
    ('Linux', 'i386'): {
        'command': 'cloudflared-linux-386',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386'
    },
    ('Linux', 'arm'): {
        'command': 'cloudflared-linux-arm',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm'
    },
    ('Linux', 'arm64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Linux', 'aarch64'): {
        'command': 'cloudflared-linux-arm64',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64'
    },
    ('Darwin', 'x86_64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    },
    ('Darwin', 'arm64'): {
        'command': 'cloudflared',
        'url': 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz'
    }
}

def _get_command(system, machine):
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['command']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")

def _get_url(system, machine):
    try:
        return CLOUDFLARED_CONFIG[(system, machine)]['url']
    except KeyError:
        raise Exception(f"{machine} is not supported on {system}")


def _download_cloudflared(cloudflared_path, command):
    system, machine = platform.system(), platform.machine()
    if Path(cloudflared_path, command).exists():
        executable = (cloudflared_path+'/'+'cloudflared') if (system == "Darwin" and machine in ["x86_64", "arm64"]) else (cloudflared_path+'/'+command)
        update_cloudflared = subprocess.Popen([executable, 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return
    print(f" * Downloading cloudflared for {system} {machine}...")
    url = _get_url(system, machine)
    _download_file(url)

def _download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    download_path = str(Path(tempfile.gettempdir(), local_filename))
    with open(download_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return download_path

def _run_cloudflared(port, metrics_port, tunnel_id=None, config_path=None):
    system, machine = platform.system(), platform.machine()
    command = _get_command(system, machine)
    cloudflared_path = str(Path(tempfile.gettempdir()))
    
    _download_cloudflared(cloudflared_path, command)
    
    executable = str(Path(cloudflared_path, command))

    cloudflared_command = [executable, 'tunnel', '--metrics', f'127.0.0.1:{metrics_port}']
    if config_path:
        cloudflared_command += ['--config', config_path, 'run']
    elif tunnel_id:
        cloudflared_command += ['--url', f'http://127.0.0.1:{port}', 'run', tunnel_id]
    else:
        cloudflared_command += ['--url', f'http://127.0.0.1:{port}']

    cloudflared = subprocess.Popen(cloudflared_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    atexit.register(cloudflared.terminate)
    localhost_url = f"http://127.0.0.1:{metrics_port}/metrics"

    for _ in range(10):
        try:
            metrics = requests.get(localhost_url).text
            if tunnel_id or config_path:
                # If tunnel_id or config_path is provided, we check for cloudflared_tunnel_ha_connections, as no tunnel URL is available in the metrics
                if re.search(r"cloudflared_tunnel_ha_connections\s\d", metrics):
                    # No tunnel URL is available in the metrics, so we return a generic text
                    tunnel_url = "preconfigured tunnel URL" 
                    break
            if not tunnel_id or not config_path:
                # If neither tunnel_id nor config_path is provided, we check for the tunnel URL in the metrics
                tunnel_url = (re.search(r"(?P<url>https?:\/\/[^\s]+.trycloudflare.com)", metrics).group("url"))
                break
        except:
            time.sleep(3)
    else:
        raise Exception(f"! Can't connect to Cloudflare Edge")

    return tunnel_url, executable

def start_cloudflared(port, metrics_port, tunnel_id=None, config_path=None):
    cloudflared_address, executable = _run_cloudflared(port, metrics_port, tunnel_id, config_path)
    file_name = os.path.basename(config_path)
    home_Path = os.path.join(Path.home().__str__(), ".cloudflared", file_name)
    
    if platform.system() == "Linux":
        shutil.copy(config_path, home_Path)
        install_command = subprocess.Popen([executable, "service", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = install_command.communicate()
        print(f" * {stderr.decode()}")
        print(f" * {stdout.decode()}")
        atexit.register(uninstall_service, home_Path, executable)
    
    print(f" * Running on {cloudflared_address}")
    print(f" * Traffic stats available on http://127.0.0.1:{metrics_port}/metrics")

    
def run_with_cloudflared(app):
    old_run = app.run

    def new_run(*args, **kwargs):
        port = kwargs.pop('port', 5000)
        metrics_port = kwargs.pop('metrics_port', randint(8100, 9000))
        tunnel_id = kwargs.pop('tunnel_id', None)
        config_path = kwargs.pop('config_path', None)

        # Starting the Cloudflared tunnel in a separate thread.
        tunnel_args = (port, metrics_port, tunnel_id, config_path)
        thread = Timer(2, start_cloudflared, args=tunnel_args)
        thread.daemon = True
        thread.start()

        # Running the Flask app.
        old_run(*args, **kwargs)

    app.run = new_run
    
# Função que executa o comando de uninstall
def uninstall_service(file_remove: str, executable: str):
    uninstall_command = subprocess.run([executable, "service", "uninstall"],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    # Verifica o resultado do comando
    if uninstall_command.returncode == 0:
        print("Serviço desinstalado com sucesso.")
    else:
        print("Erro ao desinstalar o serviço:", uninstall_command.stderr.decode())
    
    try:
        os.remove(file_remove)
    except FileNotFoundError:
        print(f"O arquivo {file_remove} não foi encontrado.")

