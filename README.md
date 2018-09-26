# PolyMap

### Do union and intersection on geojson polygons

###### Simple application using Django and Ajax with RESTful requests
![Github](https://preview.ibb.co/k7CwRp/polymap.png "Preview")

### Installation /development

###### Developed on linux with python3.6


#### Docker installation
- Install Docker: https://docs.docker.com/install/

- Get docker image:
  ```sh
  docker pull pederbg/polymap
  ```
- Clone repo and move to project folder
  ```sh
  git clone https://github.com/PederBG/PolyMap.git
  cd PolyMap
  ```

- Run docker image:
  ```sh
  ./docker/run_docker.sh
  ```

#### Normal installation
- Clone repo and install requirements:
  ```sh
  git clone https://github.com/PederBG/PolyMap.git
  cd PolyMap
  pip -r requirements.txt
  ```

- Create database and run server
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```



#### Navigate to http://localhost:8000
