# Car Pool system

A car pool system created for STAC Hackweek 2018. It is made keeping in mind the problem of transportation when you have to reach Mandi/ Other campus for some important work and the bus timings are not favourable. Someone might also be going to the same location using his/her personal vehicle and is willing to help but there is no existing system using which others can be informed. This project aims at solving this problem.

This project is made using Django 2.1 for backend.

## Deploy locally

1. Create a virtual environment and activate it.

```console
$ pyvenv hack
$ source hack/bin/activate
```

2. Install dependencies.

```console
$ pip install -r requirements.txt
```

3. Create the database.

```console
$ python manage.py migrate
```

6. Launch the development server:

```console
$ python manage.py runserver
```

7. Visit the url http://127.0.0.1:8000/ on your browser.
