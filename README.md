# Dockerizing Flask with Postgres, Gunicorn, and Nginx

### Clone the Repo



    $ git clone https://github.com/Hasib404/python-flask-boilerplate.git


### Create a virtual environment first,



    $ pip install virtualenv
    $ cd my-project/
    $ virtualenv venv
    $ source venv/bin/activate

### Development

Uses the default Flask development server.

1. Build the images and run the containers:

    ```
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:5000](http://localhost:5000). The "web" folder is mounted into the container and code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
