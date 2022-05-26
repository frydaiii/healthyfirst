# API document
## Register
### api/users/
* method POST
* body x-www-form-urlencoded
  * username
  * password
* return 
```json
{
    "username": "",
    "email": "",
    "groups": []
}
```
## Get user information
### api/users/[username]
* method GET
* header Authorization Bearer jwt_token
## Login
* api/token
* method POST
* body x-www-form-urlencoded
  * username
  * password
* return
```json
{
  "refresh": "refresh_token",
  "access": "jwt_token"
}
```
## Get new access token
* api/token/refresh 
* method POST
* body x-www-form-urlencoded
  * refresh
* return
```json
{
  "access": "jwt_token"
}
```
