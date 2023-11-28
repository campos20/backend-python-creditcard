# backend-python-creditcard

Sample backend in python for credit cards.

Currently, this project is composed of a backend only. You can navigate to the folder `app` for details.

## Get Started

- Sart containers (dev and testing databases)

```bash
docker-compose up -d
```

You will be able to connect to the local database by using your favorite database tool.

```
host=localhost
port=5432
database=credit_card
username=root
password=pass
```

Testing database uses the port 5433. You can find this configuration by checking `.env` file (in the app folder) and also `docker-compose.yaml`.

- Navigate to the `app` folder and follow the instructions in the README.md there.
