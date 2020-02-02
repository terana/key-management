# Authentication
## Login
Logs an existing user in.
### URL
`POST /rest-auth/login/`
### Body
```json
{
  "password": "johnpassword",
  "username": "john"
}
```
### Response
In headers, will return set-cookie with session token and csrf token.

## Logout
Logout the user.

### URL
`POST /rest-auth/logout/`

# Secrets management
## Create a secret 
### URL
`POST /api/secret/CreateSecret`
### Body
```json
{
  "key": "key",
  "value": "value"
}
```

## Get a secret
### URL
`GET /api/secret/GetSecret?key=key`
### Response 
```json
{
  "key": "key",
  "value": "value"
}
```

## Delete a secret
### URL
`DELETE /api/secret/DeleteSecret`
### Body 
```json
{
  "key": "key",
  "value": "value"
}
```
