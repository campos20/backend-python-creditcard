import logging
import time

import requests
from requests.models import Response

# User login at http://localhost:8092/realms/credit-card-local/account/

DEFAULT_REALM = "credit-card-local"
DEFAULT_CLIENT_ID = "credit-card"
KEYCLOAK_HOST = "http://localhost:8092"
KEYCLOAK_ADMIN = "keycloak"
KEYCLOAK_ADMIN_PASSWORD = "keycloak"
WAIT_LIMIT = 120

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

# Global
ACCESS_TOKEN = None


def get_headers():
    return {"Authorization": "Bearer %s" % ACCESS_TOKEN}


def get_master_token():
    log.info("Get master access token")

    url = "%s/realms/master/protocol/openid-connect/token" % KEYCLOAK_HOST
    data = {
        "grant_type": "password",
        "username": KEYCLOAK_ADMIN,
        "password": KEYCLOAK_ADMIN_PASSWORD,
        "client_id": "admin-cli",
    }
    response = requests.post(url, data=data)

    status_code = response.status_code
    if status_code != 200:
        raise Exception("Invalid response code: %s" % status_code)

    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json()["access_token"]


def analyze_response(response: Response):
    status_code = response.status_code

    if status_code < 200 or status_code > 299:
        raise Exception("Invalid response code: %s" % status_code)


def analyze_creation_response(response: Response, entity):
    status_code = response.status_code

    if 200 <= status_code <= 299:
        if entity:
            log.info("%s created" % entity)
        else:
            log.info("Success")
    elif status_code == 409:
        log.info("%s already exists" % entity)
    else:
        raise Exception("Invalid response code: %s" % status_code)


def create(url, data, entity):
    headers = get_headers()
    response = requests.post(url, json=data, headers=headers)
    log.info(response)
    analyze_creation_response(response, entity)


def create_realm():
    log.info("Create realm %s" % DEFAULT_REALM)

    url = "%s/admin/realms" % KEYCLOAK_HOST
    data = {"enabled": True, "realm": DEFAULT_REALM}
    create(url, data, "Realm")


def default_put(url, data):
    headers = get_headers()
    response = requests.put(url, json=data, headers=headers)

    analyze_response(response)


def create_client():
    log.info("Create client")

    url = "%s/admin/realms/%s/clients" % (KEYCLOAK_HOST, DEFAULT_REALM)
    data = {
        "protocol": "openid-connect",
        "clientId": DEFAULT_CLIENT_ID,
        "name": "",
        "description": "",
        "publicClient": True,
        "authorizationServicesEnabled": False,
        "serviceAccountsEnabled": False,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": True,
        "standardFlowEnabled": True,
        "frontchannelLogout": True,
        "alwaysDisplayInConsole": False,
        "attributes": {
            "oauth2.device.authorization.grant.enabled": False,
            "oidc.ciba.grant.enabled": False,
        },
        "redirectUris": ["http://localhost:3000", "http://localhost:3000/*"],
    }
    create(url, data, "Client")


def create_user(username):
    log.info("Create user")

    url = "%s/admin/realms/%s/users" % (KEYCLOAK_HOST, DEFAULT_REALM)
    data = {
        "email": "",
        "emailVerified": True,
        "enabled": True,
        "firstName": username,
        "groups": [],
        "lastName": "",
        "requiredActions": [],
        "username": username,
        "credentials": [{"type": "password", "value": username, "temporary": False}],
    }
    create(url, data, "Users")


def change_token_timeout():
    log.info("Change token duration")
    url = "%s/admin/realms/%s" % (KEYCLOAK_HOST, DEFAULT_REALM)

    data = {
        "id": DEFAULT_REALM,
        "realm": DEFAULT_REALM,
        "accessTokenLifespan": 3600,
    }

    default_put(url, data)


def wait_for_keycloak_start():
    log.info(f"Waiting for the server to start in {KEYCLOAK_HOST}")
    for i in range(1, WAIT_LIMIT + 1):
        try:
            requests.get(KEYCLOAK_HOST)
            log.info("Keycloak server started")
            return
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if i == WAIT_LIMIT:
                raise e
        log.info("." * i)
        time.sleep(3)
    raise Exception("Fail waiting for keycloak")


def main():
    wait_for_keycloak_start()
    get_master_token()
    create_realm()
    create_client()
    change_token_timeout()
    create_user("admin")

    log.info("Success")


if __name__ == "__main__":
    main()
