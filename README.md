# Billing Service

Service provides 4 urls to

* Register (`/api/register/`) to Register new user and account
* Purchase (`/api/purchase/`) to add finances to your account
* Withdrawal (`/api/withdrawal/`) to withdraw finances from your account
* Account (`/api/account/`) to check your balance

Also, there are a few urls, provided by oauth2 auth backend
https://github.com/jazzband/django-oauth-toolkit

### API documentation

#### Register endpoint

url: `/api/register/`
method: POST

permissions: Allow any http body example:

```
{
    "username": "test_user",
    "email": "test@test.com",
    "password": "1234567890qwerty"
}
```

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| username   | char       |                                                     |
| password   | char       | * Longer than 8 symbols * Contains digits & letters |
| email      | char       | Valid email                                         |

Example with curl

```
curl -i -X POST -H "Content-Type: application/json" http://0.0.0.0:8000/api/register/ -d '{"username": "fefe", "password": "qa1q1we23ew1", "email": "qwe@qweqw.com"}'
```

Response example

```
{
    "username":"fefe",
    "email":"qwe@qweqw.com",
    "client_id":"8FL6vq5pT8R5WuwlJ0sSPKkNPXihIj1VB43XTsPH",
    "client_secret":"GVTklxE4BvTo0juezEMC",
    "b64header":"OEZMNnZxNXBUOFI1V3V3bEowc1NQS2tOUFhpaElqMVZCNDNYVHNQSDpHVlRrbHhFNEJ2VG8wanVlekVNQw=="
}
```

#### Getting access token

To authorize the user, it is required to send POST request to URL http://0.0.0.0:8000/api/oauth2/token/ using client_id,
base64header, password from registration step

HTTP body

| Field name | Field type | Details                                             |
|------------|------------|-----------------------------------------------------|
| grant_type | char       | in current version `password` value only            |
| scope      | char       | List of scopes separated by space                   |
| username   | char       | Username                                            |
| password   | char       | Your password                                       |

Headers:

| Header name | Value                                                |
|-------------|------------------------------------------------------|
| grant_type  | Basic #{Your b64header from registration step}       |

Available scopes

| Scope name   | Description                                          |
|--------------|------------------------------------------------------|
| purchase     | Add finances from your account                       |
| withdrawal   | Withdraw finances from your account                  |
| account      | Check current balance & history                      |

Example:

```
curl -H 'Authorization: Basic QXdlN1Vrbmx3c0Nsb3JqMG1ObEUyR1Yya2JjODB2NFh5UmJCdFd6cjpxSUNlZks4bmxMa3hQOVJDZnpYWA==' -X POST http://0.0.0.0:8000/api/oauth2/token/ -d 'grant_type=password&scope=withdrawal purchase account&username=qwerty&password=qa1q1we23ew1'
```

Response example

```
{
    "access_token": "jlRRgXGKKAcO1ByrvH6VkpraiPu9Uv", 
    "expires_in": 36000, 
    "token_type": "Bearer", 
    "scope": "withdrawal purchase account", 
    "refresh_token": "Kt4NtfZGnT0sdU47dDOkfXjGgf2GOc"
}
```

`access_token` is required to interact with other endpoints.

#### Purchase endpoint

url: `/api/purchase/`
method: POST

permissions: Access token with `purchase` scope http body example:

```
{
    "amount": "10.00",
}
```

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| amount     | decimal    | > =0.01                                              |

Example with curl

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer QJdmFoPncnnZy3K1xbWhDyZyAXnBzf" http://0.0.0.0:8000/api/purchase/ -X POST  -d '{"amount": 123}'
```

#### Withdrawal endpoint

url: `/api/withdrawal/`
method: POST

permissions: Access token with `withdrawal` scope http body example:

```
{
    "amount": "-10.00",
}
```

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| amount     | decimal    | <=-0.01                                              |

Example with curl

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer QJdmFoPncnnZy3K1xbWhDyZyAXnBzf" http://0.0.0.0:8000/api/withdrawal/ -X POST  -d '{"amount": -123}'
```

#### Account endpoint

url: `/api/account/`
method: GET

permissions: Access token with `account` scope Curl example

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer QJdmFoPncnnZy3K1xbWhDyZyAXnBzf" http://0.0.0.0:8000/api/account/
```

Response example:

```
{
  "balance":"246.00",
  "username":"qwerty",
  "history":[
      {
        "date":"2021-11-08T17:36:06.477880",
        "operation_type":"withdrawal",
        "amount":"-123.00"
      },
      {
        "date":"2021-11-08T17:35:54.588030",
        "operation_type":"purchase",
        "amount":"123.00"
    },
    {
        "date":"2021-11-08T17:31:04.569239",
        "operation_type":"purchase",
        "amount":"123.00"
    },
    {
        "date":"2021-11-08T17:31:00.582667",
        "operation_type":
        "purchase","amount":"123.00"
    }]
}
```

### Make commands

* `make test` - run tests
* `make build` - build service
* `make up` - launch service
* `make linter` to launch pylint linter





todo list: 
* add refund logic
* add logging
* cover service layer with tests
