# backend-python-creditcard

Sample backend in python for credit cards.

Currently, this project is composed of a backend only. You can navigate to the folder `app` for details.

## TODOs

These TODOs were left on purpose due to time restrictions:

- Authentication and authorization (we could use keycloak or natively sign a token)
- Tests change the development database (this can be fixed with python-dotenv, creating a different file for the test database with sqlite and maybe seeding/reseting the database before tests)
