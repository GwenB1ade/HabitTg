# How to launch the app
To get started, download the code from github. After that, go to the root folder of the project and write the following command in the command prompt

```
docker-compose up --build
```

After the containers are created, create a file named ".env". Filling in the dependencies:

```
BOT_KEY=your_toke

DB_NAME=postgres
DB_USER=admin
DB_PASS=root
DB_PORT=5432
DB_HOST=127.0.0.1

REDIS_PORT=6379
REDIS_HOST=127.0.0.1
REDIS_DB=0

BROKER_USER=admin
BROKER_PASS=root
BROKER_PORT=5672
BROKER_HOST=127.0.0.1
```

Now we need to get a token for your telegram bot. Go to the bot tag 'BotFather' and create a new bot and get a token. We insert this token into the BOT_KEY variable in the ".env" file.

now you can go to the "app" directory. We enter the following code into the command line:
```
celery -A tasks.tasks worker --loglevel=INFO
```
With this code, we launch the Celery application. All that remains is to launch the main application. To do this, we write this code in the new terminal:
```
python3 main.py
```

Congratulations, you have launched the app!