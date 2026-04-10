import json
import os
from datetime import datetime

# Estética: Terminal de Resistencia (Verde, Negro, Blanco)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agenda de Lucha - Universidad Pública</title>
    <style>
        body {{ background-color: #000000; color: #FFFFFF; font-family: 'Courier New', monospace; padding: 20px; line-height: 1.5; }}
        .wrap {{ max-width: 800px; margin: auto; border: 1px solid #00FF00; padding: 20px; box-shadow: 0 0 15px #004400; }}
        h1 {{ color: #00FF00; text-align: center; border-bottom: 2px solid #00FF00; padding-bottom: 10px; text-transform: uppercase; }}
        .dia-bloque {{ margin-top: 30px; border-left: 4px solid #00FF00; padding-left: 15px; }}
        .fecha {{ color: #00FF00; font-weight: bold; font-size: 1.3rem; margin-bottom: 15px; }}
        details {{ background: #0a0a0a; margin-bottom: 10px; border: 1px solid #333; cursor: pointer; }}
        summary {{ padding: 12px; font-weight: bold; outline: none; }}
        summary:hover {{ background: #002200; color: #00FF00; }}
        .info {{ padding: 15px; border-top: 1px solid #00FF00; color: #CCC; font-size: 0.95rem; background: #050505; }}
        .hora {{ color: #00FF00; font-weight: bold; margin-right: 10px; border: 1px solid #00FF00; padding: 2px 5px; }}
        footer {{ margin-top: 40px; text-align: center; font-size: 0.7rem; color: #444; border-top: 1px dashed #333; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="wrap">
        <h1>[ AGENDA DE MOVILIZACIÓN ]</h1>
        <p style="text-align: center; color: #00FF00;">> ESTADO: EN LUCHA | ACTUALIZADO: {fecha_act}</p>
        
        {contenido}

        <footer>
            GENERADO AUTOMÁTICAMENTE - TACURÚ DIGITAL - POSADAS, MISIONES
        </footer>
    </div>
</body>
</html>
"""

def hormiguear_web():
    try:
        # Buscamos el archivo con el nombre específico que definiste
        base_path = os.path.dirname(__file__)
        ruta_json = os.path.join(base_path, 'agendaCLU.json')
        
        if not os.path.exists(ruta_json):
            print(f">>> ERROR: No encuentro el archivo {ruta_json}")
            return

        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        fecha_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        bloques_html = ""
        for dia in datos:
            bloques_html += f'<div class="dia-bloque"><div class="fecha">{dia["dia"]}</div>'
            for act in dia["actividades"]:
                bloques_html += f"""
                <details>
                    <summary><span class="hora">{act['hora']}</span> {act['titulo']}</summary>
                    <div class="info">{act['detalle']}</div>
                </details>
                """
            bloques_html += "</div>"
        
        # El resultado siempre será index.html para que el servidor lo reconozca
        ruta_salida = os.path.join(base_path, 'index.html')
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE.format(fecha_act=fecha_str, contenido=bloques_html))
            
        print(">>> Éxito: index.html generado quirúrgicamente.")
        
    except Exception as e:
        print(f">>> FALLO LÓGICO: {e}")

if __name__ == "__main__":
    hormiguear_web()
