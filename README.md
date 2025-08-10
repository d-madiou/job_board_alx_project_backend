# Job Board API Backend Documentation

This project is a RESTful API built with Django and Django REST Framework to power a modern job board application. It provides a secure and scalable backend for managing job listings, company profiles, and user authentication.

## ✨ Features

- **Job Management**: Create, read, update, and delete job postings with rich details.
- **Company Profiles**: Manage company information, including logos and descriptions.
- **User Authentication**: Secure user registration, login, and token-based authentication using JWT.
- **Role-Based Access**: Different user roles (e.g., employers) have specific permissions.
- **Search & Filtering**: Easily search and filter jobs by keywords, categories, and locations.
- **Image Uploads**: Handle file uploads for company logos via a dedicated endpoint.

## 🛠️ Technology Stack

- **Backend Framework**: Django
- **API Framework**: Django REST Framework (DRF)
- **Database**: PostgreSQL (or SQLite for development) visit this folder(databaseInfo/) to see how I handle the indexing and optimizing the performance
- **Authentication**: JWT (JSON Web Tokens)
- **Package Manager**: Pip

## 🚀 Setup and Installation

Follow these steps to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip
- A code editor (e.g., VS Code)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

Replace `your-username/your-repo-name.git` with the actual repository URL.

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required packages from the requirements.txt file.

```bash
pip install -r requirements.txt
```

### 4. Database Configuration and Migrations

If you are using PostgreSQL, update the database settings in your `settings.py`. For a quick start, the default SQLite database will work.

```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

Create a superuser to access the Django Admin interface.

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

The API will now be accessible at `http://127.0.0.1:8000/`.

## 📄 API Endpoints

The API is built on a RESTful architecture. All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/token/login/` | Log in and get an authentication token. |
| POST | `/api/auth/token/refresh/` | Refresh a JWT token. |
| POST | `/api/users/` | Register a new user. |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | Retrieve a list of all jobs. Supports search and filtering. |
| POST | `/api/jobs/` | Create a new job posting (requires authentication). |
| GET | `/api/jobs/{slug}/` | Retrieve a single job by its slug. |
| PATCH | `/api/jobs/{slug}/edit/` | Update a job (requires authentication and ownership). |
| DELETE | `/api/jobs/{slug}/edit/` | Delete a job (requires authentication and ownership). |

### Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/companies/` | Retrieve a list of all companies. |
| POST | `/api/companies/` | Create a new company profile (requires authentication). |
| GET | `/api/companies/{slug}/` | Retrieve a single company by its slug. |
| PATCH | `/api/companies/{slug}/edit/` | Update a company (requires authentication and ownership). |
| DELETE | `/api/companies/{slug}/edit/` | Delete a company (requires authentication and ownership). |

## 🔐 Authentication

This API uses JSON Web Tokens (JWT) for authentication.

1. **Obtain a Token**: Send a POST request to `/api/auth/token/login/` with your email and password.
2. **Use the Token**: Include the token in the Authorization header of subsequent requests that require authentication.

```
Authorization: Bearer <your_jwt_token>
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions or find a bug, please create an issue or submit a pull request.

## Developer
Thierno Madiou Diallo for alx prodev