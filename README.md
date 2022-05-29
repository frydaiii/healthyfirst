# API document
## Register
### api/users/
* method POST
* body x-www-form-urlencoded
  * id
  * username
  * password
  * password2
  * first_name
  * last_name
  * role: "MN" or "ST"
  * id_area
  * email
* return 
```json
{
    "username": "",
    "email": "",
    "groups": [], 
    "first_name": "",
    "last_name":  "",
    "role": "",
    "id_area": ""
}
```
## Login
### api/token/
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
* api/token/refresh/
* method POST
* body x-www-form-urlencoded
  * refresh
* return
```json
{
  "access": "jwt_token"
}
```
## Get user information
### api/users/[username]
* method GET
* header Authorization Bearer jwt_token
* return
```json
{
    "username": "",
    "email": "",
    "groups": [],
    "first_name": "",
    "last_name": "",
    "role": "",
    "id_area": ""
}
```
## Delete non-manager user
### api/users/[username]/
* method DELETE
* header Authorization Bearer jwt_token
## Update user information
### api/users/[username]/
* method PATCH
* header Authorization Bearer jwt_token
* body is fields that needed to update
