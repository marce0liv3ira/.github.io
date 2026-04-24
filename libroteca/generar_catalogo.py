import json
import os
from collections import defaultdict

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo_head}</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{ 
            --rojo-base: #991A1A; 
            --rojo-sangre: #A30000; 
            --rojo-oscuro: #660000;
            --gris-ceniza: #8E7171; 
            --fondo-hueso: #FAF6ED;
            --blanco: #FFFFFF; 
            --negro: #000000;
        }}
        
        body {{ 
            background-color: var(--fondo-hueso) !important; 
            color: #1a1a1a !important; 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 20px; 
            -webkit-user-select: none;
            user-select: none; 
        }}
        
        a {{ color: var(--rojo-sangre) !important; text-decoration: none; transition: color 0.2s ease !important; }}
        a:hover {{ color: #D62828 !important; text-shadow: 0 0 5px rgba(163, 0, 0, 0.4); }}
        
        .contenedor {{ max-width: 1200px; margin: 0 auto; display: flow-root; }}
        
        /* CABECERA (Línea ultrafina y títulos enormes) */
        header {{ 
            text-align: center; 
            border-bottom: 1px solid var(--rojo-sangre); 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8); /* Resplandor inferior de la línea */
        }}
        h1 {{ 
            font-family: 'Bebas Neue', sans-serif !important; 
            font-size: 5.5rem !important; 
            color: var(--rojo-sangre) !important; 
            margin: 0; 
            letter-spacing: -0.02em !important; 
            line-height: 1.1 !important; 
            text-shadow: 0 0 10px rgba(163, 0, 0, 0.2);
        }}
        h2 {{ 
            font-family: 'Bebas Neue', sans-serif !important; 
            font-size: 2.8rem !important; 
            color: var(--negro) !important; 
            margin: 5px 0 15px 0; 
            line-height: 1.1;
        }}
        .bajada {{ font-size: 1.2rem; font-weight: bold; color: var(--gris-ceniza); font-family: 'Inter', sans-serif; }}

        /* CAJA DE MENÚ (Redondeada con neón sutil) */
        .caja-menu {{ 
            border: 1px solid var(--rojo-sangre); 
            margin-bottom: 40px; 
            background: #fff; 
            border-radius: 8px; 
            overflow: hidden;
            box-shadow: 0 0 12px rgba(163, 0, 0, 0.25);
        }}
        .tabs-header {{ display: flex; border-bottom: 1px solid var(--rojo-sangre); background: var(--negro); }}
        .tab-btn {{ 
            flex: 1; padding: 12px; cursor: pointer; font-family: 'Bebas Neue', sans-serif; 
            font-size: 1.5rem; color: var(--blanco); background: transparent; border: none; 
            transition: all 0.3s ease; letter-spacing: 1px;
        }}
        .tab-btn.active, .tab-btn:hover {{ 
            background: var(--rojo-sangre); 
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
        }}
        .tab-content {{ padding: 20px; display: none; font-size: 1.1rem; font-family: 'Inter', sans-serif; }}
        .tab-content.active {{ display: block; }}

        /* ÍNDICE DE CATEGORÍAS (Sin cubo, puro resplandor) */
        .caja-indice {{ 
            border: 1px solid var(--rojo-sangre); 
            padding: 20px; 
            margin-bottom: 40px; 
            background: var(--blanco); 
            border-radius: 8px;
            box-shadow:
