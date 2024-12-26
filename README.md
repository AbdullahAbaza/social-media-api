# Social Media API

A robust social media backend API built with FastAPI, featuring user authentication, post management, and voting system.

## Features

- **User Management**: Registration, authentication, and profile management
- **Post Operations**: Create, read, update, and delete posts
- **Voting System**: Upvote functionality for posts
- **Authentication**: JWT-based authentication system
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Python 3.8+

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd social-media-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Running the Application

### Development
```bash
uvicorn main:app --reload
```
Access the API documentation at: http://localhost:8000/docs

## API Routes

### Posts
- `GET /posts`: Retrieve all posts
- `POST /posts`: Create a new post
- `GET /posts/{id}`: Get a specific post
- `PUT /posts/{id}`: Update a post
- `DELETE /posts/{id}`: Delete a post

### Users
- `POST /users`: Create a new user
- `GET /users/{id}`: Get user information

### Auth
- `POST /login`: User authentication

### Votes
- `POST /vote`: Vote on a post

## Upcoming Features

### Testing
- Comprehensive unit tests
- Integration tests
- API endpoint testing

### Containerization
- Docker implementation
- Production-grade Gunicorn server
- Multi-container deployment
- Nginx load balancer and reverse proxy

### CI/CD Pipeline
- GitHub Actions workflow
- Automated testing
- Continuous deployment
- Infrastructure as Code

## Development Reference
This project is based on the [FastAPI Course](https://github.com/Sanjeev-Thiyagarajan/fastapi-course) by Sanjeev Thiyagarajan, with additional enhancements and features.

## Documentation
For detailed API documentation and usage, refer to:
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- API Documentation (Swagger): http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
