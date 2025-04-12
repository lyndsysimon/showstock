# API Documentation

## Authentication

All API endpoints require authentication using JWT tokens.

### Login

```http
POST /auth/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

Response:
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

## Inventory Endpoints

### Get All Items

```http
GET /inventory
Authorization: Bearer <token>
```

### Get Item by ID

```http
GET /inventory/{item_id}
Authorization: Bearer <token>
```

### Create Item

```http
POST /inventory
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "quantity": "integer"
}
```

### Update Item

```http
PUT /inventory/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "quantity": "integer"
}
```

### Delete Item

```http
DELETE /inventory/{item_id}
Authorization: Bearer <token>
``` 