# API Documentation

## Overview

This directory contains API documentation for all services in the project. Each service should maintain its own API documentation following the structure below.

## Documentation Structure

```
api/
├── README.md (this file)
├── payment-service/
│   ├── endpoints.md
│   ├── schemas.md
│   └── examples.md
├── order-service/
│   ├── endpoints.md
│   ├── schemas.md
│   └── examples.md
└── analytics-service/
    ├── endpoints.md
    ├── schemas.md
    └── examples.md
```

## API Documentation Template

### Service: [Service Name]

#### Base URL
```
https://api.example.com/v1/[service]
```

#### Authentication
```
Authorization: Bearer <token>
```

#### Endpoints

##### GET /resource
Description: Retrieve resource details

Request:
```json
{
  "param": "value"
}
```

Response:
```json
{
  "id": "123",
  "data": "value"
}
```

##### POST /resource
Description: Create new resource

Request:
```json
{
  "name": "example",
  "type": "sample"
}
```

Response:
```json
{
  "id": "456",
  "status": "created"
}
```

## Common Response Codes

- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": {
      "resource_id": "123"
    }
  }
}
```

## API Versioning

All APIs follow semantic versioning:
- `/v1/` - Stable version
- `/v2/` - Next major version (breaking changes)
- `/beta/` - Experimental features

## Rate Limiting

Default rate limits:
- 1000 requests per hour per API key
- 100 requests per minute burst

Headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

## API Testing

Use the provided Postman collections or curl examples:

```bash
# Example API call
curl -X GET \
  https://api.example.com/v1/resource \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json'
```

## API Development Guidelines

1. **RESTful Design**: Follow REST principles
2. **Consistent Naming**: Use kebab-case for URLs, camelCase for JSON
3. **Versioning**: Always version your APIs
4. **Documentation**: Keep docs in sync with implementation
5. **Testing**: Provide examples and test cases
6. **Security**: Use HTTPS, authenticate all endpoints
7. **Error Handling**: Return meaningful error messages

## OpenAPI/Swagger

Generate OpenAPI specifications for each service:

```yaml
openapi: 3.0.0
info:
  title: Service API
  version: 1.0.0
paths:
  /resource:
    get:
      summary: Get resource
      responses:
        '200':
          description: Success
```

## Contact

For API support or questions:
- Email: api-support@example.com
- Slack: #api-help
- Documentation: https://docs.example.com