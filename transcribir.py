"""
TRANSCRIPTOR DE AUDIO CON BARRA DE PROGRESO SIMULADA
Versión: 5.0 - Compatible con todas versiones de Whisper
"""

import whisper
import sys
import os
import time
import threading
import argparse
from pathlib import Path
from tqdm import tqdm

def crear_parser():
    """Configura los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Transcribe archivos de audio a texto con Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s reunion.m4a                    # Formato simple (por defecto)
  %(prog)s reunion.m4a --formato completo # Texto con tiempos
  %(prog)s reunion.m4a --formato srt      # Solo subtítulos
  %(prog)s reunion.m4a --formato todos    # Todos los formatos
  %(prog)s reunion.m4a --modelo medium    # Mayor precisión
        """
    )
    
    parser.add_argument(
        "audio",
        help="Ruta al archivo de audio (mp3, m4a, wav, etc.)"
    )
    
    parser.add_argument(
        "--formato", "-f",
        choices=["simple", "completo", "srt", "todos"],
        default="simple",
        help="Formato de salida"
    )
    
    parser.add_argument(
        "--modelo", "-m",
        choices=["tiny", "base", "small", "medium", "large"],
        default="small",
        help="Modelo de Whisper"
    )
    
    parser.add_argument(
        "--carpeta", "-c",
        default="resultados",
        help="Carpeta para guardar resultados"
    )
    
    parser.add_argument(
        "--idioma", "-l",
        default="es",
        help="Idioma (es, en, fr, etc.)"
    )
    
    return parser

def transcribir_con_barra_simulada(ruta_audio, modelo="small", idioma="es"):
    """
    Transcripción con barra de progreso SIMULADA
    (Funciona con todas versiones de Whisper)
    """
    print(f"⚙️  Cargando modelo '{modelo}'...")
    model = whisper.load_model(modelo)
    
    # Variables compartidas para la barra de progreso
    transcripcion_completada = False
    tiempo_inicio = time.time()
    
    # Crear barra de progreso en un hilo separado
    def mostrar_barra_progreso():
        """Muestra una barra de progreso animada mientras se transcribe"""
        with tqdm(
            total=100, 
            desc="🎤 Transcribiendo", 
            unit="%",
            bar_format="{l_bar}{bar:40}{r_bar}",
            colour="green",
            ncols=80,
            mininterval=0.3
        ) as pbar:
            
            # Animar la barra hasta que termine la transcripción
            while not transcripcion_completada:
                tiempo_actual = time.time() - tiempo_inicio
                
                # Estimación basada en tiempos típicos
                # Para 1.5 horas de audio con modelo small: ~5-10 minutos
                if tiempo_actual < 30:  # Primeros 30 segundos: carga
                    progreso = min(15, (tiempo_actual / 30) * 15)
                elif tiempo_actual < 180:  # Minutos 0.5-3: transcripción principal
                    progreso = 15 + min(70, ((tiempo_actual - 30) / 150) * 70)
                else:  # Después de 3 minutos: finalización
                    progreso = 85 + min(15, ((tiempo_actual - 180) / 120) * 15)
                
                # Actualizar barra
                if progreso > pbar.n:
                    pbar.update(progreso - pbar.n)
                
                # Mostrar tiempo transcurrido
                pbar.set_postfix({
                    "Tiempo": f"{int(tiempo_actual)}s",
                    "Estado": "Procesando..." if tiempo_actual < 120 else "Finalizando"
                })
                
                time.sleep(0.5)  # Actualizar cada 0.5 segundos
    
    print("⏳ Iniciando transcripción...")
    
    # Iniciar barra de progreso en un hilo separado
    hilo_barra = threading.Thread(target=mostrar_barra_progreso)
    hilo_barra.daemon = True
    hilo_barra.start()
    
    try:
        # Realizar transcripción SIN callback (compatible con todas versiones)
        resultado = model.transcribe(
            ruta_audio,
            language=idioma,
            task="transcribe",
            verbose=False,
            fp16=False
        )
        
        # Marcar como completada y esperar a que termine la barra
        transcripcion_completada = True
        time.sleep(0.6)  # Dar tiempo a que la barra se actualice
        
        tiempo_total = time.time() - tiempo_inicio
        print(f"\n✅ Transcripción completada en {tiempo_total:.1f} segundos")
        
        return resultado
        
    except Exception as e:
        transcripcion_completada = True
        raise e

def guardar_simple(texto, ruta_base, carpeta):
    """Guarda solo el texto limpio"""
    archivo = Path(carpeta) / f"{ruta_base}_simple.txt"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto.strip())
    return archivo

def guardar_completo(resultado, ruta_base, carpeta):
    """Guarda texto con marcas de tiempo"""
    archivo = Path(carpeta) / f"{ruta_base}_completo.txt"
    
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"TRANSCRIPCIÓN DETALLADA\n")
        f.write(f"Archivo: {ruta_base}\n")
        f.write(f"Duración total: {resultado['segments'][-1]['end']:.2f} segundos\n")
        f.write("=" * 70 + "\n\n")
        
        for i, segmento in enumerate(resultado["segments"], 1):
            inicio = segmento["start"]
            fin = segmento["end"]
            texto_seg = segmento["text"].strip()
            
            min_ini = int(inicio // 60)
            seg_ini = inicio % 60
            min_fin = int(fin // 60)
            seg_fin = fin % 60
            
            f.write(f"[{i:03d}] {min_ini:02d}:{seg_ini:05.2f} - {min_fin:02d}:{seg_fin:05.2f}\n")
            f.write(f"{texto_seg}\n")
            f.write("-" * 70 + "\n")
    
    return archivo

def guardar_srt(resultado, ruta_base, carpeta):
    """Guarda en formato SRT para subtítulos"""
    archivo = Path(carpeta) / f"{ruta_base}.srt"
    
    def formato_srt(segundos):
        """Convierte segundos a formato HH:MM:SS,mmm"""
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        seg = int(segundos % 60)
        mili = int((segundos - int(segundos)) * 1000)
        return f"{horas:02d}:{minutos:02d}:{seg:02d},{mili:03d}"
    
    with open(archivo, "w", encoding="utf-8") as f:
        for i, segmento in enumerate(resultado["segments"], 1):
            inicio = segmento["start"]
            fin = segmento["end"]
            texto = segmento["text"].strip()
            
            f.write(f"{i}\n")
            f.write(f"{formato_srt(inicio)} --> {formato_srt(fin)}\n")
            f.write(f"{texto}\n\n")
    
    return archivo

def mostrar_resumen(resultado, archivos_creados, args, tiempo_transcripcion):
    """Muestra un resumen de los resultados"""
    texto = resultado["text"].strip()
    duracion = resultado['segments'][-1]['end'] if resultado['segments'] else 0
    palabras = len(texto.split())
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TRANSCRIPCIÓN")
    print("=" * 60)
    
    print(f"📁 Archivo original: {Path(args.audio).name}")
    print(f"⚙️  Configuración: {args.modelo.upper()} | {args.idioma.upper()} | {args.formato}")
    print(f"⏱️  Duración audio: {duracion/60:.1f} min ({duracion:.0f}s)")
    print(f"⚡ Tiempo transcripción: {tiempo_transcripcion:.1f}s")
    print(f"📝 Estadísticas: {len(texto):,} chars | {palabras:,} palabras")
    
    print(f"\n💾 ARCHIVOS CREADOS en '{args.carpeta}/':\n")
    for archivo in archivos_creados:
        tamaño_kb = archivo.stat().st_size / 1024
        print(f"   • {archivo.name} ({tamaño_kb:.1f} KB)")
    
    print(f"\n👁️  VISTA PREVIA (primeras 3 líneas):\n")
    print("-" * 50)
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    for i, linea in enumerate(lineas[:3]):
        print(f"{linea[:120]}{'...' if len(linea) > 120 else ''}")

def main():
    """Función principal"""
    parser = crear_parser()
    args = parser.parse_args()
    
    # Verificar archivo de audio
    archivo_audio = Path(args.audio)
    if not archivo_audio.exists():
        print(f"❌ ERROR: No se encuentra '{args.audio}'")
        print(f"   Ruta actual: {Path.cwd()}")
        return 1
    
    # Crear carpeta de resultados
    os.makedirs(args.carpeta, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🎧 TRANSCRIPTOR WHISPER v5.0 (Barra de progreso simulada)")
    print("=" * 60)
    print("ℹ️  Usando barra de progreso simulada (compatible con todas versiones)")
    
    try:
        # Realizar transcripción CON barra simulada
        inicio = time.time()
        resultado = transcribir_con_barra_simulada(
            str(archivo_audio),
            modelo=args.modelo,
            idioma=args.idioma
        )
        
        tiempo_transcripcion = time.time() - inicio
        
        # Preparar datos
        texto = resultado["text"].strip()
        nombre_base = archivo_audio.stem
        archivos_creados = []
        
        # Guardar según formato
        if args.formato in ["simple", "todos"]:
            archivos_creados.append(guardar_simple(texto, nombre_base, args.carpeta))
        
        if args.formato in ["completo", "todos"]:
            archivos_creados.append(guardar_completo(resultado, nombre_base, args.carpeta))
        
        if args.formato in ["srt", "todos"]:
            archivos_creados.append(guardar_srt(resultado, nombre_base, args.carpeta))
        
        # Mostrar resumen
        mostrar_resumen(resultado, archivos_creados, args, tiempo_transcripcion)
        
        print("\n" + "=" * 60)
        print("✅ ¡TRANSCRIPCIÓN COMPLETADA CON ÉXITO!")
        print("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Transcripción cancelada por el usuario")
        return 130
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1

if __name__ == "__main__":
    # Verificar e instalar tqdm si es necesario
    try:
        from tqdm import tqdm
    except ImportError:
        print("📦 Instalando tqdm...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm", "--quiet"])
        from tqdm import tqdm
    
    sys.exit(main())
