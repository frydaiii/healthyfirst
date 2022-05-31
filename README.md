# API document
## User
### Register
* api/users/
* POST
* body x-www-form-urlencoded
  * username
  * password
  * password2
  * first_name
  * last_name
  * is_manager: 0 or 1
  * id_area
  * email
### Login
* api/token/
* POST
* body x-www-form-urlencoded
  * username
  * password
### Get new access token
* api/token/refresh/
* POST
* body x-www-form-urlencoded
  * refresh
### Get user information
* api/users/[username]
* GET
* header Authorization Bearer jwt_token
### Delete non-manager user
* api/users/[username]/
* DELETE
* header Authorization Bearer jwt_token
### Update user information
* api/users/[username]/
* PATCH
* header Authorization Bearer jwt_token
* body is fields that needed to update
## Premises
> header Authorization Bearer jwt_token
### Get list of premises
* api/premises/
* GET
### Get information of a premises
* api/premises/[premise_id]
* GET
### Create new premise
* api/premises/
* POST
* body
  * name
  * address
  * phone_number
  * id_area
  * id_business_type
  * id_certificate
### Update premises information
* api/premises/
* PATCH
* body: fields need to update
### Delete premise
* api/premises/[premise_id]
* DELETE
## Certificate
> header Authorization Bearer jwt_token
### Get list of certificates
* api/certificate/
* GET
### Get information of a certificate
* api/certificate/[certificate_id]
* GET
### Create new certificate
* api/certificate/
* POST
* body
  * id_business_type
  * issued_date
  * expired_date
  * series
### Update certificate information
* api/certificate/
* PATCH
* body: fields need to update
### Delete certificate
* api/certificate/[certificate_id]
* DELETE
## Business type
> header Authorization Bearer jwt_token
### Get list of budinesstypes
* api/budinesstype/
* GET
### Get information of a budinesstype
* api/budinesstype/[budinesstype_id]
* GET
### Create new budinesstype
* api/budinesstype/
* POST
* body
  * name
  * description
### Update budinesstype information
* api/budinesstype/
* PATCH
* body: fields need to update
### Delete budinesstype
* api/budinesstype/[certificate_id]
* DELETE
## Inspection plan
> header Authorization Bearer jwt_token
### Get list of inspectionplans
* api/inspectionplan/
* GET
### Get information of a inspectionplan
* api/inspectionplan/[inspectionplan_id]
* GET
### Create new inspectionplan
* api/inspectionplan/
* POST
* body
  * inspection_date
  * sample_needed
  * violate
  * id_premise
  * id_sample
### Update inspectionplan information
* api/inspectionplan/
* PATCH
* body: fields need to update
### Delete inspectionplan
* api/inspectionplan/[certificate_id]
* DELETE
## Sample
> header Authorization Bearer jwt_token
### Get list of samples
* api/sample/
* GET
### Get information of a sample
* api/sample/[sample_id]
* GET
### Create new sample
* api/sample/
* POST
* body
  * id_premise
  * accreditation_premise
  * accreditation_status
  * result_date
  * result_valid
### Update sample information
* api/sample/
* PATCH
* body: fields need to update
### Delete sample
* api/sample/[certificate_id]
* DELETE
## Area
> header Authorization Bearer jwt_token
### Get list of areas
* api/area/
* GET
### Get information of a area
* api/area/[area_id]
* GET
### Create new area
* api/area/
* POST
* body
  * name
  * type
### Update area information
* api/area/
* PATCH
* body: fields need to update
### Delete area
* api/area/[certificate_id]
* DELETE
