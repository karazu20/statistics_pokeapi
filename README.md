# Statistics Poke-berries API

## Requerimientos previos
```sh
python versión 3.9 o  mayor
```

## Crear entorno virtual
Ubicados en la raíz del proyecto,  ejecutar sobre la consola los siguientes comandos:

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Levantar api

Dentro del entorno virtual previamente creado, se exporta la var de entorno de la API que apunta a la url de pokemon posterior se levanta la app:

```sh
export URL_POKE_API='https://pokeapi.co/api/v2'
python app.py
```

## Probar api
Con la api levantada, desde la consola usando curl se puede ejecutar con el siguiente comando:

```sh
curl --location 'http://127.0.0.1:5000/allBerryStats'
```

## Ejecutar pruebas unitarias
Dentro del entorno virtual ejecutamos:

```sh
pytest -c tests/pytest.ini
```
