# Traducciones exclusivas para el sistema de logs espejo en Android
# Esto solo afecta la copia pública en /storage/emulated/0/Monika After Story/log/

init -998 python:
    _register_log_translations("spanish", {
        # traceback.txt strings base
        "I'm sorry, but an uncaught exception occurred.": "Lo sentimos, pero ha ocurrido una excepción no controlada.",
        "-- Full Traceback ------------------------------------------------------------": "-- Rastreo Completo ------------------------------------------------------------",
        "Full traceback:": "Rastreo Completo:",
        
        # traceback.txt context (renpy.game.exception_info)
        "While running game code:": "Mientras se ejecutaba el código del juego:",
        "While loading the script.": "Mientras se cargaba el script.",
        "Before loading the script.": "Antes de cargar el script.",
        "After loading the script.": "Después de cargar el script.",
        "While executing init code:": "Mientras se ejecutaba el código de inicialización:",
        "After initialization, but before game start.": "Después de la inicialización, pero antes de iniciar el juego.",
        
        # log.txt extras (opcional)
        "Bootstrap to the start of init.init took": "El Bootstrap hasta el inicio de init.init tomó",
        "Early init took": "El init temprano tomó",
        "Loader init took": "El init del cargador tomó",
        "Loading error handling took": "La carga del manejo de errores tomó",
        "Loading the script took": "La carga del script tomó",
        "Loading the save directory took": "La carga del directorio de guardado tomó",
        "Loading the persistent data took": "La carga de datos persistentes tomó",
        "Loading scripts took": "La compilación/carga de scripts tomó",
        "Total time until interface ready:": "Tiempo total hasta que la interfaz estuvo lista:",
        "Init to the start of the first screen took": "Desde el inicio hasta la primera pantalla tomó",
        
        # Headers y sistema base
        "Welcome to Ren'Py": "Bienvenido a Ren'Py",
        "Platform:": "Plataforma:",
        "Screen sizes:": "Tamaños de pantalla:",
        "An exception has occurred.": "Ha ocurrido una excepción.",
        
        # Traceback structure
        ", line ": ", línea ",
        ", in ": ", en ",
        "  File \"": "  Archivo \"",
        "Exception: ": "Excepción: ",
        "ScriptError: ": "Error en Script: ",
        "ParseError: ": "Error de Análisis: ",
        "TypeError: ": "Error de Tipo: ",
        "AttributeError: ": "Error de Atributo: ",
        "SyntaxError: ": "Error de Sintaxis: ",
        
        # Arranque y Entorno
        "Unknown platform.": "Plataforma desconocida.",
        "Manufacturer": "Fabricante",
        "model": "modelo",
        "Screen diagonal is": "La diagonal de la pantalla es",
        "inches.": "pulgadas.",
        "Version:": "Versión:",
        "Mobile search paths:": "Rutas de búsqueda móvil:",
        
        # Tiempos de Carga (Loading & Init)
        "Loading error handling took": "La carga del manejo de errores tomó",
        "Loading script took": "La carga del script tomó",
        "Loading save slot metadata took": "La carga de metadatos de las ranuras de guardado tomó",
        "Loading persistent took": "La carga de persistente tomó",
        "Set script version to:": "Versión del script configurada a:",
        "Running init code took": "La ejecución del código de inicialización tomó",
        "Loading analysis data took": "La carga de datos de análisis tomó",
        "Analyze and compile ATL took": "El análisis y compilación de ATL tomó",
        "Reloading save slot metadata took": "La recarga de metadatos de guardado tomó",
        "Index archives took": "La indexación de archivos tomó",
        "Dump and make backups took": "El volcado y creación de copias de seguridad tomó",
        "Cleaning cache took": "La limpieza de la caché tomó",
        "Making clean stores took": "La creación de tiendas limpias tomó",
        "Initial gc took": "La recolección de basura inicial tomó",
        "DPI scale factor:": "Factor de escala DPI:",
        "Creating interface object took": "La creación del objeto de interfaz tomó",
        "Cleaning stores took": "La limpieza de tiendas tomó",
        "Init translation took": "La inicialización de la traducción tomó",
        "Build styles took": "La construcción de estilos tomó",
        "Load screen analysis took": "La carga del análisis de pantallas tomó",
        "Analyze screens took": "El análisis de pantallas tomó",
        "Save screen analysis took": "El guardado del análisis de pantallas tomó",
        "Prepare screens took": "La preparación de pantallas tomó",
        "Save pyanalysis. took": "El guardado de pyanalysis tomó",
        "Save bytecode. took": "El guardado del bytecode tomó",
        "Running _start took": "La ejecución de _start tomó",
        "Interface start took": "El inicio de la interfaz tomó",
        
        # Renderizado (OpenGL / GLES)
        "Initializing gles2 renderer:": "Inicializando el renderizador gles2:",
        "primary display bounds:": "Límites de pantalla principal:",
        "swap interval:": "Intervalo de intercambio:",
        "frames": "cuadros",
        "Fullscreen mode.": "Modo de pantalla completa.",
        "Vendor:": "Vendedor:",
        "Renderer:": "Renderizador:",
        "Display Info:": "Info de Pantalla:",
        "Could not open": "No se pudo abrir",
        "Maximum texture size:": "Tamaño máximo de textura:",
        "Hid presplash.": "Presplash ocultado.",
        
        # Mensajes de Logs personalizados o Warnings
        "WARNING: logging.handlers not found. Using safe fallback.": "ADVERTENCIA: logging.handlers no encontrados. Usando método seguro.",
        "Saving to": "Guardando en",
    })
