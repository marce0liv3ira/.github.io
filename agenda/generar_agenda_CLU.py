import json
import os
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>CRONOGRAMA PARO ACTIVO - CLU</title>
    <meta name="description" content="Propuesta del Comité de Lucha Universitaria para las actividades de paro activo del 13 al 17 de abril.">
    <meta property="og:title" content="CRONOGRAMA PARO ACTIVO - CLU">
    <meta property="og:description" content="Actividades de paro activo (13-17 de abril). Unidad de estudiantes, docentes y nodocentes.">
    <meta property="og:image" content="https://hormigue.ar/agenda/logo_clu.png">
    <meta property="og:url" content="https://hormigue.ar/agenda/">
    <meta property="og:type" content="website">

    <link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@700&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        :root {{ --neon-green: #00FF00; --black: #000000; --white: #FFFFFF; }}
        
        body {{ 
            background: var(--white); 
            color: var(--black); 
            font-family: 'Roboto Condensed', sans-serif; 
            font-size: 1.15rem; /* Aumento de ~2pt sobre el estándar */
            padding: 20px; 
            line-height: 1.6; 
            margin: 0; 
        }}
        
        /* 1. RECUADRO GENERAL CON NEÓN NEGRO */
        .wrap {{ 
            max-width: 800px; 
            margin: 40px auto; 
            border: 5px solid var(--black); 
            padding: 30px; 
            background-color: var(--white);
            /* Efecto neón negro: resplandor sólido y profundo */
            box-shadow: 0 0 10px var(--black), 
                        0 0 20px rgba(0,0,0,0.5),
                        10px 10px 0px var(--black); 
        }}
        
        header {{ text-align: center; border-bottom: 5px solid var(--black); margin-bottom: 30px; padding-bottom: 20px; }}
        
        /* 4. LOGO REDUCIDO UN CUARTO */
        .logo-clu {{ 
            width: 100%; 
            max-width: 240px; /* Reducción a 3/4 del tamaño anterior */
            height: auto; 
            margin: 0 auto 15px auto; 
            display: block; 
            object-fit: contain; 
        }}
        
        /* 3. TÍTULO CRONOGRAMA PARO ACTIVO */
        h1 {{ 
            font-family: 'Archivo Narrow', sans-serif; 
            font-weight: 700;
            font-size: 3rem; /* Tamaño aumentado */
            text-transform: uppercase; 
            margin: 0; 
            line-height: 0.95; /* Interlineado reducido */
            letter-spacing: -1px;
        }}
        
        .intro-text {{ text-align: justify; border: 1px solid #ddd; padding: 20px; background: #fafafa; margin-bottom: 30px; font-size: 1rem; }}
        .intro-text a {{ color: var(--black); font-weight: bold; text-decoration: underline; text-decoration-color: var(--neon-green); }}
        
        .dia-bloque {{ margin-bottom: 40px; }}
        .fecha {{ 
            font-family: 'Archivo Narrow', sans-serif; 
            font-size: 1.8rem; 
            background: var(--black); 
            color: var(--neon-green); 
            padding: 5px 15px; 
            display: inline-block; 
            margin-bottom: 15px; 
        }}
        
        details {{ border-bottom: 1px solid var(--black); }}
        summary {{ padding: 15px 0; cursor: pointer; font-weight: 700; display: flex; justify-content: space-between; align-items: center; list-style: none; font-size: 1.2rem; }}
        
        summary::after {{ 
            content: '→'; 
            color: var(--neon-green); 
            font-size: 1.3rem; 
            background: var(--black); 
            padding: 0 10px; 
            border: 1px solid var(--neon-green);
        }}
        details[open] summary::after {{ content: '↓'; }}
        
        .info {{ padding: 20px; background: #f9f9f9; border-left: 6px solid var(--neon-green); }}
        .hora {{ background: var(--neon-green); color: var(--black); padding: 2px 8px; margin-right: 10px; font-weight: bold; border: 1px solid var(--black); }}
        
        footer {{ margin-top: 50px; text-align: center; font-family: 'Archivo Narrow', sans-serif; border-top: 5px solid var(--black); padding-top: 20px; text-transform: uppercase; font-size: 1.1rem; }}
        .insta-footer {{ color: var(--black); font-size: 1.8rem; margin: 0 10px; vertical-align: middle; }}
    </style>
</head>
<body>
    <div class="wrap">
        <header>
            <a href="https://www.instagram.com/comitedelucha" target="_blank">
                <img src="logo_clu.png" alt="CLU" class="logo-clu" onerror="this.src='https://via.placeholder.com/240x100?text=CLU+UNAM'">
            </a>
            <h1>CRONOGRAMA<br>PARO ACTIVO</h1>
            <p style="margin-top:10px; font-weight: bold;">Semana del 13 al 17 de abril</p>
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
        print(">>> Orden técnica establecida. Despliegue finalizado.")
    except Exception as e:
        print(f">>> ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    hormiguear_web()
