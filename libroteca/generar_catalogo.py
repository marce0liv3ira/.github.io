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
            --rojo-base: #991A1A; --rojo-sangre: #A30000; --rojo-oscuro: #660000;
            --gris-ceniza: #8E7171; --fondo-hueso: #FAF6ED; --blanco: #FFFFFF; --negro: #000000;
        }}
        
        body {{ 
            background-color: var(--fondo-hueso) !important; color: #1a1a1a !important; 
            font-family: 'Inter', sans-serif; margin: 0; padding: 20px; 
            -webkit-user-select: none; user-select: none; 
            display: flex; flex-direction: column; min-height: 100vh;
        }}
        
        a {{ color: var(--rojo-sangre) !important; text-decoration: none; transition: 0.2s; }}
        a:hover {{ color: #D62828 !important; text-shadow: 0 0 5px rgba(163, 0, 0, 0.4); }}
        
        .contenedor {{ flex: 1; max-width: 1200px; margin: 0 auto; width: 100%; display: flow-root; }}
        
        header {{ 
            border-bottom: 1px solid var(--rojo-sangre); padding: 40px 20px; margin-bottom: 30px; border-radius: 8px;
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8);
            background-image: linear-gradient(rgba(250, 246, 237, 0.45), rgba(250, 246, 237, 0.55)), url('img/logolibro.png');
            background-size: contain; background-position: center; background-repeat: no-repeat;
            display: flex; flex-direction: column; gap: 20px;
        }}

        .header-superior {{ display: flex; justify-content: space-between; align-items: center; width: 100%; }}
        .header-titulos {{ text-align: left; }}

        /* AJUSTE 2: TÍTULOS MONUMENTALES */
        h1 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 6.5rem !important; color: var(--rojo-sangre) !important; margin: 0; line-height: 0.85 !important; }}
        h2 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 3.5rem !important; color: var(--negro) !important; margin: 0; }}

        /* AJUSTE 4: LINK EN BLOQUE AUTOR */
        .bloque-autor {{ display: flex; align-items: center; gap: 15px; background: rgba(163, 0, 0, 0.05); padding: 10px 15px; border-radius: 50px 10px 10px 50px; border: 1px solid rgba(163, 0, 0, 0.2); transition: 0.3s; cursor: pointer; }}
        .bloque-autor:hover {{ background: rgba(163, 0, 0, 0.1); transform: translateX(5px); }}
        .foto-autor {{ width: 75px; height: 75px; border-radius: 50%; border: 2px solid var(--rojo-sangre); object-fit: cover; box-shadow: 0 0 10px rgba(163, 0, 0, 0.3); }}
        .nombre-autor {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; color: var(--negro); letter-spacing: 1px; text-transform: uppercase; }}

        .bajada {{ 
            font-size: 1.15rem; font-weight: 500; color: var(--negro); 
            background: rgba(255, 255, 255, 0.35); padding: 20px; border-radius: 4px;
            text-align: left; max-width: 100%; line-height: 1.6; border-left: 4px solid var(--rojo-sangre);
            backdrop-filter: blur(2px);
        }}

        .caja-menu {{ border: 1px solid var(--rojo-sangre); margin-bottom: 40px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 12px rgba(163, 0, 0, 0.25); }}
        .tabs-header {{ display: flex; border-bottom: 1px solid var(--rojo-sangre); background: var(--negro); }}
        .tab-btn {{ flex: 1; padding: 14px; cursor: pointer; font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: var(--blanco); background: transparent; border: none; transition: 0.3s; letter-spacing: 1px; }}
        .tab-btn.active, .tab-btn:hover {{ background: var(--rojo-sangre); }}
        .tab-content {{ padding: 25px; display: none; font-size: 1.15rem; line-height: 1.6; }}
        .tab-content.active {{ display: block; }}
        
        .lista-indice {{ 
            list-style-type: none; padding: 0; margin: 0; display: flex; flex-direction: column; 
            flex-wrap: wrap; align-content: flex-start; gap: 8px 30px; max-height: 150px; 
        }}
        .lista-indice li {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 1px; }}

        .titulo-categoria {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 3.5rem !important; color: var(--blanco) !important; background: var(--negro) !important; padding: 10px 20px !important; border-left: 6px solid var(--rojo-sangre) !important; margin: 60px 0 25px 0 !important; text-transform: uppercase !important; border-radius: 4px; }}
        .grilla-tacuru {{ display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 20px !important; margin: 2rem 0 !important; }}
        
        .tarjeta-expediente {{ position: relative !important; aspect-ratio: 1 / 1 !important; background-color: #000 !important; border: 1px solid var(--rojo-oscuro) !important; border-radius: 8px !important; overflow: hidden; transition: 0.4s; cursor: pointer; }}
        .tarjeta-expediente:hover {{ transform: scale(1.03) !important; border-color: var(--rojo-sangre) !important; box-shadow: 0 0 25px rgba(163, 0, 0, 0.65); }}
        .tarjeta-imagen-wrapper img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(100%); opacity: 0.6; transition: 0.5s; }}
        .tarjeta-expediente:hover img {{ filter: grayscale(0%); opacity: 1; }}
        
        .tarjeta-expediente h3 {{ 
            font-family: 'Bebas Neue', sans-serif !important; color: #fff !important; font-size: 1.7rem !important; 
            margin: 0 0 6px 0; line-height: 1 !important; text-shadow: 2px 2px 4px #000; width: 100%; 
            overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; 
        }}

        .modal-overlay {{ display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px); }}
        .modal-caja {{ position: relative; width: 90%; max-width: 450px; aspect-ratio: 2/3; border: 2px solid var(--rojo-sangre); border-radius: 8px; background-size: cover; background-position: center; overflow: hidden; box-shadow: 0 0 40px rgba(0,0,0,0.6); }}
        .modal-oscuridad {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.75); display: flex; flex-direction: column; justify-content: center; padding: 35px; box-sizing: border-box; }}
        .modal-titulo {{ font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; color: var(--blanco); margin: 0 0 25px 0; border-bottom: 2px solid var(--rojo-sangre); padding-bottom: 12px; line-height: 1.1; }}
        .datos-expediente {{ color: var(--blanco); font-size: 1.2rem; line-height: 1.9; text-align: left; }}
        .datos-expediente strong {{ color: var(--rojo-sangre) !important; font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 1px; }}
        
        /* AJUSTE 1: TRIÁNGULO CENTRADO Y BOTÓN SUBIR */
        #btn-ascenso {{ 
            position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: rgba(0, 0, 0, 0.85); 
            color: var(--blanco); border: 2px solid var(--rojo-sangre); border-radius: 50%; font-size: 1.8rem; 
            cursor: pointer; display: none; justify-content: center; align-items: center; z-index: 1000; 
            transition: 0.3s; padding-bottom: 6px; /* Compensación visual */
        }}
        #btn-ascenso:hover {{ background: var(--rojo-sangre); transform: scale(1.1) translateY(-5px); box-shadow: 0 0 20px var(--rojo-sangre); }}

        footer {{ margin-top: 80px; background-color: var(--negro); border-top: 4px solid var(--rojo-sangre); width: 100%; padding: 40px 20px; }}

        @media (max-width: 600px) {{ 
            /* AJUSTE 3: LOGO MÓVIL CHICO Y ARRIBA */
            header {{ 
                background-size: 55% !important; 
                background-position: center 20px !important; 
                padding: 85px 15px 35px 15px !important; 
            }}
            /* AJUSTE 2: TÍTULOS MÓVIL */
            h1 {{ font-size: 4.8rem !important; }}
            h2 {{ font-size: 2.4rem !important; }}
            
            /* AJUSTE FOOTER: AIRE EN MÓVILES */
            footer {{ padding: 70px 20px !important; }}
            .footer-bunker p {{ margin-bottom: 25px !important; }}

            .grilla-tacuru {{ grid-template-columns: repeat(2, 1fr) !important; gap: 12px !important; }} 
            .lista-indice {{ max-height: none !important; flex-direction: row !important; flex-wrap: wrap !important; }}
            .lista-indice li {{ width: 45%; margin-bottom: 8px; }}

            /* AJUSTE 5: DESBORDE MODAL MÓVIL */
            .modal-caja {{ aspect-ratio: auto !important; min-height: 75vh; max-height: 92vh; overflow-y: auto; }}
            .modal-oscuridad {{ justify-content: flex-start !important; padding-top: 70px !important; }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <header>
            <div class="header-superior">
                <div class="header-titulos">
                    <h1>{titulo_pag}</h1>
                    <h2>{sub_pag}</h2>
                </div>
                <a href="https://hormigue.ar/" target="_blank">
                    <div class="bloque-autor">
                        <img src="https://hormigue.ar/media/website/marcef.webp" class="foto-autor" alt="marce oliveira">
                        <span class="nombre-autor">marce oliveira</span>
                    </div>
                </a>
            </div>
            <div class="bajada">{bajada_pag}</div>
        </header>

        <div class="caja-menu" id="menu-selector">
            <div class="tabs-header">{tabs_botones}</div>
            <div class="tabs-cuerpo">{tabs_contenido}</div>
        </div>

        {secciones_html}
    </div>

    <div id="modalLibro" class="modal-overlay" onclick="cerrarModal(event)">
        <div class="modal-caja" id="modalFondo">
            <span style="position:absolute; top:15px; right:20px; color:white; font-size:3.5rem; cursor:pointer; z-index:100; line-height:1;" onclick="cerrarModalFuerza()">&times;</span>
            <div class="modal-oscuridad">
                <div class="modal-titulo" id="modTit"></div>
                <div class="datos-expediente">
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
        <div class="footer-bunker" style="text-align: center; color: #ffffff;">
            <p style="margin-bottom: 12px;">
                <strong style="font-family: 'Almarai', sans-serif; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 0.9px;">
                    <a href="https://hormigue.ar/" style="color: white !important;">HORMIGUE.AR</a>
                </strong>
                <a href="https://hormigue.ar/">
                    <img style="height: 2.2rem; vertical-align: middle; margin: 0 8px;" src="https://pica.hormigue.ar/hormiMG/icono%20hormi.png" alt="H">
                </a>
                <span><a href="https://hormigue.ar/" style="color: white !important;">Libroteca</a></span>
            </p>
            <p style="font-family: 'Arial Narrow', sans-serif; font-size: 0.9rem; opacity: 0.8;">conocé el sitio creado con pocos recursos técnicos, económicos e intelectuales</p>
        </div>
    </footer>

    <script>
        function abrirTab(idTab, elemento) {{
            var contenidos = document.querySelectorAll('.tab-content');
            contenidos.forEach(c => c.classList.remove('active'));
            var botones = document.querySelectorAll('.tab-btn');
            botones.forEach(b => b.classList.remove('active'));
            document.getElementById(idTab).classList.add('active');
            elemento.classList.add('active');
        }}

        function abrirExpediente(elemento) {{
            document.getElementById('modTit').innerText = elemento.getAttribute('data-tit');
            document.getElementById('modAut').innerText = elemento.getAttribute('data-aut');
            document.getElementById('modEdi').innerText = elemento.getAttribute('data-edi');
            document.getElementById('modAño').innerText = elemento.getAttribute('data-ano');
            document.getElementById('modEst').innerText = elemento.getAttribute('data-est');
            document.getElementById('modPre').innerText = elemento.getAttribute('data-pre');
            document.getElementById('modalFondo').style.backgroundImage = `url('${{elemento.getAttribute('data-img')}}')`;
            document.getElementById('modalLibro').style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Sin scroll de fondo
        }}

        // AJUSTE 1: CIERRE TÁCTICO
        function cerrarModal(e) {{
            if (e.target.id === 'modalLibro') {{
                cerrarModalFuerza();
            }}
        }}
        function cerrarModalFuerza() {{
            document.getElementById('modalLibro').style.display = 'none';
            document.body.style.overflow = 'auto';
        }}

        function copiarAlPortapapeles() {{
            const t = document.getElementById('modTit').innerText;
            const a = document.getElementById('modAut').innerText;
            const txt = `Quiero este libro: "${{t}}" de "${{a}}".`;
            navigator.clipboard.writeText(txt).then(() => {{
                document.getElementById('btnCopiar').innerText = '¡COPIADO!';
                setTimeout(() => {{ document.getElementById('btnCopiar').innerText = 'COPIAR'; }}, 2000);
            }});
        }}

        window.onscroll = function() {{
            document.getElementById("btn-ascenso").style.display = (window.scrollY > 500) ? "flex" : "none";
        }};

        function volverArriba() {{ window.scrollTo({{top: 0, behavior: 'smooth'}}); }}
    </script>
</body>
</html>
"""

def normalizar_categoria(cat_cruda):
    c = cat_cruda.lower()
    if 'ensayo' in c: return 'Ensayo'
    if 'historia' in c: return 'Historia'
    if 'polític' in c or 'politic' in c: return 'Política'
    if 'comunicaci' in c: return 'Comunicación'
    if 'filosof' in c: return 'Filosofía'
    if 'narrativa' in c or 'literatura' in c or 'crónica' in c: return 'Literatura'
    if 'sociolog' in c: return 'Sociología'
    if 'psicolog' in c or 'psiquiatr' in c or 'psicoan' in c: return 'Psico'
    if 'ciencia' in c: return 'Divulgación Dura'
    if 'derechos humanos' in c: return 'Varios'
    return cat_cruda.split('/')[0].strip().title()

def orden_mafioso(cat):
    return 'ZZZZZZ' if cat.upper() == 'VARIOS' else cat

def generar_catalogo():
    try:
        ruta_json = os.path.join(os.path.dirname(__file__), 'catalogo.json')
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        bajada_forzada = (
            "Libros usados listos para seguir circulando.<br>"
            "Esta es una venta pensada para lectoras y lectores de la zona. Las ofertas se hacen por tandas. Voy cargando títulos a medida que avanzo con el inventario de mi biblioteca, por estantes.<br>"
            "Todos los libros están en muy buen estado; algunos, incluso, son nuevos. Fueron cuidados como corresponde, como mucho, alguna marca de lápiz. "
            "Los pocos ejemplares deteriorados lo están por razones nobles: paso del tiempo, ferias, reventas. Los títulos descatalogados, la resistencia."
        )
        
        pestañas_forzadas = [
            {"id": "tab1", "titulo": "QUÉ", "texto": "Las categorías son orientativas. Algunos libros encajan en varias y otros en ninguna. Revisá todo, nunca confíes en las clasificaciones."},
            {"id": "tab2", "titulo": "CÓMO", "texto": "Revisá, picá el libro que te interese y copiá los datos. Podés usarlos para enviármelos, comparar precios o buscar reseñas en la web. Si no podés contactarme, este sitio no es para vos.<br>Si podés contactarme, coordinamos detalles: estado del libro, forma de pago y entrega. El pago es en pesos argentinos, por transferencia o efectivo. No acepto trueques, monedas extranjeras ni pagos en especies (por más seductora que sea la oferta)."},
            {"id": "tab3", "titulo": "QUIÉNES", "texto": "Este sitio está pensado para lectoras y lectores cercanos. Posadas y Candelaria funcionan como referencia, pero lo central es el contacto: si podés ubicarme (directa o indirectamente), podés comprar. Si no, este sitio no es para vos."},
            {"id": "tab4", "titulo": "ENTREGA", "texto": "Las compras iguales o superiores a $25.000 tienen envío gratuito a domicilio dentro de Posadas y Candelaria. Cada entrega o retiro se coordina; fecha, lugar y horario se acuerdan entre ambas partes lectoras."}
        ]
        
        libros_agrupados = defaultdict(list)
        for lib in data.get('libros', []):
            libros_agrupados[normalizar_categoria(lib.get('categoria', 'Varios'))].append(lib)
            
        cats_ordenadas = sorted(libros_agrupados.keys(), key=orden_mafioso)

        indice_html = '<ul class="lista-indice">'
        for cat in cats_ordenadas:
            c_id = cat.lower().replace(' ', '-')
            indice_html += f'<li><a href="#{c_id}">{cat.upper()}</a></li>'
        indice_html += '</ul>'

        t_btns, t_cont = "", ""
        for i, tab in enumerate(pestañas_forzadas):
            act = "active" if i == 0 else ""
            txt = f'<div class="texto-pestaña">{tab["texto"]}</div><div class="caja-indice-interna">{indice_html}</div>' if tab["id"] == "tab1" else tab["texto"]
            t_btns += f'<button class="tab-btn {act}" onclick="abrirTab(\'{tab["id"]}\', this)">{tab["titulo"]}</button>'
            t_cont += f'<div id="{tab["id"]}" class="tab-content {act}">{txt}</div>'

        secciones_html = ""
        for cat in cats_ordenadas:
            c_id = cat.lower().replace(' ', '-')
            secciones_html += f'<h2 class="titulo-categoria" id="{c_id}">{cat.upper()}</h2><div class="grilla-tacuru">'
            for lib in libros_agrupados[cat]:
                secciones_html += f"""
                <div class="tarjeta-expediente" data-tit="{lib.get('titulo','')}" data-aut="{lib.get('autor','')}" data-edi="{lib.get('editorial','')}" data-ano="{lib.get('año','')}" data-est="{lib.get('estado','Muy bueno')}" data-pre="{lib.get('precio','Consultar')}" data-img="{lib.get('imagen','')}" onclick="abrirExpediente(this)">
                    <div class="tarjeta-imagen-wrapper"><img src="{lib.get('imagen','')}" onerror="this.style.display='none'"></div>
                    <div class="enlace-tarjeta"><h3>{lib.get('titulo','')}</h3><p>{lib.get('autor','')}</p></div>
                </div>"""
            secciones_html += '</div>'

        html_final = HTML_TEMPLATE.format(
            titulo_head="Libroteca", titulo_pag="LIBROTECA", sub_pag="ESTANTE DE ABAJO",
            bajada_pag=bajada_forzada, tabs_botones=t_btns, tabs_contenido=t_cont, secciones_html=secciones_html
        )
        
        with open(RUTA_HTML_DESTINO, 'w', encoding='utf-8') as f:
            f.write(html_final)
        print(">>> Catálogo sellado. Perfil de autor inyectado.")
        
    except Exception as e: print(f">>> ERROR EN LA MAQUINARIA: {e}")

if __name__ == "__main__": generar_catalogo()
