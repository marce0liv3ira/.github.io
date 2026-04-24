import json
import os
from collections import defaultdict

# --- COORDENADAS DEL TACURÚ ---
RUTA_JSON = os.path.join(os.path.dirname(__file__), 'catalogo.json')
RUTA_HTML_DESTINO = os.path.join(os.path.dirname(__file__), 'index.html')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo_head}}</title>
    
    <link rel="icon" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/book-half.svg" type="image/svg+xml">
    
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
        
        header {{ 
            border-bottom: 1px solid var(--rojo-sangre); padding: 40px 20px; margin-bottom: 30px; border-radius: 8px;
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8);
            background-image: linear-gradient(rgba(250, 246, 237, 0.45), rgba(250, 246, 237, 0.55)), url('img/logolibro.png');
            background-size: contain; background-position: center; background-repeat: no-repeat;
            display: flex; flex-direction: column; gap: 20px;
        }}

        .header-superior {{ display: flex; justify-content: space-between; align-items: center; width: 100%; }}
        
        /* AJUSTE 2: TÍTULOS MONUMENTALES */
        h1 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 6rem !important; color: var(--rojo-sangre) !important; margin: 0; line-height: 0.9 !important; }}
        h2 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; color: var(--negro) !important; margin: 0; }}

        /* AJUSTE 4: LINK EN BLOQUE AUTOR */
        .bloque-autor {{ display: flex; align-items: center; gap: 15px; background: rgba(163, 0, 0, 0.05); padding: 10px 15px; border-radius: 50px 10px 10px 50px; border: 1px solid rgba(163, 0, 0, 0.2); transition: 0.3s; }}
        .bloque-autor:hover {{ background: rgba(163, 0, 0, 0.1); transform: translateX(5px); }}
        .foto-autor {{ width: 70px; height: 70px; border-radius: 50%; border: 2px solid var(--rojo-sangre); object-fit: cover; box-shadow: 0 0 10px rgba(163, 0, 0, 0.3); }}
        .nombre-autor {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: var(--negro); text-transform: uppercase; }}

        .bajada {{ 
            font-size: 1.1rem; font-weight: 500; background: rgba(255, 255, 255, 0.35); padding: 20px; 
            border-radius: 4px; border-left: 4px solid var(--rojo-sangre); backdrop-filter: blur(2px); line-height: 1.6;
        }}

        .caja-menu {{ border: 1px solid var(--rojo-sangre); margin-bottom: 40px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 12px rgba(163, 0, 0, 0.25); }}
        .tabs-header {{ display: flex; border-bottom: 1px solid var(--rojo-sangre); background: var(--negro); }}
        .tab-btn {{ flex: 1; padding: 12px; cursor: pointer; font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: var(--blanco); background: transparent; border: none; transition: 0.3s; }}
        .tab-btn.active {{ background: var(--rojo-sangre); }}
        .tab-content {{ padding: 25px; display: none; line-height: 1.6; }}
        .tab-content.active {{ display: block; }}
        
        /* AJUSTE 1: ÍNDICE COLUMNAS */
        .lista-indice {{ 
            list-style: none; padding: 0; margin: 20px 0 0 0; display: flex; flex-direction: column; 
            flex-wrap: wrap; align-content: flex-start; gap: 8px 30px; max-height: 160px; 
        }}
        .lista-indice li {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; }}
        .lista-indice li a {{ color: var(--rojo-sangre) !important; }}

        .grilla-tacuru {{ display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 15px !important; margin: 2rem 0 !important; }}
        .tarjeta-expediente {{ position: relative !important; aspect-ratio: 1 / 1 !important; background-color: #000 !important; border: 1px solid var(--rojo-oscuro) !important; border-radius: 8px !important; overflow: hidden; cursor: pointer; transition: 0.4s; }}
        .tarjeta-expediente:hover {{ transform: scale(1.03); border-color: var(--rojo-sangre); box-shadow: 0 0 25px rgba(163, 0, 0, 0.65); }}
        .tarjeta-imagen-wrapper img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(100%); opacity: 0.6; transition: 0.5s; }}
        .tarjeta-expediente:hover img {{ filter: grayscale(0%); opacity: 1; }}
        
        .enlace-tarjeta {{ display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; padding: 15px; position: relative; z-index: 10; text-align: center; color: white; }}
        .tarjeta-expediente h3 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 1.6rem !important; line-height: 1 !important; text-shadow: 2px 2px 4px #000; -webkit-line-clamp: 3; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; }}

        /* AJUSTE 1 & 5: MODAL CIERRE Y DESBORDE */
        .modal-overlay {{ display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px); }}
        .modal-caja {{ position: relative; width: 90%; max-width: 450px; aspect-ratio: 2/3; border: 2px solid var(--rojo-sangre); border-radius: 8px; background-size: cover; background-position: center; overflow: hidden; }}
        .modal-oscuridad {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); display: flex; flex-direction: column; justify-content: center; padding: 30px; box-sizing: border-box; color: white; }}
        
        /* AJUSTE 5: ROJO SANGRE SECA */
        .datos-expediente strong {{ color: var(--rojo-sangre) !important; font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; }}
        
        /* AJUSTE: BOTÓN SUBIR CENTRADO */
        #btn-ascenso {{ 
            position: fixed; bottom: 30px; right: 30px; width: 55px; height: 55px; background: rgba(0, 0, 0, 0.8); 
            color: var(--blanco); border: 2px solid var(--rojo-sangre); border-radius: 50%; font-size: 1.5rem; 
            display: none; justify-content: center; align-items: center; transition: 0.3s; z-index: 1000; cursor: pointer;
            line-height: 1; padding-bottom: 5px;
        }}
        #btn-ascenso:hover {{ background: var(--rojo-sangre); transform: scale(1.1) translateY(-5px); }}

        /* AJUSTE: AIRE EN FOOTER */
        footer {{ margin-top: 60px; background-color: var(--negro); border-top: 4px solid var(--rojo-sangre); width: 100%; text-align: center; color: white; padding: 40px 20px; }}
        
        @media (max-width: 600px) {{ 
            /* AJUSTE 3: LOGO MÓVIL CHICO Y ARRIBA */
            header {{ background-size: 60% !important; background-position: center 15px !important; padding: 70px 15px 30px 15px !important; }}
            h1 {{ font-size: 4.5rem !important; }}
            h2 {{ font-size: 2.2rem !important; }}
            .grilla-tacuru {{ grid-template-columns: repeat(2, 1fr) !important; }} 
            .lista-indice {{ max-height: none !important; flex-direction: row !important; flex-wrap: wrap !important; }} 
            .lista-indice li {{ width: 45%; }}
            .modal-caja {{ aspect-ratio: auto !important; min-height: 70vh; max-height: 90vh; overflow-y: auto; }}
            .modal-oscuridad {{ justify-content: flex-start; padding-top: 60px; }}
            footer {{ padding: 60px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <header>
            <div class="header-superior">
                <div class="header-titulos"><h1>{titulo_pag}</h1><h2>{sub_pag}</h2></div>
                <a href="https://hormigue.ar/" target="_blank">
                    <div class="bloque-autor"><img src="https://hormigue.ar/media/website/marcef.webp" class="foto-autor"><span class="nombre-autor">marce oliveira</span></div>
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
            <span style="position:absolute; top:10px; right:20px; color:white; font-size:3.5rem; cursor:pointer; z-index:100;" onclick="cerrarModalFuerza()">&times;</span>
            <div class="modal-oscuridad">
                <div id="modTit" style="font-family:'Bebas Neue'; font-size:2.5rem; border-bottom:1px solid var(--rojo-sangre); margin-bottom:15px; line-height:1.1;"></div>
                <div class="datos-expediente">
                    <strong>AUTOR:</strong> <span id="modAut"></span><br>
                    <strong>EDITORIAL:</strong> <span id="modEdi"></span><br>
                    <strong>AÑO:</strong> <span id="modAño"></span><br>
                    <strong>ESTADO:</strong> <span id="modEst"></span><br>
                    <strong>PRECIO:</strong> <span id="modPre"></span>
                </div>
                <button onclick="copiarAlPortapapeles()" id="btnCopiar" style="margin-top:20px; width:100%; padding:15px; background:var(--rojo-sangre); color:white; border:none; font-family:'Bebas Neue'; font-size:1.6rem; cursor:pointer; border-radius:8px;">COPIAR</button>
            </div>
        </div>
    </div>

    <div id="btn-ascenso" onclick="window.scrollTo({{top:0, behavior:'smooth'}})">&#9650;</div>

    <footer>
        <p style="margin-bottom:15px;"><strong style="font-family:'Almarai'; text-transform:uppercase;"><a href="https://hormigue.ar/" style="color:white;">HORMIGUE.AR</a></strong>
        <a href="https://hormigue.ar/"><img src="https://pica.hormigue.ar/hormiMG/icono%20hormi.png" style="height:2.2rem; vertical-align:middle; margin: 0 8px;"></a>
        <a href="https://hormigue.ar/" style="color:white;">Copyleft</a></p>
        <p style="font-family:'Arial Narrow'; font-size:0.85rem; opacity:0.7;">conocé el sitio creado con pocos recursos técnicos, económicos e intelectuales</p>
    </footer>

    <script>
        function abrirTab(id, el) {{ 
            document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active')); 
            document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active')); 
            document.getElementById(id).classList.add('active'); el.classList.add('active'); 
        }}
        function abrirExpediente(el) {{
            document.getElementById('modTit').innerText = el.getAttribute('data-tit');
            document.getElementById('modAut').innerText = el.getAttribute('data-aut');
            document.getElementById('modEdi').innerText = el.getAttribute('data-edi');
            document.getElementById('modAño').innerText = el.getAttribute('data-ano');
            document.getElementById('modEst').innerText = el.getAttribute('data-est');
            document.getElementById('modPre').innerText = el.getAttribute('data-pre');
            document.getElementById('modalFondo').style.backgroundImage = `url('${{el.getAttribute('data-img')}}')`;
            document.getElementById('modalLibro').style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }}
        function cerrarModal(e) {{ if(e.target.id==='modalLibro') cerrarModalFuerza(); }}
        function cerrarModalFuerza() {{ document.getElementById('modalLibro').style.display='none'; document.body.style.overflow='auto'; }}
        function copiarAlPortapapeles() {{
            const txt = `Quiero este libro: "${{document.getElementById('modTit').innerText}}" de ${{document.getElementById('modAut').innerText}}.`;
            navigator.clipboard.writeText(txt).then(()=>{{
                document.getElementById('btnCopiar').innerText = '¡COPIADO!';
                setTimeout(()=>{{ document.getElementById('btnCopiar').innerText = 'COPIAR'; }}, 2000);
            }});
        }}
        window.onscroll = ()=>{{ document.getElementById("btn-ascenso").style.display = (window.scrollY>500)? "flex":"none"; }};
    </script>
</body>
</html>
"""

def normalizar_categoria(c):
    c = c.lower()
    if 'ensayo' in c: return 'Ensayo'
    if 'historia' in c: return 'Historia'
    if 'polític' in c: return 'Política'
    if 'literatura' in c or 'narrativa' in c or 'crónica' in c: return 'Literatura'
    if 'sociolog' in c: return 'Sociología'
    if 'filosof' in c: return 'Filosofía'
    if 'psico' in c: return 'Psico'
    if 'antropolog' in c: return 'Antropología'
    return c.split('/')[0].strip().title()

def generar():
    with open(RUTA_JSON, 'r', encoding='utf-8') as f: data = json.load(f)
    libros_agrupados = defaultdict(list)
    for lib in data['libros']: libros_agrupados[normalizar_categoria(lib.get('categoria', 'Varios'))].append(lib)
    cats = sorted(libros_agrupados.keys())
    
    indice = '<ul class="lista-indice">' + "".join([f'<li><a href="#{c.lower().replace(" ","-")}">{c.upper()}</a></li>' for c in cats]) + '</ul>'
    
    # RESTAURACIÓN LITERAL DE TEXTOS
    bajada = ("Libros usados listos para seguir circulando.<br>"
              "Esta es una venta pensada para lectoras y lectores de la zona. Las ofertas se hacen por tandas. Voy cargando títulos a medida que avanzo con el inventario de mi biblioteca, por estantes.<br>"
              "Todos los libros están en muy buen estado; algunos, incluso, son nuevos. Fueron cuidados como corresponde, como mucho, alguna marca de lápiz. "
              "Los pocos ejemplares deteriorados lo están por razones nobles: paso del tiempo, ferias, reventas. Los títulos descatalogados, la resistencia.")

    t_btns = '<button class="tab-btn active" onclick="abrirTab(\'tab1\', this)">QUÉ</button>'
    t_btns += '<button class="tab-btn" onclick="abrirTab(\'tab2\', this)">CÓMO</button>'
    t_btns += '<button class="tab-btn" onclick="abrirTab(\'tab3\', this)">QUIÉNES</button>'
    t_btns += '<button class="tab-btn" onclick="abrirTab(\'tab4\', this)">ENTREGA</button>'
    
    t_cont = f'<div id="tab1" class="tab-content active">Las categorías son orientativas. Algunos libros encajan en varias y otros en ninguna. Revisá todo, nunca confíes en las clasificaciones.<div class="caja-indice-interna">{indice}</div></div>'
    t_cont += '<div id="tab2" class="tab-content">Revisá, picá el libro que te interese y copiá los datos. Podés usarlos para enviármelos, comparar precios o buscar reseñas en la web. Si no podés contactarme, este sitio no es para vos.<br>Si podés contactarme, coordinamos detalles: estado del libro, forma de pago y entrega. El pago es en pesos argentinos, por transferencia o efectivo. No acepto trueques, monedas extranjeras ni pagos en especies (por más seductora que sea la oferta).</div>'
    t_cont += '<div id="tab3" class="tab-content">Este sitio está pensado para lectoras y lectores cercanos. Posadas y Candelaria funcionan como referencia, pero lo central es el contacto: si podés ubicarme (directa o indirectamente), podés comprar. Si no, este sitio no es para vos.</div>'
    t_cont += '<div id="tab4" class="tab-content">Las compras iguales o superiores a $25.000 tienen envío gratuito a domicilio dentro de Posadas y Candelaria. Cada entrega o retiro se coordina; fecha, lugar y horario se acuerdan entre ambas partes lectoras.</div>'
    
    secciones = ""
    for cat in cats:
        c_id = cat.lower().replace(" ","-")
        secciones += f'<h2 class="titulo-categoria" id="{c_id}" style="font-family:\'Bebas Neue\'; font-size:3rem; color:white; background:black; padding:5px 15px; border-left:5px solid var(--rojo-sangre); margin:50px 0 20px 0; border-radius:4px;">{cat.upper()}</h2><div class="grilla-tacuru">'
        for lib in libros_agrupados[cat]:
            secciones += f"""
            <div class="tarjeta-expediente" data-tit="{lib.get('titulo','')}" data-aut="{lib.get('autor','')}" data-edi="{lib.get('editorial','')}" data-ano="{lib.get('año','')}" data-est="{lib.get('estado','Muy bueno')}" data-pre="{lib.get('precio','Consultar')}" data-img="{lib.get('imagen','')}" onclick="abrirExpediente(this)">
                <div class="tarjeta-imagen-wrapper"><img src="{lib.get('imagen','')}" onerror="this.style.display='none'"></div>
                <div class="enlace-tarjeta"><h3>{lib.get('titulo','')}</h3><p>{lib.get('autor','')}</p></div>
            </div>"""
        secciones += '</div>'
    
    with open(RUTA_HTML_DESTINO, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE.format(titulo_head="Libroteca", titulo_pag="LIBROTECA", sub_pag="ESTANTE DE ABAJO", bajada_pag=bajada, tabs_botones=t_btns, tabs_contenido=t_cont, secciones_html=secciones))
    print(">>> OPERACIÓN EXITOSA: Los textos han vuelto a casa y el diseño está blindado.")

if __name__ == "__main__": generar()
