import json
import os
from datetime import datetime

# Estética: Blanco, Negro y Neón Negro (Sombra sólida)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Cronograma de Paro Activo - CLU</title>
    <meta name="description" content="Esta es la propuesta del Comité de Lucha Universitaria para las actividades de paro activo del 13 al 17 de abril. Sumá tu propuesta.">
    <meta property="og:title" content="Cronograma de Paro Activo - CLU">
    <meta property="og:description" content="Esta es la propuesta del Comité de Lucha Universitaria para las actividades de paro activo del 13 al 17 de abril. Sumá tu propuesta.">
    <meta property="og:image" content="https://hormigue.ar/agenda/logo_clu.png">
    <meta property="og:url" content="https://hormigue.ar/agenda/">
    <meta property="og:type" content="website">

    <link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@700&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        :root {{ --neon: #00FF00; --black: #000000; --white: #FFFFFF; }}
        body {{ background: var(--white); color: var(--black); font-family: 'Roboto Condensed', sans-serif; padding: 20px; line-height: 1.6; margin: 0; }}
        
        /* Recuadro con Sombra Negra Sólida */
        .wrap {{ 
            max-width: 800px; 
            margin: 40px auto; 
            border: 5px solid var(--black); 
            padding: 30px; 
            box-shadow: 12px 12px 0px var(--black); 
            background-color: var(--white);
        }}
        
        header {{ text-align: center; border-bottom: 5px solid var(--black); margin-bottom: 30px; padding-bottom: 20px; }}
        
        /* Estilo del Logo */
        .logo-clu {{ 
            max-width: 220px; 
            height: auto; 
            display: block; 
            margin: 0 auto 15px auto;
            transition: transform 0.2s ease-in-out;
        }}
        .logo-clu:hover {{ transform: scale(1.03); }}
        
        h1 {{ font-family: 'Archivo Narrow', sans-serif; font-size: 2.5rem; text-transform: uppercase; margin: 0; line-height: 1.1; }}
        
        .intro-text {{ text-align: justify; border: 1px solid #ddd; padding: 20px; background: #fafafa; margin-bottom: 30px; font-size: 0.95rem; }}
        .intro-text a {{ color: var(--black); text-decoration: underline; text-decoration-color: var(--neon); }}
        
        .dia-bloque {{ margin-bottom: 40px; }}
        .fecha {{ font-family: 'Archivo Narrow', sans-serif; font-size: 1.6rem; background: var(--black); color: var(--neon); padding: 5px 15px; display: inline-block; margin-bottom: 15px; }}
        
        details {{ border-bottom: 1px solid var(--black); }}
        summary {{ padding: 15px 0; cursor: pointer; font-weight: 700; display: flex; justify-content: space-between; align-items: center; list-style: none; }}
        summary::after {{ content: '→'; color: var(--neon); font-size: 1.2rem; background: var(--black); padding: 0 10px; }}
        details[open] summary::after {{ content: '↓'; }}
        
        .info {{ padding: 20px; background: #f9f9f9; border-left: 6px solid var(--neon); }}
        .hora {{ background: var(--neon); color: var(--black); padding: 2px 8px; margin-right: 10px; font-weight: bold; border: 1px solid var(--black); }}
        
        footer {{ margin-top: 50px; text-align: center; font-family: 'Archivo Narrow', sans-serif; border-top: 5px solid var(--black); padding-top: 20px; text-transform: uppercase; font-size: 1rem; }}
        .insta-footer {{ color: var(--black); font-size: 1.6rem; margin: 0 10px; vertical-align: middle; }}
    </style>
</head>
<body>
    <div class="wrap">
        <header>
            <a href="https://www.instagram.com/comitedelucha" target="_blank">
                <img src="logo_clu.png" alt="Logo Comité de Lucha" class="logo-clu" onerror="this.src='https://via.placeholder.com/220x100?text=CLU+UNAM'">
            </a>
            <h1>Cronograma de Paro Activo</h1>
            <p style="margin-top:10px;"><strong>Semana del 13 al 17 de abril</strong></p>
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
        print(">>> Despliegue CLU Finalizado con Logo y SEO.")
    except Exception as e:
        print(f">>> ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    hormiguear_web()
