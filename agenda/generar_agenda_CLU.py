import json
import os
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRONOGRAMA DE PARO ACTIVO - CLU</title>
    <link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@700&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{ --neon: #00FF00; --black: #000000; --white: #FFFFFF; }}
        body {{ background: var(--white); color: var(--black); font-family: 'Roboto Condensed', sans-serif; padding: 20px; line-height: 1.6; margin: 0; }}
        
        /* Recuadro General con Neón Negro */
        .wrap {{ 
            max-width: 800px; 
            margin: 40px auto; 
            border: 4px solid var(--black); 
            padding: 30px; 
            box-shadow: 0 0 20px rgba(0,0,0,0.8); /* Efecto Neón Negro */
            background-color: var(--white);
        }}
        
        header {{ text-align: center; border-bottom: 4px solid var(--black); margin-bottom: 30px; padding-bottom: 20px; }}
        .logo-link img {{ max-width: 180px; height: auto; }}
        h1 {{ font-family: 'Archivo Narrow', sans-serif; font-size: 2.5rem; text-transform: uppercase; margin: 15px 0 0 0; line-height: 1; }}
        
        .intro-text {{ text-align: justify; border: 1px solid #ddd; padding: 15px; background: #fafafa; margin-bottom: 30px; font-size: 0.95rem; }}
        .intro-text a {{ color: var(--black); text-decoration: underline; text-decoration-color: var(--neon); }}
        
        .dia-bloque {{ margin-bottom: 40px; }}
        .fecha {{ font-family: 'Archivo Narrow', sans-serif; font-size: 1.6rem; background: var(--black); color: var(--neon); padding: 5px 15px; display: inline-block; margin-bottom: 15px; }}
        
        details {{ border-bottom: 1px solid var(--black); }}
        summary {{ padding: 15px 0; cursor: pointer; font-weight: 700; display: flex; justify-content: space-between; align-items: center; list-style: none; }}
        
        /* Flecha Verde de despliegue */
        summary::after {{ content: '→'; color: var(--neon); font-size: 1.2rem; background: var(--black); padding: 0 10px; }}
        details[open] summary::after {{ content: '↓'; }}
        
        .info {{ padding: 20px; background: #f9f9f9; border-left: 6px solid var(--neon); }}
        .hora {{ background: var(--neon); color: var(--black); padding: 2px 8px; margin-right: 10px; font-weight: bold; border: 1px solid var(--black); }}
        
        footer {{ margin-top: 50px; text-align: center; font-family: 'Archivo Narrow', sans-serif; border-top: 4px solid var(--black); padding-top: 20px; text-transform: uppercase; font-size: 1rem; }}
        .insta-footer {{ color: var(--black); font-size: 1.5rem; margin: 0 10px; vertical-align: middle; }}
    </style>
</head>
<body>
    <div class="wrap">
        <header>
            <a href="https://www.instagram.com/comitedelucha" class="logo-link" target="_blank">
                <img src="logo_clu.png" alt="CLU" onerror="this.src='https://via.placeholder.com/200x80?text=CLU+UNAM'">
            </a>
            <h1>Cronograma de Paro Activo</h1>
            <p><strong>Semana del 13 al 17 de abril</strong></p>
        </header>

        <div class="intro-text">{intro}</div>
        
        {contenido}

        <footer>
            Comité de Lucha Universitaria 
            <a href="https://www.instagram.com/comitedelucha" class="insta-footer" target="_blank"><i class="fab fa-instagram"></i></a> 
            Universidad Nacional de Misiones
        </footer>
    </div>
</body>
</html>
"""

def hormiguear_web():
    try:
        base_path = os.path.dirname(__file__)
        ruta_json = os.path.join(base_path, 'agendaCLU.json')
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        bloques_html = ""
        for dia in data['cronograma']:
            bloques_html += f'<div class="dia-bloque"><div class="fecha">{dia["dia"]}</div>'
            for act in dia["actividades"]:
                bloques_html += f"""
                <details>
                    <summary><span><span class="hora">{act['hora']}</span> {act['titulo']}</span></summary>
                    <div class="info">{act['detalle']}</div>
                </details>"""
            bloques_html += "</div>"
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE.format(intro=data['introduccion'], contenido=bloques_html))
        print(">>> Despliegue CLU finalizado.")
    except Exception as e:
        print(f">>> ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    hormiguear_web()
