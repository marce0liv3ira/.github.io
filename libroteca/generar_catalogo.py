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
    
    <link rel="icon" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/book-half.svg" type="image/svg+xml">
    
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
        
        header {{ 
            text-align: center; 
            border-bottom: 1px solid var(--rojo-sangre); 
            padding: 50px 20px; 
            margin-bottom: 30px; 
            border-radius: 8px;
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8);
            background-image: linear-gradient(rgba(250, 246, 237, 0.85), rgba(250, 246, 237, 0.92)), url('img/logolibro.png');
            background-size: contain; 
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
            font-size: 1.1rem; font-weight: bold; color: var(--negro); 
            font-family: 'Inter', sans-serif; position: relative; z-index: 2; 
            background: rgba(250, 246, 237, 0.85);
            display: inline-block; padding: 15px 25px; border-radius: 4px;
            text-align: left; max-width: 800px; margin: 0 auto; line-height: 1.5;
            border: 1px solid var(--rojo-sangre);
        }}

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
        .tab-content {{ padding: 20px; display: none; font-size: 1.1rem; font-family: 'Inter', sans-serif; line-height: 1.5; }}
        .tab-content.active {{ display: block; }}

        .caja-indice-interna {{
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px dashed var(--rojo-sangre);
        }}
        
        /* ÍNDICE: ALTURA AMPLIADA PARA EVITAR EL SCROLL VERTICAL */
        .lista-indice {{ 
            list-style-type: none; 
            padding: 0; 
            margin: 0;
            max-height: 220px; 
            display: flex;
            flex-direction: column;
            flex-wrap: wrap;
            align-content: flex-start;
            gap: 6px 15px; 
            overflow: hidden; 
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
            color: var(--blanco); font-size: 1.15rem; line-height: 1.8; text-align: left; 
            -webkit-user-select: text; user-select: text; font-family: 'Inter', sans-serif;
            text-shadow: 0 0 8px #000, 0 0 15px #000; 
        }}
        .datos-expediente strong {{ color: var(--rojo-base); font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 1px; }}
        
        .modal-titulo {{ 
            font-family: 'Bebas Neue', sans-serif; font-size: 2.6rem; color: var(--blanco); 
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
            font-size: 1.5rem;
            cursor: pointer;
            display: none; 
            justify-content: center;
            align-items: center;
            z-index: 1000;
            box-shadow: 0 0 15px rgba(163, 0, 0, 0.5);
            transition: all 0.3s ease;
            backdrop-filter: blur(4px);
            text-decoration: none;
            padding-bottom: 2px;
        }}
        #btn-ascenso:hover {{
            transform: scale(1.1);
            background: var(--rojo-sangre);
            box-shadow: 0 0 25px rgba(163, 0, 0, 0.8);
        }}

        footer {{
            margin-top: 60px;
            background-color: var(--negro);
            border-top: 4px solid var(--rojo-sangre);
            box-shadow: 0 -4px 15px rgba(163, 0, 0, 0.3);
            width: 100%;
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
            #btn-ascenso {{ bottom: 20px; right: 20px; width: 45px; height: 45px; font-size: 1.2rem; }}
            .enlace-tarjeta {{ padding: 10px !important; }}
            .tarjeta-expediente h3 {{ font-size: 1.15rem !important; margin-bottom: 4px !important; }}
            .tarjeta-expediente p {{ font-size: 0.85rem !important; }}
            .bajada {{ font-size: 1rem; padding: 10px 15px; }}
            
            /* TÁCTICA PARA MÓVILES: 2 COLUMNAS ILIMITADAS VERTICALMENTE */
            .lista-indice {{ 
                max-height: none !important; 
                flex-direction: row !important; 
            }}
            .lista-indice li {{ 
                width: 48%; 
                box-sizing: border-box; 
            }}
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
                    <strong>AÑO:</strong> <span id="modAño"></span><br>
                    <strong>ESTADO:</strong> <span id="modEst"></span><br>
                    <strong>PRECIO:</strong> <span id="modPre"></span>
                </div>
                <button class="btn-copiar" id="btnCopiar" onclick="copiarAlPortapapeles()">COPIAR</button>
            </div>
        </div>
    </div>

    <div id="btn-ascenso" onclick="volverArriba()" title="Volver a arriba">&#9650;</div>

    <footer>
        <div class="footer-bunker" style="text-align: center; vertical-align: middle; width: 100%; color: #ffffff; line-height: 1.6; padding: 25px 0; display: block;">
            <p style="margin-bottom: 8px; text-align: center !important; vertical-align: middle;">
                <strong class="title-site-m" style="font-family: 'Almarai', sans-serif; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.8px; text-shadow: 0 0 4px #000, 0 0 8px #000, 0 0 12px #000, 0 0 16px #000, 0 0 20px #000 !important;"> 
                    <a href="https://hormigue.ar/" style="color: #fff !important; text-decoration: none;">HORMIGUE.AR</a> 
                </strong> 
                <span class="no-break" style="white-space: nowrap !important; display: inline-block;"> 
                    <a href="https://hormigue.ar/" style="text-decoration: none;">
                        <img style="height: 2rem; width: auto; vertical-align: middle; margin-right: 0.3em; filter: drop-shadow(0 0 4px #000) drop-shadow(0 0 8px #000) drop-shadow(0 0 12px #000);" src="https://pica.hormigue.ar/hormiMG/icono%20hormi.png" alt="Ícono Hormi"> 
                    </a>
                </span> 
                <span style="text-shadow: 0 0 4px #000, 0 0 8px #000, 0 0 12px #000, 0 0 16px #000, 0 0 20px #000 !important;"> 
                    <span style="display: inline-block; transform: scaleX(-1);">C</span>onfianza
                </span>
            </p>
            <p class="sub-text-m" style="font-family: 'Arial Narrow', Arial, sans-serif; font-weight: 500; font-size: 0.8rem; color: #ffffff; margin: 0 auto; max-width: 90%; text-shadow: 0 0 5px #000, 0 0 9px #000; text-align: center; vertical-align: middle;">
                conocé el sitio creado con pocos recursos técnicos,<br>económicos e intelectuales
            </p>
        </div>
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
            document.getElementById('modEst').innerText = elemento.getAttribute('data-est');
            
            document.getElementById('modPre').innerText = elemento.getAttribute('data-pre');
            
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
    if 'narrativa' in c or 'literatura' in c or 'crónica' in c or 'cronica' in c:
        return 'Literatura'
    if 'sociolog' in c:
        return 'Sociología'
    if 'psicolog' in c or 'psiquiatr' in c or 'psicoan' in c:
        return 'Psico'
    if 'ciencia' in c:
        return 'Divulgación Dura'
    if 'derechos humanos' in c:
        return 'Varios'
        
    return cat_cruda.split('/')[0].strip().title()

def orden_mafioso(cat):
    if cat.upper() == 'VARIOS':
        return 'ZZZZZZ'
    return cat

def generar_catalogo():
    try:
        base_path = os.path.dirname(__file__)
        ruta_json = os.path.join(base_path, 'catalogo.json')
        
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        bajada_forzada = (
            "Libros usados listos para seguir circulando.<br>"
            "Esta es una venta pensada para lectoras y lectores de la zona. Las ofertas se hacen por tandas. Voy cargando títulos a medida que avanzo con el inventario de mi biblioteca, por estantes.<br>"
            "Todos los libros están en muy buen estado; algunos, incluso, son nuevos. Fueron cuidados como corresponde, como mucho, alguna marca de lápiz. "
            "Los pocos ejemplares deteriorados lo están por razones nobles: paso del tiempo, ferias, reventas. Los títulos descatalogados, la resistencia."
        )
        
        pestañas_forzadas = [
            {"id": "tab1", "titulo": "CONTENIDO", "texto": "Las categorías son orientativas. Algunos libros encajan en varias y otros en ninguna. Revisá todo, nunca confíes en las clasificaciones."},
            {"id": "tab2", "titulo": "CÓMO", "texto": "Revisá, picá lo que te interese y copiá los datos del libro. Podés usarlos para enviarme un mensaje, comparar precios o buscar reseñas en la web. Si no podés contactarme, este sitio no es para vos.<br>Si podés contactarme, coordinamos detalles: estado del libro, forma de pago y entrega. El pago es en pesos argentinos, por transferencia o efectivo. No acepto trueques, monedas extranjeras ni pagos en especies (por más seductora que sea la oferta)."},
            {"id": "tab3", "titulo": "QUIÉNES", "texto": "Este sitio está pensado para lectoras y lectores cercanos. Posadas y Candelaria funcionan como referencia, pero lo central es el contacto: si podés ubicarme (directa o indirectamente), podés comprar. Si no, este sitio no es para vos."},
            {"id": "tab4", "titulo": "ENTREGA", "texto": "Las compras iguales o superiores a $25.000 tienen envío gratuito a domicilio dentro de Posadas y Candelaria. Cada entrega o retiro se coordina; fecha, lugar y horario se acuerdan entre ambas partes lectoras."}
        ]
        
        libros_agrupados = defaultdict(list)
        for lib in data.get('libros', []):
            cat_cruda = lib.get('categoria', 'Sin Categoría')
            cat_maestra = normalizar_categoria(cat_cruda)
            libros_agrupados[cat_maestra].append(lib)
            
        categorias_ordenadas = sorted(libros_agrupados.keys(), key=orden_mafioso)

        indice_html = '<ul class="lista-indice">'
        for cat in categorias_ordenadas:
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n').replace('ó','o').replace('í','i').replace('á','a')
            indice_html += f'<li><a href="#{cat_id}">{cat.upper()}</a></li>'
        indice_html += '</ul>'

        t_btns = ""
        t_cont = ""
        
        for i, tab in enumerate(pestañas_forzadas):
            act = "active" if i == 0 else ""
            t_id = tab.get("id")
            t_tit = tab.get("titulo")
            t_txt = tab.get("texto")
            
            if t_tit.upper() == "CONTENIDO" or t_id == "tab1":
                t_txt = f'<div class="texto-pestaña">{t_txt}</div><div class="caja-indice-interna">{indice_html}</div>'
            
            t_btns += f'<button class="tab-btn {act}" onclick="abrirTab(\'{t_id}\', this)">{t_tit}</button>'
            t_cont += f'<div id="{t_id}" class="tab-content {act}">{t_txt}</div>'

        secciones_html = ""
        for cat in categorias_ordenadas:
            cat_id = cat.lower().replace(' ', '-').replace('ñ', 'n').replace('ó','o').replace('í','i').replace('á','a')
            
            secciones_html += f'<h2 class="titulo-categoria" id="{cat_id}">{cat.upper()}</h2>'
            secciones_html += '<div class="grilla-tacuru">'
            
            for lib in libros_agrupados[cat]:
                tit = lib.get('titulo', 'Sin Título').replace('"', '&quot;')
                aut = lib.get('autor', 'Desconocido').replace('"', '&quot;')
                edi = lib.get('editorial', '-').replace('"', '&quot;')
                ano = lib.get('año', '-').replace('"', '&quot;')
                img = lib.get('imagen', '').replace('"', '&quot;')
                est = lib.get('estado', 'Muy bueno').replace('"', '&quot;')
                pre = lib.get('precio', 'Consultar').replace('"', '&quot;')
                
                secciones_html += f"""
                <div class="tarjeta-expediente" 
                     data-tit="{tit}" 
                     data-aut="{aut}" 
                     data-edi="{edi}" 
                     data-ano="{ano}" 
                     data-est="{est}"
                     data-pre="{pre}"
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
            titulo_head="Libroteca",
            titulo_pag="LIBROTECA",
            sub_pag="ESTANTE DE ABAJO",
            bajada_pag=bajada_forzada,
            tabs_botones=t_btns,
            tabs_contenido=t_cont,
            secciones_html=secciones_html
        )
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_final)
            
        print(">>> Catálogo sellado. Icono de pestaña cargado y regla vertical suprimida.")
        
    except Exception as e:
        print(f">>> ERROR TÉCNICO EN EL TACURÚ (Catálogo): {e}")

if __name__ == "__main__":
    generar_catalogo()
