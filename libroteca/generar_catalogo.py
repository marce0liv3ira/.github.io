import json
import os
from collections import defaultdict

# --- COORDENADAS TÁCTICAS ---
RUTA_JSON = r'C:\Users\sebam\bunker\HORMIgithub2\.github.io\libroteca\catalogo.json'
RUTA_HTML_DESTINO = r'C:\Users\sebam\bunker\HORMIgithub2\.github.io\libroteca\index.html'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Libroteca - Hormiguear</title>
    
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
        
        a {{ color: var(--rojo-sangre) !important; text-decoration: none; transition: 0.2s; }}
        a:hover {{ color: #D62828 !important; text-shadow: 0 0 5px rgba(163, 0, 0, 0.4); }}
        
        .contenedor {{ flex: 1; max-width: 1200px; margin: 0 auto; width: 100%; display: flow-root; }}
        
        /* HEADER: LOGO SÓLIDO Y PERFIL */
        header {{ 
            border-bottom: 1px solid var(--rojo-sangre); padding: 40px 20px; margin-bottom: 30px; border-radius: 8px;
            box-shadow: 0 4px 6px -6px rgba(163, 0, 0, 0.8);
            background-image: linear-gradient(rgba(250, 246, 237, 0.4), rgba(250, 246, 237, 0.5)), url('img/logolibro.png');
            background-size: contain; background-position: center; background-repeat: no-repeat;
            display: flex; flex-direction: column; gap: 20px;
        }}

        .header-superior {{ display: flex; justify-content: space-between; align-items: center; width: 100%; }}
        h1 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 5rem !important; color: var(--rojo-sangre) !important; margin: 0; line-height: 0.9 !important; }}
        h2 {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 2.5rem !important; color: var(--negro) !important; margin: 0; }}

        .bloque-autor {{ display: flex; align-items: center; gap: 15px; background: rgba(163, 0, 0, 0.05); padding: 10px 15px; border-radius: 50px 10px 10px 50px; border: 1px solid rgba(163, 0, 0, 0.2); }}
        .foto-autor {{ width: 70px; height: 70px; border-radius: 50%; border: 2px solid var(--rojo-sangre); object-fit: cover; box-shadow: 0 0 10px rgba(163, 0, 0, 0.3); }}
        .nombre-autor {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; color: var(--negro); text-transform: uppercase; }}

        .bajada {{ 
            font-size: 1.1rem; font-weight: 500; background: rgba(255, 255, 255, 0.3); padding: 15px 20px; 
            border-radius: 4px; border-left: 4px solid var(--rojo-sangre); backdrop-filter: blur(2px); 
        }}

        /* MENÚ E ÍNDICE DE COLUMNAS */
        .caja-menu {{ border: 1px solid var(--rojo-sangre); margin-bottom: 40px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 12px rgba(163, 0, 0, 0.25); }}
        .tabs-header {{ display: flex; border-bottom: 1px solid var(--rojo-sangre); background: var(--negro); }}
        .tab-btn {{ flex: 1; padding: 12px; cursor: pointer; font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: var(--blanco); background: transparent; border: none; transition: 0.3s; }}
        .tab-btn.active {{ background: var(--rojo-sangre); }}
        .tab-content {{ padding: 20px; display: none; font-size: 1.1rem; line-height: 1.5; }}
        .tab-content.active {{ display: block; }}
        
        .lista-indice {{ 
            list-style: none; padding: 0; margin: 15px 0 0 0; display: flex; flex-direction: column; 
            flex-wrap: wrap; align-content: flex-start; gap: 6px 30px; max-height: 150px; 
        }}
        .lista-indice li {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.25rem; }}

        /* GRID Y TARJETAS */
        .titulo-categoria {{ font-family: 'Bebas Neue', sans-serif !important; font-size: 3rem !important; color: var(--blanco) !important; background: var(--negro) !important; padding: 5px 15px !important; border-left: 5px solid var(--rojo-sangre) !important; margin: 50px 0 20px 0 !important; border-radius: 4px; }}
        .grilla-tacuru {{ display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 15px !important; margin: 2rem 0 !important; }}
        
        .tarjeta-expediente {{ position: relative !important; aspect-ratio: 1 / 1 !important; background-color: #000 !important; border: 1px solid var(--rojo-oscuro) !important; border-radius: 8px !important; overflow: hidden; transition: 0.4s; cursor: pointer; }}
        .tarjeta-expediente:hover {{ transform: scale(1.03) !important; border-color: var(--rojo-sangre) !important; box-shadow: 0 0 25px rgba(163, 0, 0, 0.65); }}
        .tarjeta-imagen-wrapper img {{ width: 100%; height: 100%; object-fit: cover; filter: grayscale(100%); opacity: 0.6; transition: 0.5s; }}
        .tarjeta-expediente:hover img {{ filter: grayscale(0%); opacity: 1; }}
        
        .enlace-tarjeta {{ display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; height: 100%; padding: 15px; position: relative; z-index: 10; text-align: center; color: white; }}
        .tarjeta-expediente h3 {{ 
            font-family: 'Bebas Neue', sans-serif !important; font-size: 1.6rem !important; margin: 0 0 6px 0; 
            line-height: 1 !important; text-shadow: 2px 2px 4px #000; width: 100%; overflow: hidden; 
            text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; 
        }}

        /* MODAL: ROJO SANGRE SECA */
        .modal-overlay {{ display: none; position: fixed; z-index: 9999; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px); }}
        .modal-caja {{ position: relative; width: 90%; max-width: 450px; aspect-ratio: 2/3; border: 2px solid var(--rojo-sangre); border-radius: 8px; background-size: cover; background-position: center; overflow: hidden; }}
        .modal-oscuridad {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); display: flex; flex-direction: column; justify-content: center; padding: 30px; box-sizing: border-box; color: white; }}
        .modal-titulo {{ font-family: 'Bebas Neue', sans-serif; font-size: 2.6rem; border-bottom: 1px solid var(--rojo-sangre); margin-bottom: 20px; padding-bottom: 10px; }}
        .datos-expediente {{ font-size: 1.15rem; line-height: 1.8; text-align: left; }}
        .datos-expediente strong {{ color: var(--rojo-sangre) !important; font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; }}
        
        #btn-ascenso {{ 
            position: fixed; bottom: 30px; right: 30px; width: 55px; height: 55px; background: rgba(0, 0, 0, 0.8); 
            color: var(--blanco); border: 2px solid var(--rojo-sangre); border-radius: 50%; display: none; 
            justify-content: center; align-items: center; transition: 0.3s; z-index: 1000; 
        }}
        #btn-ascenso:hover {{ background: var(--rojo-sangre); transform: scale(1.1) translateY(-5px); box-shadow: 0 0 20px var(--rojo-sangre); }}

        footer {{ margin-top: 60px; background-color: var(--negro); border-top: 4px solid var(--rojo-sangre); width: 100%; text-align: center; color: white; padding: 25px 0; }}
        
        @media (max-width: 600px) {{ 
            .grilla-tacuru {{ grid-template-columns: repeat(2, 1fr) !important; }} 
            .lista-indice {{ max-height: none !important; flex-direction: row !important; flex-wrap: wrap !important; }} 
            .lista-indice li {{ width: 45%; }} 
            .header-superior {{ flex-direction: column; align-items: flex-start; gap: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <header>
            <div class="header-superior">
                <div class="header-titulos"><h1>LIBROTECA</h1><h2>ESTANTE DE ABAJO</h2></div>
                <div class="bloque-autor">
                    <img src="https://hormigue.ar/media/website/marcef.webp" class="foto-autor">
                    <span class="nombre-autor">marce oliveira</span>
                </div>
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
            <span style="position:absolute; top:10px; right:20px; color:white; font-size:3rem; cursor:pointer;" onclick="cerrarModalFuerza()">&times;</span>
            <div class="modal-oscuridad">
                <div id="modTit" class="modal-titulo"></div>
                <div class="datos-expediente">
                    <strong>AUTOR:</strong> <span id="modAut"></span><br>
                    <strong>EDITORIAL:</strong> <span id="modEdi"></span><br>
                    <strong>AÑO:</strong> <span id="modAño"></span><br>
                    <strong>ESTADO:</strong> <span id="modEst"></span><br>
                    <strong>PRECIO:</strong> <span id="modPre"></span>
                </div>
                <button onclick="copiarAlPortapapeles()" style="margin-top:20px; width:100%; padding:15px; background:var(--rojo-sangre); color:white; border:none; font-family:'Bebas Neue'; font-size:1.6rem; cursor:pointer; border-radius:8px;">COPIAR</button>
            </div>
        </div>
    </div>

    <div id="btn-ascenso" onclick="window.scrollTo({{top:0, behavior:'smooth'}})">&#9650;</div>

    <footer>
        <p><strong style="font-family:'Almarai'; text-transform:uppercase;"><a href="https://hormigue.ar/" style="color:white;">HORMIGUE.AR</a></strong>
        <a href="https://hormigue.ar/"><img src="https://pica.hormigue.ar/hormiMG/icono%20hormi.png" style="height:2rem; vertical-align:middle; margin: 0 5px;"></a>
        <a href="https://hormigue.ar/" style="color:white;">Copyleft</a></p>
        <p style="font-family:'Arial Narrow'; font-size:0.8rem; opacity:0.7;">un sitio creado con pocos recursos técnicos, económicos e intelectuales</p>
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
        }}
        function cerrarModal(e) {{ if(e.target.id==='modalLibro') e.target.style.display='none'; }}
        function cerrarModalFuerza() {{ document.getElementById('modalLibro').style.display='none'; }}
        function copiarAlPortapapeles() {{
            const txt = `Quiero este libro: "${{document.getElementById('modTit').innerText}}" de ${{document.getElementById('modAut').innerText}}.`;
            navigator.clipboard.writeText(txt).then(()=>alert('Copiado al portapapeles'));
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
    if 'ciencia' in c: return 'Divulgación Dura'
    return c.split('/')[0].strip().title()

def generar():
    try:
        with open(RUTA_JSON, 'r', encoding='utf-8') as f: data = json.load(f)
        libros_agrupados = defaultdict(list)
        for lib in data['libros']: libros_agrupados[normalizar_categoria(lib.get('categoria', 'Varios'))].append(lib)
        cats = sorted(libros_agrupados.keys())
        
        indice = '<ul class="lista-indice">' + "".join([f'<li><a href="#{c.lower().replace(" ","-")}">{c.upper()}</a></li>' for c in cats]) + '</ul>'
        
        t_btns = '<button class="tab-btn active" onclick="abrirTab(\'tab1\', this)">CONTENIDO</button>'
        t_btns += '<button class="tab-btn" onclick="abrirTab(\'tab2\', this)">CÓMO</button>'
        t_btns += '<button class="tab-btn" onclick="abrirTab(\'tab3\', this)">ENTREGA</button>'
        
        t_cont = f'<div id="tab1" class="tab-content active"><p>Categorías orientativas. No confíes en las etiquetas.</p><div class="caja-indice-interna">{indice}</div></div>'
        t_cont += '<div id="tab2" class="tab-content">Revisá, picá en el título y copiá los datos. Si podés ubicarme, podés comprar. Pago en pesos, transferencia o efectivo.</div>'
        t_cont += '<div id="tab3" class="tab-content">Envío gratuito en Posadas y Candelaria en compras superiores a $25.000. Coordinamos lugar y horario.</div>'
        
        secciones = ""
        for cat in cats:
            c_id = cat.lower().replace(" ","-")
            secciones += f'<h2 class="titulo-categoria" id="{c_id}">{cat.upper()}</h2><div class="grilla-tacuru">'
            for lib in libros_agrupados[cat]:
                secciones += f"""
                <div class="tarjeta-expediente" data-tit="{lib.get('titulo','')}" data-aut="{lib.get('autor','')}" data-edi="{lib.get('editorial','')}" data-ano="{lib.get('año','')}" data-est="{lib.get('estado','Muy bueno')}" data-pre="{lib.get('precio','Consultar')}" data-img="{lib.get('imagen','')}" onclick="abrirExpediente(this)">
                    <div class="tarjeta-imagen-wrapper"><img src="{lib.get('imagen','')}" onerror="this.style.display='none'"></div>
                    <div class="enlace-tarjeta"><h3>{lib.get('titulo','')}</h3><p>{lib.get('autor','')}</p></div>
                </div>"""
            secciones += '</div>'
        
        bajada = "Libros usados listos para seguir circulando. Tandas de ofertas para lectores cercanos. Cuidados como corresponde."
        
        with open(RUTA_HTML_DESTINO, 'w', encoding='utf-8') as f:
            f.write(HTML_TEMPLATE.format(titulo_head="Libroteca", bajada_pag=bajada, tabs_botones=t_btns, tabs_contenido=t_cont, secciones_html=secciones))
        
        print(f">>> OPERACIÓN EXITOSA: {len(data['libros'])} libros procesados. HTML blindado en su destino.")

    except Exception as e: print(f">>> ERROR EN LA MATRIZ: {e}")

if __name__ == "__main__": generar()
