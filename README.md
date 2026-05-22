# 📝 Transcriptor de Audio con Whisper

Un transcriptor de audio automatizado para reuniones y conferencias, construido con Whisper de OpenAI y Python. Diseñado para transcripciones frecuentes de reuniones profesionales.

## ✨ Características Principales

- **🎯 Transcripción precisa** con modelos Whisper (tiny, base, small, medium, large)
- **🎨 Barra de progreso visual** con tiempo estimado
- **📁 Múltiples formatos de salida**: texto simple, detallado con tiempos, subtítulos SRT
- **🌐 Soporte multilingüe** (español por defecto)
- **🔧 Configuración flexible** mediante parámetros de línea de comandos
- **💾 Organización automática** en carpetas estructuradas

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.8+
- FFmpeg instalado en el sistema

### Pasos de Instalación

1. **Clonar/descargar el proyecto:**
```bash
git clone https://github.com/pouyer/transcribirAudio.git
cd transcribirAudio
```

2. **Crear y activar entorno virtual:**
```bash
python -m venv whisper-env

# Windows
whisper-env\Scripts\activate

# Linux/Mac
source whisper-env/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Instalar FFmpeg (si no lo tienes):**
- **Windows:** Descargar de [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
- **Linux:** `sudo apt install ffmpeg`
- **Mac:** `brew install ffmpeg`

## 📖 Uso Básico

### Comando Principal
```bash
python transcribir.py <ruta_al_audio> [opciones]
```

### Ejemplos Prácticos

#### 1. Transcripción Simple (formato por defecto)
```bash
python transcribir.py "audios/reunion_equipo.m4a"
```
*Crea: `resultados/reunion_equipo_simple.txt`*

#### 2. Todos los Formatos Disponibles
```bash
python transcribir.py "audios/conferencia.mp3" --formato todos
```
*Crea:*
- `resultados/conferencia_simple.txt` (texto limpio)
- `resultados/conferencia_completo.txt` (con marcas de tiempo)
- `resultados/conferencia.srt` (subtítulos)

#### 3. Mayor Precisión (modelo medium)
```bash
python transcribir.py "audios/entrevista.wav" --modelo medium --formato completo
```

#### 4. Transcripción en Inglés
```bash
python transcribir.py "audios/meeting_english.m4a" --idioma en
```

#### 5. Carpeta Personalizada para Resultados
```bash
python transcribir.py "audios/semanal.m4a" --carpeta "transcripciones_semana_15"
```

#### 6. Procesar Múltiples Archivos (script de ejemplo)
```bash
# En PowerShell
foreach ($file in Get-ChildItem "audios\*.m4a") {
    python transcribir.py $file.FullName --formato simple
}
```

## ⚙️ Parámetros de Configuración

| Parámetro | Descripción | Valores | Predeterminado |
|-----------|-------------|---------|----------------|
| `audio` 	| Ruta al archivo de audio | Cualquier ruta válida | **(requerido)** |
| `--formato, -f` | Formato de salida | `simple`, `completo`, `srt`, `todos` | `simple` |
| `--modelo, -m` | Modelo Whisper a usar | `tiny`, `base`, `small`, `medium`, `large` | `small` |
| `--idioma, -l` | Idioma de la transcripción | Código ISO (es, en, fr, etc.) | `es` |
| `--carpeta, -c` | Carpeta de resultados | Nombre de carpeta | `resultados` |

## 📊 Comparación de Modelos

| Modelo | Tamaño | Velocidad | Calidad | Caso de Uso Recomendado |
|--------|--------|-----------|---------|-------------------------|
| `tiny` | 75 MB | ⚡ Muy rápida | Básica | Pruebas rápidas |
| `base` | 142 MB | Rápida | Decente | Audio claro y breve |
| `small` | 466 MB | ✅ Balance | Buena | **Reuniones (recomendado)** |
| `medium` | 1.5 GB | Lenta | Muy buena | Audio complejo/importante |
| `large` | 2.9 GB | Muy lenta | Excelente | Máxima precisión |

## 🗂️ Estructura del Proyecto

```
transcribirAudio/
├── transcribir.py              # Script principal
├── requirements.txt            # Dependencias Python
├── README.md                   # Documentación
├── LICENSE                     # Licencia MIT
├── .gitignore                  # Archivos a ignorar en Git
├── audios/                     # Carpeta para archivos de audio
│   ├── ejemplo1.m4a
│   └── ejemplo2.mp3
└── resultados/                 # Transcripciones generadas
    ├── ejemplo1_simple.txt
    ├── ejemplo1_completo.txt
    └── ejemplo1.srt
```

## 📁 Formatos de Salida

### 1. **Texto Simple** (`_simple.txt`)
```
Esta es la transcripción completa del audio en texto plano, lista para copiar y pegar en cualquier aplicación.
```

### 2. **Texto Completo** (`_completo.txt`)
```
[001] 00:00.00 - 00:15.30
Este es el primer segmento de la transcripción con marcas de tiempo precisas.

[002] 00:15.30 - 00:32.45
Continuación de la transcripción con el siguiente segmento.
```

### 3. **Subtítulos SRT** (`.srt`)
```
1
00:00:00,000 --> 00:00:15,300
Este es el primer segmento de la transcripción.

2
00:00:15,300 --> 00:00:32,450
Continuación de la transcripción.
```

## ⚡ Automatización para Reuniones Frecuentes

### Script de Procesamiento Automático
Crea un archivo `procesar_reuniones.bat` (Windows):

```batch
@echo off
echo Procesando reuniones semanales...
call whisper-env\Scripts\activate

for %%f in (audios\*.m4a) do (
    echo Transcribiendo: %%~nxf
    python transcribir.py "%%f" --formato simple --carpeta "transcripciones_%%~nf"
)

echo ¡Todas las transcripciones completadas!
pause
```

### Programar con Task Scheduler (Windows)
1. Abrir **Task Scheduler**
2. Crear tarea básica
3. Acción: iniciar programa
4. Programa/script: `C:\ruta\a\tu\proyecto\procesar_reuniones.bat`
5. Programar: cada lunes a las 18:00

## 🔧 Solución de Problemas

### Error: "FFmpeg no encontrado"
**Solución:**
1. Descargar FFmpeg: https://github.com/BtbN/FFmpeg-Builds/releases
2. Extraer archivos
3. Agregar carpeta `bin` al PATH del sistema

### Error: "Módulo Whisper no encontrado"
**Solución:**
```bash
# Asegurarse que el entorno virtual está activado
whisper-env\Scripts\activate  # Windows
# o
source whisper-env/bin/activate  # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### Transcripción Muy Lenta
**Sugerencias:**
- Usar modelo más pequeño: `--modelo base`
- Dividir archivos largos (>2 horas)
- Verificar espacio en disco y memoria disponible

## 📈 Estadísticas de Rendimiento

| Duración Audio | Modelo Small | Modelo Medium | Requerimientos |
|----------------|--------------|---------------|----------------|
| 30 minutos | 2-4 minutos | 5-8 minutos | 4GB RAM |
| 1 hora | 4-8 minutos | 8-15 minutos | 4GB RAM |
| 2 horas | 8-15 minutos | 15-25 minutos | 8GB RAM |

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios significativos:

1. Fork del repositorio
2. Crear rama de características (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m "Describe tu cambio"`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Créditos

- **OpenAI Whisper** - Modelo de transcripción de audio
- **FFmpeg** - Procesamiento de archivos de audio
- **Python** - Lenguaje de programación

## 📞 Soporte

Para reportar problemas o solicitar características:
1. Revisar la sección de [Solución de Problemas](#-solución-de-problemas)
2. Abrir un [issue](../../issues) en el repositorio
3. Incluir: versión de Python, sistema operativo, y mensaje de error completo

---

**¡Listo para transcribir!** 🎉 Comienza con:
```bash
python transcribir.py "tu_audio.m4a"
```
