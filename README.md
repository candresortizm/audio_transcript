# Ejecución del proyecto para Analisis de audio 2 personas
Se recomienda el uso de un entorno virtual (venv) para el manejo de dependencias entre proyectos. Documentación en: https://docs.python.org/3/tutorial/venv.html .

## Creación del entorno virtual
Se sugiere el entorno de un entorno virtual para el manejo de las librerí­as. El siguiente código crea un entorno virtual llamado env, se recomienda ese nombre para que sea ignorado por el .gitignore
```
python -m venv env
```

## Activación del entorno virtual
Para activar el entorno virtual se ejecuta el siguiente comando (en windows):
```
env\Scripts\activate
```

## Instalación de dependencias
Ejecutar el siguiente código para instalar las dependencias que requiere el proyecto:
```
pip install -r .\requirements.txt
```
Nota: si se sugiere la actualización de pip, entonces actualizarlo.


## Comando para ejecutar el servidor
Para la ejecución del servidor ejecutar el siguiente comando:
```
python src\app.py
```

acceder desde un navegador al la dirección http://localhost:5000


## TODO
- Continuar con la imagen de docker
- Manejo de excepciones
- hacer set de pruebas
