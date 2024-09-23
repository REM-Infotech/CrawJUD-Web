import os
import json
import pathlib
from dotenv import dotenv_values

from app import app
from cloudflare import run_with_cloudflared

if __name__ == "__main__":

    path_main = pathlib.Path(__file__).parent.resolve()
    values = dotenv_values()
    debug = values.get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")
    
    ## Cloudflare Tunnel Configs
    hostname = values.get("HOSTNAME")
    port = values.get("PORT", 5000)
    tunnel = values.get("TUNNEL_ID")
    credentials = json.loads(values.get("CREDENTIALS_TUNNEL"))

    ## Set credentials and config.yml path
    credentials_json = os.path.join(path_main, "credentials.json")
    config_yml = os.path.join(path_main, "config.yml")
    
    
    ## Config Content
    config_content = f"""
tunnel: {tunnel}
credentials-file: {credentials_json}

ingress:
    - hostname: {hostname}
      service: http://127.0.0.1:{port}
    - service: http_status:404
    """

    
    ## Save the configuration and credentials content into files
    with open(config_yml, 'w') as file:
        content = file.write(config_content)
        
    with open(credentials_json, "w") as f:
        f.write(json.dumps(credentials))
    
    run_with_cloudflared(app)
    
    app.run("0.0.0.0", port=int(port), debug=debug, config_path=config_yml)
