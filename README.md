# BookStoreWeb

## Video demo
Video demo [here](https://www.youtube.com/watch?v=BedY-nFctMc)

## Installation

### Download and install Docker Desktop
Download and install Docker [here](https://www.docker.com/products/docker-desktop/)

### Run the project
1. Launch Docker Desktop
2. Open a terminal or command prompt.
3. Run the following command:
```python 
cd bookstoreweb
docker-compose up --build
```
4. When the containers are running, open a new terminal and execute the following command to migrate the database:
```python 
docker-compose exec web python manage.py makemigrations webapp
docker-compose exec web python manage.py migrate
```
5. Import the available data into the database using the following command (This process may take around 20 - 30 minutes):
```python 
docker-compose exec web python manage.py runscript import_data -v 2
```
6. Train an AI model for the recommendation system or update the recommendation model based on the latest data using the following command:
```python 
docker-compose exec web python ml_model.py
```
7. Access the website via the following link: http://localhost:8000/
