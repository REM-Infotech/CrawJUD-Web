import os
import json



def csp() -> dict[str]:
    
    from app.models import Servers
    srvs = Servers.query.all()
    csp_vars = {
    'default-src': [
        '\'self\''
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        'https://code.jquery.com',
        'https://use.fontawesome.com',
        '',
        '\'unsafe-inline\'',
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        'https://github.com',
        'https://avatars.githubusercontent.com',
        '\'unsafe-inline\'',
    ],
    'img-src': [
        '\'self\'',
        'data:',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://unpkg.com',
        'https://cdn-icons-png.flaticon.com',
        'https://github.com',
        'https://domain.cliente.com',
        'https://avatars.githubusercontent.com',
        
    ],
    'connect-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://cdn.datatables.net',
        'https://github.com',
        'https://unpkg.com',
        'https://avatars.githubusercontent.com',
        
    ],
    'frame-src': [
        '\'self\'',
        'https://domain.cliente.com',
        'https://github.com',
        'https://avatars.githubusercontent.com'
        
    ]
}   
    if srvs:
        for srv in srvs:
            csp_vars.get('connect-src').append(f"https://{srv.address}")
            csp_vars.get('connect-src').append(f"wss://{srv.address}")
    
    return csp_vars
