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
    
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{ 
            --rojo-base: #991A1A; 
            --rojo-sangre: #A30000; 
            --gris-ceniza: #8E7171; 
            --blanco: #FFFFFF; 
            --negro: #000000;
            --azul-enlace: #0000EE; 
        }}
        
        body {{ 
            background-color: var(--blanco); 
            color: var(--negro); 
            font-family: 'Roboto Condensed', sans-serif; 
            margin: 0; 
            padding: 20px; 
            /* MEDIDAS DE SEGURIDAD */
            -webkit-user-select: none;
            user-select: none; 
        }}
        
        a {{ color: var(--azul-enlace); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        
        .contenedor {{ max-width: 1200px; margin: 0 auto; }}
        
        /* CABECERA */
        header {{ text-align: center; border-bottom: 6px double var(--rojo-sangre); padding-bottom: 20px; margin-bottom: 30px; }}
        h1 {{ font-family: 'Bebas Neue', sans-serif; font-size: 4rem; color: var(--rojo-sangre); margin: 0; letter-spacing: 2px; }}
        h2 {{ font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: var(--negro); margin: 5px 0; }}
        .bajada {{ font-size: 1.2rem; font-weight: bold; color: var(--gris-ceniza); }}

        /* CAJA DE PESTAÑAS */
        .caja-menu {{ border: 3px solid var(--negro); margin-bottom: 40px; background: #fafafa; }}
        .tabs-header {{ display: flex; border-bottom: 3px solid var(--negro); background: var(--negro); }}
        .tab-btn {{ 
            flex: 1; padding: 12px; cursor: pointer; font-family: 'Bebas Neue', sans-serif; 
            font-size: 1.3rem; color: var(--blanco); background: transparent; border: none; 
            transition: background 0.3s; 
        }}
        .tab-btn.active, .tab-btn:hover {{ background: var(--rojo-sangre); }}
        .tab-content {{ padding: 20px; display: none; font-size: 1.1rem; border-left: 6px solid var(--rojo-base); }}
        .tab-content.active {{ display: block; }}

        /* ÍNDICE DE CATEGORÍAS */
        .caja-indice {{ 
            border: 4px solid var(--rojo-sangre); padding: 20px; margin-bottom: 40px; 
            background: #fff; box-shadow: 4px 4px 0px var(--negro);
        }}
        .caja-indice h3 {{ font-family: 'Bebas Neue', sans-serif; font-size: 2rem; margin-top: 0; color: var(--negro); }}
        .lista-indice {{ list-style-type: square; color: var(--rojo-base); font-size: 1.2rem; font-weight: bold; }}
        .lista-indice li {{ margin-bottom: 8px; }}
        
        .titulo-categoria {{ 
            font-family: 'Bebas Neue', sans-serif; font-size: 3rem; color: var(--blanco); 
            background: var(--negro); padding: 5px 15px; border-left: 8px solid var(--rojo-sangre); 
            margin: 50px 0 20px 0; 
        }}

        /* GRILLA DE LIBROS */
        .grilla-libros {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; }}
        
        .libro-card {{
            border: 2px solid var(--negro);
            background: var(--blanco);
            cursor: pointer;
            transition: transform 0.2s ease, filter 0.2s ease, box-shadow 0.2s ease;
            position: relative;
        }}
        
        .libro-card:hover {{
            transform: scale(1.03);
            filter: brightness(1.1);
            box-shadow: 0 8px 15px rgba(153, 26, 26, 0.4);
            border-color: var(--rojo-sangre);
        }}
        
        /* MEDIDA DE SEGURIDAD: pointer-events impide arrastrar o clic derecho fácil en la foto */
        .libro-img-ctn {{ width: 100%; aspect-ratio: 2/3; background: var(--gris-ceniza); overflow: hidden; border-bottom: 2px solid var(--negro); }}
        .libro-img {{ width: 100%; height: 100%; object-fit: cover; pointer-events: none; }}
        
        .libro-info {{ padding: 15px; text-align: center; }}
        .libro-titulo {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; margin: 0 0 5px 0; color: var(--rojo-sangre); line-height: 1; }}
        .libro-autor {{ font-weight: bold; margin: 0 0 10px 0; font-size: 1.1rem; color: var(--negro); }}
        .libro-precio {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; background: var(--negro); color: var(--blanco); padding: 5px; margin: 0; display: inline-block; width: 80%; }}

        /* MODAL (VISOR DE EXPEDIENTE) */
        .modal-overlay {{
            display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px);
        }}
        
        .modal-caja {{
            position: relative; width: 90%; max-width: 450px; aspect-ratio: 2/3; 
            border: 4px solid var(--rojo-sangre); box-shadow: 0 0 30px rgba(163, 0, 0, 0.6);
            background-size: cover; background-position: center;
        }}
        
        .modal-oscuridad {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; 
            justify-content: center; padding: 30px; box-sizing: border-box;
        }}
        
        .cerrar-modal {{
            position: absolute; top: 5px; right: 15px; color: var(--rojo-sangre); font-size: 2.5rem; 
            font-weight: bold; cursor: pointer; z-index: 10; font-family: sans-serif; transition: color 0.2s;
        }}
        .cerrar-modal:hover {{ color: var(--blanco); }}
        
        /* EXCEPCIÓN DE SEGURIDAD: Se permite copiar solo los datos del expediente */
        .datos-expediente {{ color: var(--blanco); font-size: 1.2rem; line-height: 1.6; text-align: left; -webkit-user-select: text; user-select: text; }}
        .datos-expediente strong {{ color: var(--rojo-base); font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 1px; }}
        .modal-titulo {{ font-family: 'Bebas Neue', sans-serif; font-size: 3rem; color: var(--blanco); margin: 0 0 20px 0; border-bottom: 2px solid var(--rojo-sangre); line-height: 1; }}
        
        .btn-copiar {{
            margin-top: 25px; width: 100%; padding: 15px; background: var(--rojo-sangre); 
            color: var(--blanco); border: 2px solid var(--negro); font-family: 'Bebas Neue', sans-serif; 
            font-size: 1.6rem; cursor: pointer; transition: background 0.2s, border-color 0.2s;
        }}
        .btn-copiar:hover {{ background: var(--negro); color: var(--rojo-sangre); border-color: var(--rojo-sangre); }}

        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .grilla-libros {{ grid-template-columns: repeat(2, 1fr); gap: 15px; }}
            h1 {{ font-size: 3rem; }}
            .modal-caja {{ width: 95%; aspect-ratio: auto; min-height: 75vh; }}
            .tabs-header {{ flex-direction: column; }}
            .tab-btn {{ border-bottom: 1px solid var(--blanco); }}
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
                <button class="btn-copiar" id="btnCopiar" onclick="copiarAlPortapapeles()">COPIAR DATOS AL PORTAPAPELES</button>
            </div>
        </div>
    </div>

    <script>
        function abrirTab(idTab, elemento) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(idTab).classList.add('active');
            elemento.classList.add('active');
        }}

        const modal = document.getElementById('modalLibro');
        
        function verExpediente(tit, aut, edi, cat, col, pre, año, img) {{
            document.getElementById('modTit').innerText = tit;
            document.getElementById('modAut').innerText = aut;
            document.getElementById('modEdi').innerText = edi;
            document.getElementById('modCat').innerText = cat;
            document.getElementById('modCol').innerText = col;
            document.getElementById('modPre').innerText = pre;
            document.getElementById('modAño').innerText = año;
            document.getElementById('modalFondo').style.backgroundImage = `url('${{img}}')`;
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
            
        conf = data['config']
        
        # 1. Armar Pestañas
        t_btns = ""
        t_cont = ""
        for i, tab in enumerate(data['pestañas']):
            act = "active" if i == 0 else ""
            t_btns += f'<button class="tab-btn {act}" onclick="abrirTab(\'{tab["id"]}\', this)">{tab["titulo"]}</button>'
            t_cont += f'<div id="{tab["id"]}" class="tab-content {act}">{tab["texto"]}</div>'

        # 2. Agrupar libros por categoría
        libros_agrupados = defaultdict(list)
        for lib in data['libros']:
            libros_agrupados[lib['categoria']].append(lib)
            
        # 3. Construir Índice y Secciones
        indice_html = ""
        secciones_html = ""
        
        for cat in sorted(libros_agrupados.keys()):
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n')
            
            # Sumar al índice
            indice_html += f'<li><a href="#{cat_id}">{cat}</a></li>'
            
            # Armar la sección de la grilla
            secciones_html += f'<h2 class="titulo-categoria" id="{cat_id}">{cat}</h2>'
            secciones_html += '<div class="grilla-libros">'
            
            for lib in libros_agrupados[cat]:
                # Escapar comillas simples por si un título las tiene
                tit = lib['titulo'].replace("'", "\\'")
                aut = lib['autor'].replace("'", "\\'")
                edi = lib['editorial'].replace("'", "\\'")
                cat_txt = lib['categoria'].replace("'", "\\'")
                col = lib['coleccion'].replace("'", "\\'")
                onClick_js = f"verExpediente('{tit}', '{aut}', '{edi}', '{cat_txt}', '{col}', '{lib['precio']}', '{lib['año']}', '{lib['imagen']}')"
                
                secciones_html += f"""
                <div class="libro-card" onclick="{onClick_js}">
                    <div class="libro-img-ctn">
                        <img src="{lib['imagen']}" alt="{lib['titulo']}" class="libro-img" onerror="this.style.display='none'">
                    </div>
                    <div class="libro-info">
                        <h3 class="libro-titulo">{lib['titulo']}</h3>
                        <p class="libro-autor">{lib['autor']}</p>
                        <p class="libro-precio">{lib['precio']}</p>
                    </div>
                </div>
                """
            secciones_html += '</div>'

        # Renderizar final
        html_final = HTML_TEMPLATE.format(
            titulo_head=conf['titulo'],
            titulo_pag=conf['titulo'],
            sub_pag=conf['subtitulo'],
            bajada_pag=conf['bajada'],
            tabs_botones=t_btns,
            tabs_contenido=t_cont,
            indice_html=indice_html,
            secciones_html=secciones_html
        )
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_final)
            
        print(">>> Catálogo de Contrabando generado exitosamente.")
        
    except Exception as e:
        print(f">>> ERROR TÉCNICO EN EL TACURÚ (Catálogo): {e}")

if __name__ == "__main__":
    generar_catalogo()
