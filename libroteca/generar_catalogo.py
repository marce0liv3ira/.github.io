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
    
    <meta name="description" content="Libros usados, listos para seguir usándose. Picá y mirá.">
    <meta property="og:title" content="{titulo_head}">
    <meta property="og:description" content="Libros usados, listos para seguir usándose. Picá y mirá.">
    <meta property="og:image" content="https://hormigue.ar/libroteca/img/logolibro.png">
    <meta property="og:type" content="website">
    
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
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}
        
        a {{ color: var(--rojo-sangre) !important; text-decoration: none; transition: color 0.2s ease !important; }}
        a:hover {{ color: #D62828 !important; text-shadow: 0 0 5px rgba(163, 0, 0, 0.4); }}
        
        .contenedor {{ flex: 1; max-width: 1200px; margin: 0 auto; width: 100%; display: flow-root; }}
        
        /* CABECERA CON LOGO DE FONDO Y VELADURA */
        header {{ 
            text-align: center; 
            border-bottom: 1px solid var(--rojo-sangre); 
            padding: 50px 20px; 
            margin-bottom: 30px; 
            border-radius: 8px;
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8);
            /* La veladura (rgba) protege el texto para que el logo no lo ahogue */
            background-image: linear-gradient(rgba(250, 246, 237, 0.85), rgba(250, 246, 237, 0.92)), url('img/logolibro.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        h1 {{ 
            font-family: 'Bebas Neue', sans-serif !important; 
            font-size: 5.5rem !important; 
            color: var(--rojo-sangre) !important; 
            margin: 0; 
            letter-spacing: -0.02em !important; 
            line-height: 1.1 !important; 
            text-shadow: 0 0 10px rgba(163, 0, 0, 0.2);
            position: relative;
            z-index: 2;
        }}
        h2 {{ 
            font-family: 'Bebas Neue', sans-serif !important; 
            font-size: 2.8rem !important; 
            color: var(--negro) !important; 
            margin: 5px 0 15px 0; 
            line-height: 1.1;
            position: relative;
            z-index: 2;
        }}
        .bajada {{ 
            font-size: 1.2rem; font-weight: bold; color: var(--negro); 
            font-family: 'Inter', sans-serif; position: relative; z-index: 2; 
            background: rgba(250, 246, 237, 0.7);
            display: inline-block; padding: 5px 15px; border-radius: 4px;
        }}

        /* CAJA DE MENÚ */
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

        /* ÍNDICE INTERNO (COMPRIMIDO) */
        .caja-indice-interna {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px dashed var(--rojo-sangre);
        }}
        .lista-indice {{ 
            list-style-type: none; 
            padding: 0; 
            margin: 0;
            max-height: 160px; 
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            align-content: flex-start;
            gap: 4px 15px; 
            overflow-x: auto;
        }}
        .lista-indice li {{ 
            font-family: 'Bebas Neue', sans-serif; 
            font-size: 1.25rem; 
            letter-spacing: 1px; 
            line-height: 1.1; 
        }}
        .lista-indice li a {{ color: var(--rojo-oscuro) !important; transition: color 0.2s; }}
        .lista-indice li a:hover {{ color: var(--rojo-sangre) !important; }}

        .titulo-categoria {{ 
            font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; color: var(--blanco) !important; 
            background: var(--negro) !important; padding: 5px 15px !important; border-left: 5px solid var(--rojo-sangre) !important; 
            margin: 50px 0 20px 0 !important; text-transform: uppercase !important;
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(163, 0, 0, 0.3);
        }}

        /* GRILLA: 4 COLUMNAS */
        .grilla-tacuru {{
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 15px !important;
            margin: 2rem 0 !important;
            background-color: transparent !important;
        }}

        .tarjeta-expediente {{
            position: relative !important;
            aspect-ratio: 1 / 1 !important;
            background-color: #000 !important;
            border: 1px solid var(--rojo-oscuro) !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            padding: 0 !important;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(163, 0, 0, 0.2) !important;
        }}

        .enlace-tarjeta {{
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            height: 100% !important;
            padding: 15px !important;
            text-decoration: none !important;
            position: relative !important;
            z-index: 10 !important; 
            box-sizing: border-box !important;
            text-align: center;
        }}

        .tarjeta-expediente:hover {{
            transform: scale(1.03) !important;
            border-color: var(--rojo-sangre) !important;
            box-shadow: 0 0 25px rgba(163, 0, 0, 0.65), inset 0 0 12px rgba(163, 0, 0, 0.4) !important;
        }}

        .tarjeta-imagen-wrapper {{
            position: absolute !important;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1 !important;
        }}

        .tarjeta-imagen-wrapper img {{
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            filter: grayscale(100%) contrast(1.1) !important;
            opacity: 0.6;
            transition: all 0.5s ease !important;
            pointer-events: none;
        }}

        .tarjeta-imagen-wrapper::after {{
            content: "" !important;
            position: absolute !important;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.65) !important;
            z-index: 2 !important;
            transition: background-color 0.4s ease !important;
        }}

        .tarjeta-expediente:hover .tarjeta-imagen-wrapper::after {{
            background-color: rgba(0, 0, 0, 0.15) !important;
        }}

        .tarjeta-expediente:hover img {{
            filter: grayscale(0%) contrast(1.2) saturate(1.8) brightness(1.1) !important;
            opacity: 1 !important;
        }}

        .tarjeta-expediente h3 {{
            font-family: 'Bebas Neue', sans-serif !important;
            color: #ffffff !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin: 0 0 6px 0 !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 8px #000, 2px 2px 4px #000 !important;
            z-index: 11 !important;
            
            display: -webkit-box !important;
            -webkit-line-clamp: 4 !important;
            -webkit-box-orient: vertical !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        .tarjeta-expediente p {{
            font-family: 'Inter', sans-serif !important;
            color: var(--fondo-hueso) !important;
            font-size: 0.95rem !important;
            line-height: 1.2 !important;
            margin: 0 !important;
            text-shadow: 0 0 5px #000, 1px 1px 3px #000 !important;
            z-index: 11 !important;
            font-weight: 500;
            
            display: -webkit-box !important;
            -webkit-line-clamp: 2 !important;
            -webkit-box-orient: vertical !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        /* PIE DE PÁGINA HORMIGUEAR */
        footer {{
            margin-top: 60px;
            padding: 40px 20px;
            text-align: center;
            background-color: var(--negro);
            border-top: 4px solid var(--rojo-sangre);
            box-shadow: 0 -4px 15px rgba(163, 0, 0, 0.3);
        }}
        .link-hormiguear {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            color: var(--fondo-hueso) !important;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            transition: all 0.3s ease !important;
        }}
        .link-hormiguear:hover {{
            color: var(--rojo-sangre) !important;
            text-shadow: 0 0 10px rgba(163, 0, 0, 0.5);
            transform: translateY(-3px);
        }}
        .svg-hormiga {{
            width: 45px;
            height: 45px;
            fill: var(--rojo-sangre);
            margin-bottom: 12px;
            transition: fill 0.3s ease, transform 0.3s ease;
        }}
        .link-hormiguear:hover .svg-hormiga {{
            fill: var(--fondo-hueso);
            transform: scale(1.1);
        }}

        /* MODAL VISOR */
        .modal-overlay {{
            display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px);
        }}
        
        .modal-caja {{
            position: relative; width: 90%; max-width: 450px; aspect-ratio: 2/3; 
            border: 2px solid var(--rojo-sangre); 
            border-radius: 8px;
            box-shadow: 0 0 35px rgba(163, 0, 0, 0.7);
            background-size: cover; background-position: center;
            overflow: hidden;
        }}
        
        .modal-oscuridad {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.65); 
            display: flex; flex-direction: column; 
            justify-content: center; padding: 30px; box-sizing: border-box;
        }}
        
        .cerrar-modal {{
            position: absolute; top: 5px; right: 15px; color: var(--rojo-sangre); font-size: 3rem; 
            font-weight: bold; cursor: pointer; z-index: 10; font-family: sans-serif; transition: all 0.2s;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
        }}
        .cerrar-modal:hover {{ color: var(--blanco); transform: scale(1.1); text-shadow: 0 0 10px rgba(163,0,0,0.8); }}
        
        .datos-expediente {{ 
            color: var(--blanco); font-size: 1.2rem; line-height: 1.8; text-align: left; 
            -webkit-user-select: text; user-select: text; font-family: 'Inter', sans-serif;
            text-shadow: 0 0 8px #000, 0 0 15px #000; 
        }}
        .datos-expediente strong {{ color: var(--rojo-base); font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 1px; }}
        
        .modal-titulo {{ 
            font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: var(--blanco); 
            margin: 0 0 20px 0; border-bottom: 1px solid var(--rojo-sangre); line-height: 1.1; 
            padding-bottom: 10px; box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8); 
            text-shadow: 0 0 8px #000, 0 0 15px #000; 
        }}
        
        .btn-copiar {{
            margin-top: 25px; width: 100%; padding: 15px; background: var(--rojo-sangre); 
            color: var(--blanco); border: 1px solid var(--rojo-oscuro); font-family: 'Bebas Neue', sans-serif; 
            font-size: 1.6rem; cursor: pointer; border-radius: 8px;
            box-shadow: 0 0 10px rgba(163, 0, 0, 0.4);
            transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), filter 0.3s ease, box-shadow 0.3s ease !important;
        }}
        .btn-copiar:hover {{ 
            transform: scale(1.02) !important;
            background: var(--rojo-sangre); 
            color: var(--blanco); 
            box-shadow: 0 0 20px rgba(158, 40, 19, 0.8), inset 0 0 8px rgba(158, 40, 19, 0.4) !important;
        }}

        #btn-ascenso {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 55px;
            height: 55px;
            background: rgba(0, 0, 0, 0.8);
            color: var(--blanco);
            border: 2px solid var(--rojo-sangre);
            border-radius: 50%;
            font-size: 2rem;
            cursor: pointer;
            display: none; 
            justify-content: center;
            align-items: center;
            z-index: 1000;
            box-shadow: 0 0 15px rgba(163, 0, 0, 0.5);
            transition: all 0.3s ease;
            backdrop-filter: blur(4px);
            text-decoration: none;
            padding-bottom: 5px; 
        }}
        #btn-ascenso:hover {{
            transform: scale(1.1);
            background: var(--rojo-sangre);
            box-shadow: 0 0 25px rgba(163, 0, 0, 0.8);
        }}

        @media (max-width: 900px) {{
            .grilla-tacuru {{ grid-template-columns: repeat(3, 1fr) !important; }}
            h1 {{ font-size: 4rem !important; }}
            h2 {{ font-size: 2.2rem !important; }}
        }}
        @media (max-width: 600px) {{
            .grilla-tacuru {{ grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }}
            h1 {{ font-size: 3.5rem !important; }}
            h2 {{ font-size: 1.8rem !important; }}
            .modal-caja {{ width: 95%; aspect-ratio: auto; min-height: 75vh; }}
            .tabs-header {{ flex-direction: column; }}
            .tab-btn {{ border-bottom: 1px solid var(--negro); }}
            #btn-ascenso {{ bottom: 20px; right: 20px; width: 45px; height: 45px; font-size: 1.5rem; }}
            .enlace-tarjeta {{ padding: 10px !important; }}
            .tarjeta-expediente h3 {{ font-size: 1.15rem !important; margin-bottom: 4px !important; }}
            .tarjeta-expediente p {{ font-size: 0.85rem !important; }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <header>
            <h1>{titulo_pag}</h1>
            <h2>{sub_pag}</h2>
            <div class="bajada">{bajada_pag}</div>
        </header>

        <div class="caja-menu" id="menu-selector">
            <div class="tabs-header">
                {tabs_botones}
            </div>
            <div class="tabs-cuerpo">
                {tabs_contenido}
            </div>
        </div>

        {secciones_html}
    </div>

    <div id="modalLibro" class="modal-overlay" onclick="cerrarModal(event)">
        <div class="modal-caja" id="modalFondo">
            <span class="cerrar-modal" onclick="cerrarModalFuerza()">&times;</span>
            <div class="modal-oscuridad">
                <div class="modal-titulo" id="modTit"></div>
                <div class="datos-expediente" id="datosCopiar">
                    <strong>AUTOR:</strong> <span id="modAut"></span><br>
                    <strong>EDITORIAL:</strong> <span id="modEdi"></span><br>
                    <strong>AÑO:</strong> <span id="modAño"></span>
                </div>
                <button class="btn-copiar" id="btnCopiar" onclick="copiarAlPortapapeles()">COPIAR</button>
            </div>
        </div>
    </div>

    <div id="btn-ascenso" onclick="volverArriba()" title="Volver al índice">&#8679;</div>

    <footer>
        <a href="https://hormigue.ar/" class="link-hormiguear" target="_blank" rel="noopener noreferrer">
            <svg class="svg-hormiga" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12,2C9.5,2 7.5,3.8 7.1,6.1C5.7,6.8 4.6,8 4.2,9.6C3.9,11 4.2,12.5 5,13.7L3.5,15.2C3.1,15.6 3.1,16.2 3.5,16.6C3.9,17 4.5,17 4.9,16.6L6.4,15.1C7.8,16.2 9.8,17 12,17C14.2,17 16.2,16.2 17.6,15.1L19.1,16.6C19.5,17 20.1,17 20.5,16.6C20.9,16.2 20.9,15.6 20.5,15.2L19,13.7C19.8,12.5 20.1,11 19.8,9.6C19.4,8 18.3,6.8 16.9,6.1C16.5,3.8 14.5,2 12,2ZM12,4C13.7,4 15,5.3 15,7C15,8.7 13.7,10 12,10C10.3,10 9,8.7 9,7C9,5.3 10.3,4 12,4ZM7.5,10.5C8.3,10.5 9,11.2 9,12C9,12.8 8.3,13.5 7.5,13.5C6.7,13.5 6,12.8 6,12C6,11.2 6.7,10.5 7.5,10.5ZM16.5,10.5C17.3,10.5 18,11.2 18,12C18,12.8 17.3,13.5 16.5,13.5C15.7,13.5 15,12.8 15,12C15,11.2 15.7,10.5 16.5,10.5Z"/>
                <path d="M12,18C9,18 6.5,19.5 5.5,22H18.5C17.5,19.5 15,18 12,18Z"/>
            </svg>
            Conocé el sitio creado con pocos recursos económicos, técnicos e intelectuales.
        </a>
    </footer>

    <script>
        function abrirTab(idTab, elemento) {{
            try {{
                var contenidos = document.querySelectorAll('.tab-content');
                for(var i = 0; i < contenidos.length; i++) {{ contenidos[i].classList.remove('active'); }}
                
                var botones = document.querySelectorAll('.tab-btn');
                for(var j = 0; j < botones.length; j++) {{ botones[j].classList.remove('active'); }}
                
                var panelDestino = document.getElementById(idTab);
                if (panelDestino) {{ panelDestino.classList.add('active'); }}
                if (elemento) {{ elemento.classList.add('active'); }}
            }} catch(error) {{
                console.error("Error táctico en pestañas:", error);
            }}
        }}

        const modal = document.getElementById('modalLibro');
        
        function abrirExpediente(elemento) {{
            document.getElementById('modTit').innerText = elemento.getAttribute('data-tit');
            document.getElementById('modAut').innerText = elemento.getAttribute('data-aut');
            document.getElementById('modEdi').innerText = elemento.getAttribute('data-edi');
            document.getElementById('modAño').innerText = elemento.getAttribute('data-ano');
            
            const imgUrl = elemento.getAttribute('data-img');
            document.getElementById('modalFondo').style.backgroundImage = `url('${{imgUrl}}')`;
            
            modal.style.display = 'flex';
        }}

        function cerrarModal(e) {{
            if (e.target === modal) modal.style.display = 'none';
        }}
        function cerrarModalFuerza() {{ modal.style.display = 'none'; }}

        function copiarAlPortapapeles() {{
            const titulo = document.getElementById('modTit').innerText;
            const aut = document.getElementById('modAut').innerText;
            const edi = document.getElementById('modEdi').innerText;
            const ano = document.getElementById('modAño').innerText;
            
            const textoFinal = `Quiero este libro: "${{titulo}}" de "${{aut}}" ("${{edi}}", "${{ano}}").`;
            
            navigator.clipboard.writeText(textoFinal).then(() => {{
                const btn = document.getElementById('btnCopiar');
                const textoOriginal = btn.innerText;
                btn.innerText = '¡COPIADO!';
                btn.style.background = 'var(--negro)';
                btn.style.color = 'var(--blanco)';
                setTimeout(() => {{
                    btn.innerText = textoOriginal;
                    btn.style.background = 'var(--rojo-sangre)';
                    btn.style.color = 'var(--blanco)';
                }}, 2500);
            }});
        }}

        window.onscroll = function() {{
            var btn = document.getElementById("btn-ascenso");
            if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {{
                btn.style.display = "flex";
            }} else {{
                btn.style.display = "none";
            }}
        }};

        function volverArriba() {{
            document.getElementById('menu-selector').scrollIntoView({{ behavior: 'smooth' }});
        }}
    </script>
</body>
</html>
"""

def normalizar_categoria(cat_cruda):
    c = cat_cruda.lower()
    
    if 'ensayo' in c:
        return 'Ensayo'
    if 'historia' in c:
        return 'Historia'
    if 'polític' in c or 'politic' in c:
        return 'Política'
    if 'comunicaci' in c:
        return 'Comunicación'
    if 'filosof' in c:
        return 'Filosofía'
    if 'narrativa' in c or 'literatura' in c:
        return 'Literatura'
        
    return cat_cruda.split('/')[0].strip().title()

def generar_catalogo():
    try:
        base_path = os.path.dirname(__file__)
        ruta_json = os.path.join(base_path, 'catalogo.json')
        
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        conf = data.get('config', {})
        
        libros_agrupados = defaultdict(list)
        for lib in data.get('libros', []):
            cat_cruda = lib.get('categoria', 'Sin Categoría')
            cat_maestra = normalizar_categoria(cat_cruda)
            libros_agrupados[cat_maestra].append(lib)
            
        indice_html = '<ul class="lista-indice">'
        for cat in sorted(libros_agrupados.keys()):
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n').replace('ó','o').replace('í','i').replace('á','a')
            indice_html += f'<li><a href="#{cat_id}">{cat.upper()}</a></li>'
        indice_html += '</ul>'

        t_btns = ""
        t_cont = ""
        pestañas = data.get('pestañas', [])
        
        for i, tab in enumerate(pestañas):
            act = "active" if i == 0 else ""
            t_id = tab.get("id", f"tab_seguro_{i}")
            t_tit = tab.get("titulo", f"SECCIÓN {i+1}")
            t_txt = tab.get("texto", "")
            
            if t_tit.upper() == "CONTENIDO" or t_id == "tab1":
                t_txt = f'<div class="texto-pestaña">{t_txt}</div><div class="caja-indice-interna">{indice_html}</div>'
            
            t_btns += f'<button class="tab-btn {act}" onclick="abrirTab(\'{t_id}\', this)">{t_tit}</button>'
            t_cont += f'<div id="{t_id}" class="tab-content {act}">{t_txt}</div>'

        secciones_html = ""
        for cat in sorted(libros_agrupados.keys()):
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n').replace('ó','o').replace('í','i').replace('á','a')
            
            secciones_html += f'<h2 class="titulo-categoria" id="{cat_id}">{cat.upper()}</h2>'
            secciones_html += '<div class="grilla-tacuru">'
            
            for lib in libros_agrupados[cat]:
                tit = lib.get('titulo', 'Sin Título').replace('"', '&quot;')
                aut = lib.get('autor', 'Desconocido').replace('"', '&quot;')
                edi = lib.get('editorial', '-').replace('"', '&quot;')
                ano = lib.get('año', '-').replace('"', '&quot;')
                img = lib.get('imagen', '').replace('"', '&quot;')
                
                secciones_html += f"""
                <div class="tarjeta-expediente" 
                     data-tit="{tit}" 
                     data-aut="{aut}" 
                     data-edi="{edi}" 
                     data-ano="{ano}" 
                     data-img="{img}" 
                     onclick="abrirExpediente(this)">
                     
                    <div class="tarjeta-imagen-wrapper">
                        <img src="{img}" alt="{tit}" onerror="this.style.display='none'">
                    </div>
                    <div class="enlace-tarjeta">
                        <h3>{tit}</h3>
                        <p>{aut}</p>
                    </div>
                </div>
                """
            secciones_html += '</div>'

        html_final = HTML_TEMPLATE.format(
            titulo_head=conf.get('titulo', 'Libroteca'),
            titulo_pag=conf.get('titulo', 'Libroteca'),
            sub_pag=conf.get('subtitulo', ''),
            bajada_pag=conf.get('bajada', ''),
            tabs_botones=t_btns,
            tabs_contenido=t_cont,
            secciones_html=secciones_html
        )
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_final)
            
        print(">>> Catálogo finalizado. Cabecera, carnada SEO y manifiesto nodocente inyectados con éxito.")
        
    except Exception as e:
        print(f">>> ERROR TÉCNICO EN EL TACURÚ (Catálogo): {e}")

if __name__ == "__main__":
    generar_catalogo()
