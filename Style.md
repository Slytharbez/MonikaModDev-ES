# 🎨 Estilo de Código (Coding Style)

El equipo de desarrollo oficial de MAS no tiene pautas de estilo extremadamente estrictas, pero aquí hay algunas convenciones que se recomienda seguir para mantener la consistencia en el repositorio:

## 🗂️ Sangría (Indentation)

* **Sangrías de cuatro espacios (Four-space indents).** No utilices tabulaciones.

## 🏷️ Etiquetas (Labels)

Los nombres de las etiquetas deben estar en minúsculas y separados por guiones bajos (`monika_twitter`).
Si utilizas muchas etiquetas para un subprograma o flujo relacionado, prefíjalas con `mas` y el nombre de tu subprograma (ej: `mas_coolfungame_flowstart`).

> [!NOTE]
> **Excepciones a esta regla:** Temas de conversación (topics), saludos y despedidas de Monika, aunque esto podría cambiar en el futuro.

Ciertos prefijos están reservados:

* 💬 `greeting` - Usado para saludos regulares.
* 🤝 `i_greeting` - Usado para saludos interactivos especiales.
* 📖 `ch30` - Usado para etiquetas clave del capítulo 30.
* 💚 `monika` - Usado para casi todos los temas (topics) de Monika.
* 🎭 `joke` - Usado para el sistema de chistes.
* 🃏 `m_joke` - También usado para el sistema de chistes.
* ✍️ `mas_poem` - Usado para el sistema del juego de poemas.
* 🎮 `game` - Usado para la mayoría de los minijuegos.
* 🔄 `vv` - Usado para material relacionado con actualizaciones.
* 📁 `v` - También usado para material relacionado con actualizaciones.
* 👋 `bye` - Usado para despedidas (farewells).

Puede haber más, así que en general, sé consciente de las etiquetas que utilizas.

## 📦 Almacenamiento (Store)

En Ren'Py, los `stores` son como espacios de nombres (namespaces), excepto que no se pueden tener anidados. Se recomienda agrupar datos relacionados, constantes y funciones en stores para evitar interferir con el espacio de nombres global.

Para crear un store:
```python
init python in mas_store_name:
    var1 = 1
    var2 = 2
    ...

# o bien
define mas_store_name.var1 = 1
define mas_store_name.var2 = 2
```

Para acceder a un store:
```python
store.mas_store_name.var1 = 1

# o bien
python:
    import store.mas_store_name as mas_store_name
    mas_store_name.var1 = 1
```

El proyecto utiliza varios stores diferentes para agrupar distintas clases de datos. Al decidir crear un nuevo store, asegúrate de que no esté ya en uso. Prefija los nombres de tus stores con `mas_`.

> [!IMPORTANT]
> `persistent` es similar a un store, pero es especial ya que se guarda en el disco duro. **Solo usa esto si necesitas guardar datos entre múltiples sesiones del juego.** Más sobre esto más adelante...

## ⚙️ Funciones

Si una función es muy específica de un subprograma o flujo, considera crearla dentro de un store e importarla cuando sea necesario. Si una función se puede generalizar para muchos casos de uso, entonces créala en un bloque `init python` normal (lo que la hace global).

**Prefija las funciones globales con `mas_`** (por ejemplo, `mas_nombre_funcion`).

Para la documentación, tanto los comentarios en bloque (`#`) como los docstrings (`"""`) están bien. No se exige una forma particular de documentar las funciones, pero indicar qué hace la función, sus variables de entrada y salida, qué devuelve y qué variables asume, sería un buen comienzo:

```python
def mas_someKindOfFunction(var1, var2, var3=None):
    """
    Esta función hace algún tipo de cosa. Úsala con precaución.

    ENTRADA (IN):
        var1 - valor de algo
        var3 - el valor máximo de algo
            (Predeterminado: None)

    SALIDA (OUT):
        var2 - contiene la referencia modificada a algo

    DEVUELVE (RETURNS):
        una copia de var2

    ASUME (ASSUMES):
        persistent.var4 
    """
```

> [!NOTE]
> Para los nombres de las funciones, tanto `camelCase` como `minúsculas_con_guion_bajo` (snake_case) están bien.

## 💾 Variables Persistentes (Persistent)

Este elemento similar a un store guarda datos en el disco y es la forma en que Ren'Py hace un seguimiento de los datos guardados.

> [!WARNING]
> Debido a que ya viene cargado con datos del juego base, **evita usarlo si puedes**. Por ejemplo, en lugar de usar un persistent para verificar si se ha visto un evento, usa `renpy.seen_label` o `seen_event`.

**Prefija todos los nombres de variables persistentes con `_mas_`.** (Actualmente el equipo oficial está en proceso de convertir todas las variables `persistent` creadas hasta ahora para que tengan este prefijo correctamente).

## 🔒 Constantes

Define constantes en lugar de valores literales cuando las uses múltiples veces. Usa `MAYÚSCULAS_CON_GUION_BAJO` para nombrarlas.

> [!IMPORTANT]
> **Una excepción a esto son los valores literales usados en pantallas (screens).** Si una pantalla **no** se llama con `nopredict`, entonces usa literales siempre que puedas, ya que Ren'Py optimiza mejor las pantallas que contienen valores literales directamente.

## 🔢 Variables

Por favor, haz que los nombres de las variables sean descriptivos. No es necesario que parezca Java, solo lo suficiente para que sea fácil entender qué almacena. El uso de abreviaturas o acrónimos está bien. Usa `minúsculas_con_guion_bajo` para nombrarlas.

## 💬 Comentarios

Por favor, escribe comentarios. Aunque Python es bastante legible por sí mismo, conocer el propósito general o los efectos globales de hacer algo resulta de gran ayuda.

## 📏 Longitud de Línea

De nuevo, no es algo estrictamente obligatorio, pero mantenlas dentro de un límite razonable. Se recomienda limitarse a 80 columnas, pero hasta unas 120 está bien.

> [!NOTE]
> **La excepción es el código de Ren'Py.** El código de Ren'Py no siempre se puede dividir en múltiples líneas sin romper su lógica.

## 📁 Recursos (Assets)

Cualquier recurso (imagen, audio, etc.) que utilices debe estar en la carpeta `mod_assets/`. Si tienes una gran cantidad de recursos, agrúpalos en una subcarpeta dedicada.

## 🔌 Librerías de Terceros (3rd-party Packages)

Si puedes resolverlo sin usar un paquete externo, hazlo sin el paquete externo. Las excepciones deben discutirse con el equipo de desarrollo oficial. Si la librería que deseas agregar pesa más de un megabyte, es casi seguro que **no** será permitida.
