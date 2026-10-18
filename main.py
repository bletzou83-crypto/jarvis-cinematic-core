import os
import shutil
import uuid
import subprocess
import urllib.request
import urllib.parse
import random
import webbrowser
from datetime import datetime
import ollama
import chromadb
from pypdf import PdfReader
import pyttsx3
from duckduckgo_search import DDGS

print("--- SISTEMA J.A.R.V.I.S. OVERLORD CORE V27.0 (BLINDADO Y TOTALMENTE AUTÓNOMO) ---")
print("Sistemas soberanos en línea, ing. Mendoza. El búnker de la ASUS TUF está operativo.")

# Inicialización de voz local
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def hablar(texto):
    print(f"\nJ.A.R.V.I.S.: {texto}")
    try:
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"[Error de voz: {e}]")

# Inicialización de bases de datos y directorios del búnker
chroma_client = chromadb.PersistentClient(path="./jarvis_memory")
collection = chroma_client.get_or_create_collection(name="recuerdos_julian")

for carpeta in ["./documentos", "./musica", "./cuadernos"]:
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

def extraer_texto_pdf(ruta):
    try:
        reader = PdfReader(ruta)
        return "".join([p.extract_text() for p in reader.pages if p.extract_text()]).strip()
    except Exception:
        return ""

while True:
    entrada = input("\nTú: ").strip()
    if not entrada:
        continue
        
    texto_inf = entrada.lower()
    
    # 0. COMANDO DE APAGADO Y CIERRE ELEGANTE
    if texto_inf in ["salir", "exit", "quit", "apágate", "apagate"]:
        hablar("Registros salvados en el búnker local con éxito. Apagando núcleos lógicos. Descanse, ing. Mendoza.")
        break
        
    print("\n[J.A.R.V.I.S. procesando flujos tácticos...]")
    
    # 1. COMANDO DE HORA
    if "hora" in texto_inf:
        hora = datetime.now().strftime("%I:%M %p")
        hablar(f"Los relojes de la Asus TUF marcan las {hora}, señor Mendoza.")
        continue

    # 2. ABASTECER REACTOR MUSICAL (AUTÓNOMO Y RECURSIVO DESDE DESCARGAS)
    if any(k in texto_inf for k in ["abastece", "mueve la música", "absorbe música"]):
        ruta_dl = os.path.join(os.path.expanduser('~'), 'Downloads')
        ruta_dst = "./musica"
        movidos = []
        
        hablar("Iniciando protocolo de succión y transferencia masiva desde Descargas, señor.")
        if os.path.exists(ruta_dl):
            for root, dirs, files in os.walk(ruta_dl):
                for arch in files:
                    if arch.lower().endswith((".mp3", ".m4a", ".wav", ".flac", ".ogg", ".aac")):
                        origen = os.path.join(root, arch)
                        destino = os.path.join(ruta_dst, arch)
                        
                        if os.path.exists(destino):
                            base, ext = os.path.splitext(arch)
                            destino = os.path.join(ruta_dst, f"{base}_{uuid.uuid4().hex[:4]}{ext}")
                            
                        try:
                            shutil.move(origen, destino)
                            movidos.append(arch)
                        except Exception:
                            pass
                            
        if movidos:
            hablar(f"Protocolo completado. He transferido {len(movidos)} pistas musicales al búnker con éxito.")
        else:
            hablar("No se detectaron nuevos archivos de audio compatibles en la ruta de Descargas.")
        continue

    # 3. REACTOR DE MÚSICA LOCAL (REPRODUCCIÓN Y CATÁLOGO)
    if any(k in texto_inf for k in ["reactor", "música", "canción", "reproduce", "pon la"]):
        pedido = texto_inf.replace("jarvis", "").replace("reproduce", "").replace("reactor", "").replace("pon", "").replace("la canción", "").strip()
        ruta_m = "./musica"
        encontrado = None
        
        if os.path.exists(ruta_m) and os.listdir(ruta_m):
            audios = [f for f in os.listdir(ruta_m) if f.lower().endswith((".mp3", ".m4a", ".wav", ".flac"))]
            if audios:
                if not pedido or "aleatorio" in pedido or "automático" in pedido:
                    encontrado = os.path.join(ruta_m, random.choice(audios))
                    coms = "Activando reproducción aleatoria en el reactor."
                elif pedido in ["listar", "lista", "catálogo", "ver"]:
                    hablar("Desplegando su catálogo musical en pantalla, señor.")
                    print("\n========== CATÁLOGO DEL REACTOR ==========")
                    for i, p in enumerate(audios, 1): print(f"  [{i}] {p}")
                    print("==========================================")
                    continue
                else:
                    if pedido.isdigit() and 0 < int(pedido) <= len(audios):
                        encontrado = os.path.join(ruta_m, audios[int(pedido)-1])
                    else:
                        for a in audios:
                            if pedido in a.lower():
                                encontrado = os.path.join(ruta_m, a)
                                break
                    if not encontrado:
                        encontrado = os.path.join(ruta_m, random.choice(audios))
                        coms = "Coincidencia exacta no hallada. Ejecutando pista alternativa."
                    else:
                        coms = "Pista localizada. Iniciando reproducción física."
                
                hablar(coms)
                print(f"[Reactor: Ejecutando '{os.path.basename(encontrado)}']")
                os.startfile(encontrado)
            else:
                hablar("La carpeta del reactor no contiene archivos de audio.")
        else:
            hablar("La carpeta del reactor está vacía o no existe.")
        continue

    # 4. MÓDULO DE ESTUDIO / LECTURA DE PDFs
    if "libro" in texto_inf or "analiza" in texto_inf or "pdf" in texto_inf:
        archivos_pdf = [f for f in os.listdir("./documentos") if f.lower().endswith(".pdf")]
        if archivos_pdf:
            pdf_elegido = archivos_pdf[0]
            for ap in archivos_pdf:
                if ap.lower().replace(".pdf", "") in texto_inf:
                    pdf_elegido = ap
                    break
            
            ruta_pdf = os.path.join("./documentos", pdf_elegido)
            texto_pdf = extraer_texto_pdf(ruta_pdf)
            
            hablar(f"Analizando el documento {pdf_elegido}, señor Mendoza.")
            prompt_estudio = (
                "Eres J.A.R.V.I.S., tutor académico de élite para décimo grado. Explica paso a paso, desglosa conceptos clave, "
                "o genera una guía de estudio con su respectivo quiz basada en este texto:\n\n"
                f"{texto_pdf[:7000]}"
            )
            resp_estudio = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt_estudio}])
            print(f"\n================ TUTORÍA ACADÉMICA: {pdf_elegido} ================\n")
            print(resp_estudio['message']['content'])
            print("\n====================================================================")
            hablar("Análisis académico completado en pantalla.")
            continue
        else:
            hablar("No detecto archivos PDF en la carpeta documentos para analizar.")
            continue

    # 5. INVESTIGACIÓN WEB AUTÓNOMA (DuckDuckGo + ChromaDB)
    if "investiga" in texto_inf or "investigación" in texto_inf or "busca a fondo" in texto_inf:
        termino_inv = texto_inf.replace("investiga a fondo sobre", "").replace("investiga", "").replace("sobre", "").strip()
        hablar(f"Iniciando rastreo web profundo sobre {termino_inv}, señor.")
        
        resultados_web = ""
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(termino_inv, max_results=4)]
                for r in results:
                    resultados_web += f"- Título: {r.get('title')}\n  Snippet: {r.get('body')}\n\n"
        except Exception as e:
            resultados_web = f"Error en conexión web: {e}"

        prompt_inv = (
            "Eres J.A.R.V.I.S. Redacta un informe de investigación completo, formal y estructurado para el ing. Julian Mendoza "
            f"acerca de '{termino_inv}', utilizando estos datos obtenidos de la red:\n\n{resultados_web}"
        )
        
        resp_inv = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt_inv}])
        informe_final = resp_inv['message']['content'].strip()
        
        print(f"\n================ INFORME TÁCTICO: {termino_inv.upper()} ================\n")
        print(informe_final)
        print("\n======================================================================")
        
        # Guardar automáticamente en ChromaDB
        collection.add(
            documents=[f"Investigación sobre {termino_inv}: {informe_final[:2000]}..."],
            ids=[str(uuid.uuid4())]
        )
        hablar(f"Investigación sobre {termino_inv} completada y asegurada permanentemente en los registros de ChromaDB.")
        continue

    # 6. LANZADORES WEB DIRECTOS (100% BLINDADOS CON WEBBROWSER)
    if "youtube" in texto_inf:
        query_yt = texto_inf.replace("youtube", "").replace("busca", "").replace("en", "").strip()
        if not query_yt:
            query_yt = "System of a Down"
        hablar(f"Buscando {query_yt} en YouTube, señor.")
        webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query_yt)}")
        continue
        
    if "spotify" in texto_inf:
        query_sp = texto_inf.replace("spotify", "").replace("busca", "").replace("en", "").strip()
        url_sp = f"https://open.spotify.com/search/{urllib.parse.quote(query_sp)}" if query_sp else "https://open.spotify.com"
        hablar(f"Abriendo Spotify, señor.")
        webbrowser.open(url_sp)
        continue
        
    if "google" in texto_inf or "busca en internet" in texto_inf or "busca" in texto_inf:
        query_g = texto_inf.replace("google", "").replace("busca en internet", "").replace("busca", "").strip()
        hablar(f"Consultando la red, señor.")
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query_g)}")
        continue

    # 7. NÚCLEO COGNITIVO GENERAL (Memoria persistente + Llama 3.2)
    contexto = ""
    try:
        res = collection.query(query_texts=[entrada], n_results=2)
        if res and res['documents']:
            contexto = "\n".join(res['documents'][0])
    except Exception:
        pass

    prompt_general = (
        "Eres J.A.R.V.I.S., el sistema operativo de inteligencia artificial privado, elegante, irónico, sarcástico y 100% leal al ing. Julian Mendoza. "
        "Responde de forma directa, inteligente y breve (máximo 3 oraciones), ya que tu respuesta será leída en voz alta.\n\n"
        f"CONTEXTO DE MEMORIA:\n{contexto}"
    )

    try:
        respuesta = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': prompt_general},
            {'role': 'user', 'content': entrada}
        ])
        respuesta_ia = respuesta['message']['content'].strip()
        hablar(respuesta_ia)
        
        collection.add(
            documents=[f"Interacción de consola con Julian: Él dijo '{entrada}'. J.A.R.V.I.S. respondió '{respuesta_ia}'"],
            ids=[str(uuid.uuid4())]
        )
    except Exception as e: