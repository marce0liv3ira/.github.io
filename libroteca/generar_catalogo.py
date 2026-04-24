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
            box-shadow: 0 0 15px rgba(163, 0, 0, 0.25);
        }}
        .caja-indice h3 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 2.2rem !important; margin-top: 0; color: var(--negro) !important; }}
        .lista-indice {{ list-style-type: square; color: var(--rojo-base); font-size: 1.2rem; font-weight: bold; font-family: 'Inter', sans-serif; }}
        .lista-indice li {{ margin-bottom: 8px; }}
        
        .titulo-categoria {{ 
            font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; color: var(--blanco) !important; 
            background: var(--negro) !important; padding: 5px 15px !important; border-left: 5px solid var(--rojo-sangre) !important; 
            margin: 50px 0 20px 0 !important; text-transform: uppercase !important;
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(163, 0, 0, 0.3);
        }}

        .grilla-tacuru {{
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 25px !important;
            margin: 2rem 0 !important;
            background-color: transparent !important;
        }}

        /* TARJETAS (Redondeadas y radiactivas) */
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
            padding: 25px !important;
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
            background-color: rgba(0, 0, 0, 0.6) !important;
            z-index: 2 !important;
            transition: background-color 0.4s ease !important;
        }}

        .tarjeta-expediente:hover .tarjeta-imagen-wrapper::after {{
            background-color: rgba(0, 0, 0, 0.3) !important;
        }}

        .tarjeta-expediente:hover img {{
            filter: grayscale(0%) contrast(1.1) !important;
            opacity: 0.8 !important;
        }}

        .tarjeta-expediente h3 {{
            font-family: 'Bebas Neue', sans-serif !important;
            color: #ffffff !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin: 0 0 12px 0 !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
            text-shadow: 0 0 8px #000, 2px 2px 4px #000 !important;
            z-index: 11 !important;
        }}

        .tarjeta-expediente p {{
            font-family: 'Inter', sans-serif !important;
            color: var(--fondo-hueso) !important;
            font-size: 1.1rem !important;
            line-height: 1.2 !important;
            margin: 0 !important;
            text-shadow: 0 0 5px #000, 1px 1px 3px #000 !important;
            z-index: 11 !important;
            font-weight: 500;
        }}

        .precio-tacuru {{
            background: var(--rojo-sangre);
            color: var(--blanco);
            padding: 4px 12px;
            margin-top: 10px;
            display: inline-block;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.4rem;
            letter-spacing: 1px;
            border: 1px solid var(--rojo-oscuro);
            border-radius: 4px;
            box-shadow: 0 0 8px rgba(163, 0, 0, 0.5);
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
            background: rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; 
            justify-content: center; padding: 30px; box-sizing: border-box;
        }}
        
        .cerrar-modal {{
            position: absolute; top: 5px; right: 15px; color: var(--rojo-sangre); font-size: 3rem; 
            font-weight: bold; cursor: pointer; z-index: 10; font-family: sans-serif; transition: all 0.2s;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
        }}
        .cerrar-modal:hover {{ color: var(--blanco); transform: scale(1.1); text-shadow: 0 0 10px rgba(163,0,0,0.8); }}
        
        .datos-expediente {{ color: var(--blanco); font-size: 1.1rem; line-height: 1.6; text-align: left; -webkit-user-select: text; user-select: text; font-family: 'Inter', sans-serif; }}
        .datos-expediente strong {{ color: var(--rojo-base); font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 1px; }}
        .modal-titulo {{ font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: var(--blanco); margin: 0 0 20px 0; border-bottom: 1px solid var(--rojo-sangre); line-height: 1.1; padding-bottom: 10px; box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8); }}
        
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

        @media (max-width: 900px) {{
            .grilla-tacuru {{ grid-template-columns: repeat(2, 1fr) !important; }}
            h1 {{ font-size: 4rem !important; }}
            h2 {{ font-size: 2.2rem !important; }}
        }}
        @media (max-width: 600px) {{
            .grilla-tacuru {{ grid-template-columns: 1fr !important; }}
            h1 {{ font-size: 3.5rem !important; }}
            h2 {{ font-size: 1.8rem !important; }}
            .modal-caja {{ width: 95%; aspect-ratio: auto; min-height: 75vh; }}
            .tabs-header {{ flex-direction: column; }}
            .tab-btn {{ border-bottom: 1px solid var(--negro); }}
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

        <div class="caja-menu">
            <div class="tabs-header">
                {tabs_botones}
            </div>
            <div class="tabs-cuerpo">
                {tabs_contenido}
            </div>
        </div>

        <div class="caja-indice">
            <h3>ÍNDICE DE EXPEDIENTES</h3>
            <ul class="lista-indice">
                {indice_html}
            </ul>
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
                    <strong>CATEGORÍA:</strong> <span id="modCat"></span><br>
                    <strong>COLECCIÓN:</strong> <span id="modCol"></span><br>
                    <strong>AÑO:</strong> <span id="modAño"></span><br>
                    <strong>PRECIO:</strong> <span id="modPre"></span>
                </div>
                <button class="btn-copiar" id="btnCopiar" onclick="copiarAlPortapapeles()">COPIAR EXPEDIENTE AL PORTAPAPELES</button>
            </div>
        </div>
    </div>

    <script>
        // JS BLINDADO PARA PESTAÑAS
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
            document.getElementById('modCat').innerText = elemento.getAttribute('data-cat');
            document.getElementById('modCol').innerText = elemento.getAttribute('data-col');
            document.getElementById('modPre').innerText = elemento.getAttribute('data-pre');
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
            const datos = document.getElementById('datosCopiar').innerText;
            const textoFinal = `SOLICITUD DE LIBRO\\n---\\nTÍTULO: ${{titulo}}\\n${{datos}}`;
            
            navigator.clipboard.writeText(textoFinal).then(() => {{
                const btn = document.getElementById('btnCopiar');
                const textoOriginal = btn.innerText;
                btn.innerText = '¡EXPEDIENTE COPIADO!';
                btn.style.background = 'var(--negro)';
                btn.style.color = 'var(--blanco)';
                setTimeout(() => {{
                    btn.innerText = textoOriginal;
                    btn.style.background = 'var(--rojo-sangre)';
                    btn.style.color = 'var(--blanco)';
                }}, 2500);
            }});
        }}
    </script>
</body>
</html>
"""

def generar_catalogo():
    try:
        base_path = os.path.dirname(__file__)
        ruta_json = os.path.join(base_path, 'catalogo.json')
        
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        conf = data.get('config', {})
        
        # 1. Armar Pestañas
        t_btns = ""
        t_cont = ""
        pestañas = data.get('pestañas', [])
        
        for i, tab in enumerate(pestañas):
            act = "active" if i == 0 else ""
            t_id = tab.get("id", f"tab_seguro_{i}")
            t_tit = tab.get("titulo", f"SECCIÓN {i+1}")
            t_txt = tab.get("texto", "")
            
            t_btns += f'<button class="tab-btn {act}" onclick="abrirTab(\'{t_id}\', this)">{t_tit}</button>'
            t_cont += f'<div id="{t_id}" class="tab-content {act}">{t_txt}</div>'

        # 2. Agrupar libros por categoría
        libros_agrupados = defaultdict(list)
        for lib in data.get('libros', []):
            cat = lib.get('categoria', 'Sin Categoría')
            libros_agrupados[cat].append(lib)
            
        # 3. Construir Índice y Secciones
        indice_html = ""
        secciones_html = ""
        
        for cat in sorted(libros_agrupados.keys()):
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n')
            
            indice_html += f'<li><a href="#{cat_id}">{cat}</a></li>'
            
            secciones_html += f'<h2 class="titulo-categoria" id="{cat_id}">{cat}</h2>'
            secciones_html += '<div class="grilla-tacuru">'
            
            for lib in libros_agrupados[cat]:
                tit = lib.get('titulo', 'Sin Título').replace('"', '&quot;')
                aut = lib.get('autor', 'Desconocido').replace('"', '&quot;')
                edi = lib.get('editorial', '-').replace('"', '&quot;')
                cat_txt = lib.get('categoria', '-').replace('"', '&quot;')
                col = lib.get('coleccion', '-').replace('"', '&quot;')
                pre = lib.get('precio', '-').replace('"', '&quot;')
                ano = lib.get('año', '-').replace('"', '&quot;')
                img = lib.get('imagen', '').replace('"', '&quot;')
                
                secciones_html += f"""
                <div class="tarjeta-expediente" 
                     data-tit="{tit}" 
                     data-aut="{aut}" 
                     data-edi="{edi}" 
                     data-cat="{cat_txt}" 
                     data-col="{col}" 
                     data-pre="{pre}" 
                     data-ano="{ano}" 
                     data-img="{img}" 
                     onclick="abrirExpediente(this)">
                     
                    <div class="tarjeta-imagen-wrapper">
                        <img src="{img}" alt="{tit}" onerror="this.style.display='none'">
                    </div>
                    <div class="enlace-tarjeta">
                        <h3>{tit}</h3>
                        <p>{aut}</p>
                        <span class="precio-tacuru">{pre}</span>
                    </div>
                </div>
                """
            secciones_html += '</div>'

        # Renderizar final
        html_final = HTML_TEMPLATE.format(
            titulo_head=conf.get('titulo', 'Libroteca'),
            titulo_pag=conf.get('titulo', 'Libroteca'),
            sub_pag=conf.get('subtitulo', ''),
            bajada_pag=conf.get('bajada', ''),
            tabs_botones=t_btns,
            tabs_contenido=t_cont,
            indice_html=indice_html,
            secciones_html=secciones_html
        )
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_final)
            
        print(">>> Catálogo blindado. Ajustes finos de cartelería y luces neón aplicados.")
        
    except Exception as e:
        print(f">>> ERROR TÉCNICO EN EL TACURÚ (Catálogo): {e}")

if __name__ == "__main__":
    generar_catalogo()
