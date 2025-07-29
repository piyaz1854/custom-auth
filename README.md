# custom-auth

A simple learning project: custom authentication and authorization system built with Django REST Framework, JWT, and PostgreSQL.

No built-in Django auth — everything is handcrafted.
JWT-based, role-driven, with access control stored in the database.

POST /api/login/ -> get token -> use it in Bearer header

# How to install:
git clone <this_repo_http>

---

## Features

- Custom User model (email login, soft delete, role field)
- Manual JWT authentication (no sessions, no cookies)
- Custom middleware for token validation
- Role-based access control system
- Permissions per business element (create, read, update, delete — own/all)
- Admins can configure roles and rules via API

---

## 🛠 Tech Stack

- Python, Django, DRF
- PostgreSQL
- bcrypt for password hashing
- PyJWT for token generation
- Custom middleware, no magic

---
# Database:
Roles: Overlord, Commander, Scout, Novice
Overlord:
AccessRule.objects.create(
    role=overlord,
    element=element,
    read_my_permission=True,
    read_all_permission=True,
    create_my_permission=True,
    create_all_permission=True,
    update_my_permission=True,
    update_all_permission=True,
    delete_my_permission=True,
    delete_all_permission=True
)

Commander:
AccessRule.objects.create(
    role=commander
    element=element,
    read_my_permission=True,
    read_all_permission=True,
    create_my_permission=True,
    update_my_permission=True,
    delete_my_permission=True
)

Scout:
AccessRule.objects.create(
    role=role,
    element=element,
    read_all_permission=True
)

Novice:
AccessRule.objects.create(
    role=role,
    element=element,
    read_my_permission=True
)


# Business Elements: Documents and Projects
Documents:
DOCUMENTS = [
    {"id": 1,
    "owner_pk": 9,
    "title": "secret document",
    "content":"Джо не входил в сделку."},
    {"id": 2,
    "owner_pk": 9,
    "title": "some document",
    "content":"Special for Effective Mobile."
    }
]


PROJECTS = [
    {"id": 1, "name": "project 1", "owner": 1},
    {"id": 2, "name": "secure project", "owner": 2}
]

How it works?
I think ER diagram explains better than any words:
<img src="er.jpg" alt="er diagram" width="400"/>




# Quick test with curl

# Register

curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Tony",
    "last_name": "Montana",
    "middle_name": "Carlos",
    "email": "tony@scarface.com",
    "password": "sayhello123",
    "password2": "sayhello123"
  }'

# Login

curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tony@scarface.com",
    "password": "sayhello123"
  }'

# Authorization
(Note: Some endpoints may require additional middleware/auth setup due to DRF request context.)

curl -X GET http://localhost:8000/api/profile/ -H "Authorization: Bearer your_token"

# Business elements
(Note: Some endpoints may require additional middleware/auth setup due to DRF request context.)

curl -X GET http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMn0.8w4QGGgrJdVhIsNFYLp1fWcocyFhvMXd6tk-RP4qofA"

# Delete account
(Note: Some endpoints may require additional middleware/auth setup due to DRF request context.)

curl -X DELETE http://localhost:8000/api/delete-account/ \  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMn0.8w4QGGgrJdVhIsNFYLp1fWcocyFhvMXd6tk-RP4qofA"


## Conclusion

Before introducing role-based access control, business element access worked smoothly. After adding roles, some issues emerged — mostly around middleware and DRF request context.

Despite that, the task was a great learning experience, and I enjoyed working on it. Thank you, Effective Mobile, for the opportunity!



