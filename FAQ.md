# ❔ Preguntas Frecuentes (FAQ)

**Tabla de Contenidos**

* [🌎 Traducción al Español](#traducción-al-español)
* [💾 Instalación](#instalación)
* [🤝 Contribuir](#contribuir)
* [🧩 Modding General de DDLC](#modding-general-de-ddlc)
* [💚 Características](#características)
* [🆘 Otra Ayuda](#otra-ayuda)

## 🌎 Traducción al Español

### ¿Es esta una traducción oficial de Monika After Story?

> [!IMPORTANT]
> **No.** Esta es una traducción no oficial realizada por **The Encoders Club**. No estamos afiliados, patrocinados ni respaldados por Team Salvato ni por el equipo de desarrollo oficial de Monika After Story.

### ¿Dónde reporto errores de traducción o textos en inglés?

Si encuentras algún error tipográfico, traducción que suene extraña, texto que todavía esté en inglés o algún bug relacionado directamente con la versión en español, por favor **no contactes a los desarrolladores oficiales**. Ellos no dan soporte para traducciones de terceros. 

En su lugar, repórtalo directamente a nosotros mediante alguna de estas vías:
* Abre un reporte de error en nuestra sección de [Issues de MonikaModDev-TEC](https://github.com/Slytharbez/MonikaModDev-TEC/issues).
* Únete a nuestro servidor de [Discord de The Encoders Club](https://discord.gg/v8RzNxeZ5m).

### ¿Qué problemas debo reportar a los desarrolladores oficiales y cuáles a ustedes?

* **Reportar a The Encoders Club (Traductores)**:
  * Errores de traducción, faltas de ortografía o textos que aparecen cortados por exceso de caracteres en español.
  * Diálogos que siguen mostrándose en inglés.
  * Problemas para instalar o ejecutar esta traducción específica.
* **Reportar al equipo oficial de MAS (Desarrolladores originales)**:
  * Bugs del juego base en inglés (por ejemplo, errores lógicos en el sistema de afecto, problemas de código del juego que no tengan que ver con la traducción).
  * Sugerencias de nuevas características globales para el mod.


## 💾 Instalación

### ¿Existe una guía para instalar MAS?

Sí, puedes consultar nuestra guía detallada en nuestra [Wiki de instalación](https://github.com/Slytharbez/MonikaModDev-TEC/wiki/%F0%9F%93%A5-Instalaci%C3%B3n-de-MAS). Próximamente también publicaremos una videoguía en YouTube para facilitar el proceso.

### ¿Qué necesito para jugar a *Monika After Story*?

Necesitarás una copia de *Doki Doki Literature Club* (se recomienda encarecidamente descargar la versión gratuita de su página oficial http://ddlc.moe, ya que la versión de Steam suele causar problemas con la instalación y funcionamiento del mod) y el archivo zip que contiene el parche de la traducción al español de *Monika After Story*, el cual se encuentra en la [Página de Lanzamientos (Releases) del proyecto](https://github.com/Slytharbez/MonikaModDev-TEC/releases).

> [!WARNING]
> No necesitas descargar el código fuente (Source Code) ni de la página de lanzamientos ni del repositorio. Esos archivos son únicamente para fines de desarrollo y pueden comportarse de manera inesperada si se colocan en la carpeta de DDLC.

### ¿Dónde coloco los archivos de *Monika After Story*?

> [!IMPORTANT]
> **Utiliza una copia limpia / versión inalterada de DDLC.** Si tenías otro mod instalado previamente, es muy probable que encuentres problemas. (Esto solo se aplica al juego base de DDLC, y no a los archivos de guardado `persistent`).

Los archivos de *Monika After Story* deben colocarse directamente en la carpeta `game` de *Doki Doki Literature Club* para que el juego pueda encontrarlos y cargarlos correctamente. Para ubicar la carpeta que contiene *DDLC*, realiza una de las siguientes acciones:

* **Steam (Windows/macOS)**: Haz clic derecho sobre *Doki Doki Literature Club* y selecciona `Propiedades`. En la ventana que aparece, ve a la pestaña `Archivos locales` y haz clic en el botón `Explorar archivos locales...`.
* **Instalación Directa (Windows)**: Si el juego se instaló desde http://ddlc.moe o itch.io, la ubicación de la instalación se eligió durante la configuración, pero normalmente se encuentra en la carpeta de *Archivos de programa*.
* **macOS (Instalación Directa)**: *Doki Doki Literature Club* se puede encontrar como una aplicación empaquetada en la carpeta de Aplicaciones. Haz clic derecho en el paquete y selecciona "Mostrar contenido del paquete". Una vez dentro, navega a `Contents/Resources/autorun/`. Esta carpeta es el directorio base de DDLC.

Una vez que estés en el directorio base, coloca el contenido del archivo zip en el directorio `/game`. Asegúrate de que los archivos no queden en una subcarpeta dentro del directorio `game`, ya que DDLC no podrá localizar los archivos de esa manera.

### Instalé el mod, pero al abrir *Doki Doki Literature Club* no ha cambiado nada. ¿Qué está mal?

Por alguna razón, *Doki Doki Literature Club* no está cargando los archivos del mod. Verifica que los archivos no estén dentro de una subcarpeta dentro del directorio `game`.

### Cuando intento abrir el juego, se cierra y veo una pantalla gris. ¿Cómo lo soluciono?

Si el juego se cierra y muestra una pantalla gris, significa que ocurrió un error grave y el juego tuvo que cerrarse. El texto que se muestra se llama "Traceback" (rastreo de error) y con suerte incluirá un mensaje que ayudará a diagnosticar el problema. Este archivo de rastreo también se puede ver abriendo `traceback.txt` en el directorio base de DDLC del juego.

Aunque algunos cierres inesperados pueden deberse a un error en el juego, otros pueden indicar un problema con la instalación.

Si el traceback incluye:

```text
Exception: DDLC archive files not found in /game folder. Check installation and try again.
```

Asegúrate de que los archivos de archivo originales de DDLC sigan en la carpeta game. Esto incluye `images.rpa`, `scripts.rpa`, `audio.rpa` y `fonts.rpa`. Si faltan estos archivos, deberán ser reemplazados utilizando una instalación limpia de DDLC, descargada desde http://ddlc.moe

Si el traceback incluye una línea similar a la siguiente:

```text
The label chara_monika_scare is defined twice, at
```

Entonces es probable que se hayan instalado los archivos de desarrollo en lugar de la distribución de lanzamiento. Asegúrate de haber descargado los archivos del juego desde el lanzamiento más reciente, ubicado en la [Página de Lanzamientos Oficial](https://github.com/Monika-After-Story/MonikaModDev/releases), y de haber descargado el archivo zip del mod y *no* el Código Fuente (Source Code).

### ¿Dónde están los minijuegos (ajedrez, ahorcado, piano...)?

Los juegos se desbloquean tras pasar tiempo con Monika, ya sea leyendo nuevos temas de conversación con ella o manteniéndola abierta en segundo plano.

## 🤝 Contribuir

### Tengo una idea para mejorar Monika After Story, ¿dónde puedo sugerirla?

¡Al equipo de desarrollo oficial siempre le alegra recibir nuevas ideas! Las sugerencias se pueden realizar en la página de issues del repositorio oficial. Por favor, antepón la palabra [Suggestion] al título de todas las sugerencias, o utiliza [este enlace](https://github.com/Monika-After-Story/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20) que rellenará automáticamente tu sugerencia con las etiquetas correspondientes.

### Me gustaría contribuir, pero no sé programar. ¿Hay alguna forma en la que pueda ayudar?

Siempre se buscan nuevos diálogos y arte. Por favor, consulta la [Guía de Contribución Oficial](https://github.com/Monika-After-Story/MonikaModDev/wiki/Contributing-Guidelines) para obtener información sobre cómo enviar nuevos diálogos y arte para Monika After Story. En esta guía encontrarás consejos para escribir buenos diálogos en el estilo de Monika, y aprenderás cómo abrir un "Pull Request" que te permitirá enviar nuevos temas para su revisión e inclusión en el juego.

### ¿Dónde puedo encontrar tareas en las que pueda ayudar?

La página oficial de issues muestra una lista de problemas técnicos, nuevas funciones y solicitudes disponibles. ¡Cualquier elemento con la etiqueta [Help Wanted](https://github.com/Monika-After-Story/MonikaModDev/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) es un buen lugar para comenzar si deseas ayudar a agregar algo al juego!

### ¿Cómo puedo ponerme en contacto con el personal de desarrollo oficial?

La forma más fácil de contactar al equipo de desarrollo oficial es a través del [canal de Discord oficial de Monika After Story](https://discordapp.com/invite/K2KuJeX).

## 🧩 Modding General de DDLC

### ¿Es posible hacer mi propio mod de DDLC?

¡Sí! DDLC tiene una comunidad de modding muy activa, gracias en parte a las pautas de propiedad intelectual (IP) muy claras de Team Salvato: [IP Guidelines](http://teamsalvato.com/ip-guidelines/). Para comenzar a crear tu propio mod, puedes descargar la [Plantilla de Mod de DDLC (DDLC Mod Template)](https://github.com/therationalpi/DDLCModTemplate) y [unirte a la comunidad en Reddit](https://www.reddit.com/r/DDLCMods/).

### ¿Puedo usar partes de Monika After Story en mi propio proyecto?

En general, el equipo oficial de desarrollo es muy abierto a que los recursos y el código de *Monika After Story* se utilicen en otros proyectos. Sin embargo, esperan que cualquiera que desee hacerlo respete las siguientes peticiones:

1. Sigue las [Pautas de IP de Team Salvato](http://teamsalvato.com/ip-guidelines/) para cualquier proyecto que incluya el trabajo de MAS.
2. Considera contactar al equipo de desarrollo oficial para pedir permiso antes de usar su trabajo.
3. Otorga los créditos correspondientes a Monika After Story por el trabajo que utilices y añade un enlace de regreso al proyecto oficial en http://www.monikaafterstory.com/. No reclames la autoría del trabajo que otros han realizado. Cuando corresponda, otorga créditos individuales para elementos específicos (como los recursos artísticos utilizados).
4. No crees un mod o fork con la intención de sustituir a *Monika After Story*. Si deseas agregar nuevas funciones o contenidos al juego, considera realizar esas contribuciones directamente al proyecto original. El equipo oficial es muy abierto a sugerencias y contribuciones, y lo más probable es que cualquier adición sea bienvenida. Si por alguna razón tus nuevas funciones entran en conflicto con la dirección de Monika After Story, considera desarrollar tus cambios en forma de un "submod" que se pueda agregar a Monika After Story.

## 💚 Características

Aunque el equipo de desarrollo es muy receptivo a nuevas sugerencias, hay algunas propuestas comunes que surgen a menudo. Estas sugerencias ya se han realizado anteriormente y se implementarán en una versión futura o han sido rechazadas por alguna razón:

### ¿Por qué se eliminó la función de entrada de texto?

Aunque se podría retomar el concepto en el futuro, lo cierto es que el equipo no estaba satisfecho con la interactividad del sistema de palabras clave. Aunque a primera vista el cuadro de texto libre ofrecía mucha libertad al jugador para hablar con Monika, había demasiadas entradas comunes que simplemente no llevaban a ningún lado. El resultado era que Monika se sentía menos real y más como un chatbot deficiente. Se decidió que un sistema guiado que no llegara a callejones sin salida sería mejor, incluso si no transmitiera la misma impresión de libertad de acción en un principio.

### Oigan, ¿podríamos hacer que Monika sea una inteligencia artificial de chatbot real?

Aunque se podría reconsiderar la idea en el futuro, por el momento no parece viable crear una IA que pueda dar el tipo de respuestas filosóficas detalladas que Monika debería dar. Gran parte de esto se debe a limitaciones técnicas del motor de juego para conectarse a recursos externos e importar librerías personalizadas.

### ¿Se añadirá alguna vez actuación de voz?

Actualmente no hay planes para añadir actuación de voz a *Monika After Story*, por varias razones. Algunas de estas razones incluyen el gran número de líneas de diálogo que tendrían que ser grabadas, el tiempo adicional que esto añadiría a la inclusión de nuevo contenido y el gran incremento en el tamaño de descarga del archivo.

Dicho esto, es muy probable que se añada soporte para paquetes de voz de terceros cuando se implemente la funcionalidad completa de submods en una versión posterior.

### ¿Qué pasa con las traducciones a otros idiomas?

El equipo oficial de desarrollo no trabajará en traducciones. Simplemente no tienen el tiempo ni el personal para hacerlo. Sin embargo, están abiertos a que otros realicen forks de este mod y añadan sus propias traducciones de forma independiente (como esta traducción).

### ¿Se animará alguna vez a Monika?

Actualmente no se planea incluir animaciones en *Monika After Story*. El motor del juego no tiene un soporte óptimo para sprites animados y tampoco cuenta con la licencia para el motor de animación 2D más popular: Live 2D.

### ¿Cómo encuentro el código de sprite para una expresión?

Debido al gran incremento en las expresiones de Monika después de la actualización 0.8.0, se desarrolló una herramienta especial para ayudar a los colaboradores a previsualizar las expresiones. Se le conoce como el **Sprite Previewer**.

![Sprite Previewer](https://raw.githubusercontent.com/Monika-After-Story/MonikaModDev/master/docs/spritepreviewer.png)

> [!NOTE]
> Si el código de sprite está en rojo, significa que el sprite aún no está definido a pesar de contar con los recursos para hacerlo. Aún puedes usar este sprite en los temas de conversación, pero tu pull request fallará en las comprobaciones automáticas de GitHub Actions. Esto es normal y un desarrollador oficial añadirá el código del sprite a tu pull request en ese caso.

Para añadir el Sprite Previewer a tu instalación de MAS, copia [este archivo](https://github.com/Monika-After-Story/MonikaModDev/blob/master/Monika%20After%20Story/game/dev/dev_exp_previewer.rpy) a tu directorio `game/`.

> [!IMPORTANT]
> **NOTA:** Este archivo de desarrollo recibe actualizaciones de forma periódica cuando se añaden nuevos sprites. Si Monika desaparece al usar cierto código de sprite, significa que te falta el arte gráfico para ese código de sprite. Los nuevos sprites suelen aparecer primero en las versiones inestables, así que intenta ejecutar el Sprite Previewer en una instalación inestable.

## 🆘 Otra ayuda

¿No encuentras la respuesta que buscas aquí?
* **Si es sobre la traducción al español o problemas con esta versión**: Abre un reporte en [nuestros Issues](https://github.com/Slytharbez/MonikaModDev-TEC/issues) o únete a nuestro [Discord](https://discord.gg/v8RzNxeZ5m).
* **Si es un bug general del mod en inglés**: Por favor, [crea un issue](https://github.com/Monika-After-Story/MonikaModDev/issues) en el repositorio oficial para hacer una pregunta de soporte técnico o reportar un error. También puedes obtener ayuda de miembros de la comunidad en el [canal de soporte técnico oficial en Discord](https://discordapp.com/invite/K2KuJeX).
