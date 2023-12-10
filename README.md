
# Proyecto CircleCI para Aplicación Python

Este repositorio contiene un archivo de configuración para CircleCI que establece un flujo de trabajo para construir, probar y desplegar una aplicación Python. A continuación se detalla cómo utilizar la aplicación y cómo está configurado el CI/CD en CircleCI.



# Uso de la Aplicación
La aplicación es una aplicación Python que utiliza un entorno PostgreSQL para almacenar datos multimedia. Aquí hay una guía paso a paso para trabajar con la aplicación:


## Configuración local para la aplicación

### Dependencias

- Python
- Postgresql
- pip

## Entorno

1. Crear un entorno virtual y actívarlo

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias

```
pip install -r requirements.txt
```

3. Crear base de datos y usuario 
```bash
createdb my_media
psql my_media
my_media=> CREATE ROLE multimedia WITH LOGIN CREATEDB PASSWORD 'm0v13';
```

4. Ejecutar las migraciones.

```
python manage.py migrate
```

##  Tests
las pruebas unitarias se pueden ejecutar con:

```
python manage.py test
```
## Pylint
linting de la aplicacion:

```
pylint my_media/ media_organizer/
```
## Ejecutar aplicacion
```
python manage.py runserver
```




# Configuración del CI/CD en CircleCI
Tareas Realizadas en el Flujo de Trabajo

1. Job code quality

Se define un job llamado "code-quality" que utiliza dos imágenes de Docker: una con Python 3.10.1 y otra con PostgreSQL 14.1. También establece una variable de entorno para el usuario de PostgreSQL.

```
jobs: 
  code-quality:
    docker:
      - image: cimg/python:3.10.1
      - image: cimg/postgres:14.1
        environment:
          POSTGRES_USER: multimedia
```



2. Checkout

Se realiza una operación de checkout, de esta manera obtenemos el código del repositorio.

```
    steps:
      - checkout
```

3.  Instalación de Dependencias


Se instalan las dependencias del proyecto utilizando pip.

```
      - run:
          name: install dependencies
          command: pip install -r requirements.txt
```

4. Linting

 Se ejecuta pylint en los directorios my_media/ y media_organizer/ y almacena los resultados en un archivo pylint.json. 

```
      - run:
          name: lint
          command: pylint my_media/ media_organizer/ 2>&1 | tee pylint.json
```



5. Pruebas con Cobertura

Se ejecuta las pruebas unitarias con cobertura y genera un informe XML y almacena los resultados de las pruebas en un directorio llamado test_results.

```
      - run:
          name: run tests with coverage
          command: coverage run --source=my_media,media_organizer manage.py test && coverage xml -o coverage.xml
      - store_test_results:
          path: test_results        
```


6. Análisis de SonarCloud:

Se Utiliza el orb de SonarCloud para realizar un análisis estático del código.
```
orbs:
  sonarcloud: sonarsource/sonarcloud@2.0.0
---
      - sonarcloud/scan
```
![Alt text](<Captura desde 2023-12-10 23-21-46.png>)
https://sonarcloud.io/summary/new_code?id=jeffersonnc_ci-cd-project

7. Informe de Cobertura

 se Muestra un informe de cobertura en la consola y almacena el informe de covertura en un artefacto
```
      - run:
          name: show coverage report
          command: coverage report -m
      - store_artifacts:
          path: coverage.xml

```


8. Build and Push Job

Definimos otro job que construye la imagen de Docker del proyecto y la sube a Docker Hub. Los pasos incluyen:

- Docker Setup:
 Utiliza una imagen Docker con Python 3.10.1.

- Configuración Remota de Docker:
 Se configura el entorno para ejecutar comandos de Docker, permite el almacenamiento en caché de capas de Docker para acelerar el proceso de construcción.

- Inicio de Sesión en Docker Hub:
 Inicia sesión en Docker Hub con las credenciales proporcionadas como variables de entorno en CircleCI.

- Construcción de Imagen: Construye la imagen Docker con la etiqueta jeffnacato/circle_ci_python:$CIRCLE_BRANCH.

- Push a Docker Hub: Sube la imagen Docker recién construida a Docker Hub.
```
  build-and-push:
    docker:
      - image: cimg/python:3.10.1
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run: |
          echo "$DOCKERHUB_PASSWORD" | docker login --username $DOCKERHUB_USERNAME --password-stdin
      - run: docker build -t jeffnacato/circle_ci_python:$CIRCLE_BRANCH .
      - run: docker push jeffnacato/circle_ci_python:$CIRCLE_BRANCH
```

9. build-and-test-workflow y deploy


- build-and-test-workflow: Este flujo de trabajo se activa en cada confirmación y ejecuta el trabajo code-quality seguido por el trabajo build-and-push. La construcción y el push a Docker Hub se realizan solo si el trabajo de calidad del código es exitoso.

- deploy: Este trabajo está configurado para ejecutarse solo en la rama main. Desencadena el trabajo build-and-push solo cuando se confirma en la rama principal.

```
workflows:
  build-and-test-workflow:
    jobs:
      - code-quality:
          context: SonarCloud
      - build-and-push:
          requires:
            - code-quality
  deploy:
    jobs:
      - build-and-push:
          filters:
            branches:
              only:
                - main

```

imagen del docker en dockerhub

![Alt text](<Captura desde 2023-12-10 23-48-23.png>)

10. Analisis de vulnerabilidades

Ademas ha conectado el repositorio con la aplicacion Snyk para el analisis de vulnerabilidades

![Alt text](<Captura desde 2023-12-10 23-40-31.png>)


## notas

no he llegado a completar como me gustaria el proyecto, ya que aun que he visto las clases grabadas ademas de buscar informacion se me ha complicado comprender como integrar GIT FLOW Y ARGO CD al proyecto, aun que entiendo correctamente la funcion de estas 2 aplicaciones y como pueden ayudar al proyecto, las pruebas que he realizado no me daban un resultado coherente.

completare y mejorare el proyecto a lo largo de la semana

gracias Xavi por todo lo enseñado










