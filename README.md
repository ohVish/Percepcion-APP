# SCORE APP
## Descripción
Aplicación destinada a la digitalización de partituras. Para ello la aplicación dispone de dos funciones principales:

- El reconocimiento sonoro de una melodía y la generación automática de la notación musical que le corresponde.
- El reconocimiento de imágenes digitales de partituras, de modo que podamos identificar que nota y que duración tiene de forma automatizada a partir de una imagen.

Estas dos funciones de la aplicación comprenden los dos grandes objetivos que tratamos de cumplir con ella.

## Requisitos
Para realizar la aplicación hemos empleado los siguientes componentes software:
- Python 3, para la creación de una interfaz de usuario amigable y que sea posible integrarla fácilmente con otra aplicación ya desarrollada.
- El framework Kivy de Python 3, para lograr una interfaz multiplataforma para que la aplicación sea independiente del sistema operativo.
- El framework de OpenCV, para la captura de imágenes a través de la interfaz de Python.
- La biblioteca sounddevice para la captura de la melodía a partir de la interfaz de Python.
- La biblioteca desarrollada por Mathworks para ejecutar código MatLab desde Python.
- MatLab, para la creación de todo el proceso de reconocimiento de audio y de visión artificial debido a que es el lenguaje de programación empleado en la asignatura, y su facilidad para realizar estas tareas.
- El software Lilypond, que lo integramos junto a la interfaz de Python para generar las partituras autogeneradas por nuestro algoritmo (Para indepencia del sistema, empleamos Docker).
