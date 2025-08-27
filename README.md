# Healthcare Backend API

A robust Django-based REST API for managing healthcare data, including patients, doctors, and their relationships.

## 🚀 Features

- **User Authentication**
  - JWT-based authentication
  - User registration and login
  - Secure password handling

- **Patient Management**
  - Create, read, update, and delete patient records
  - Patient-specific access control
  - Medical history tracking

- **Doctor Management**
  - Manage doctor profiles
  - Track specializations
  - Contact information management

- **Patient-Doctor Relationships**
  - Assign doctors to patients
  - Track patient-doctor relationships
  - Filter mappings by patient

## 🛠️ Technology Stack

- **Backend Framework:** Django 5.0.1
- **API Framework:** Django REST Framework 3.14.0
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Environment Management:** python-dotenv

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- pip (Python package manager)

## 🔧 Installation & Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd whatbytes-django
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a .env file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DB_NAME=healthcare_db
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
  ```json
  {
      "username": "user1",
      "email": "user1@example.com",
      "password": "secure_password"
  }
  ```
- `POST /api/auth/login/` - Login and get JWT token
  ```json
  {
      "username": "user1",
      "password": "secure_password"
  }
  ```
- `POST /api/auth/refresh/` - Refresh JWT token

### Patients
- `GET /api/patients/` - List all patients (authenticated user's patients)
- `POST /api/patients/` - Create a new patient
  ```json
  {
      "name": "John Doe",
      "age": 30,
      "gender": "Male",
      "contact": "1234567890",
      "address": "123 Main St",
      "medical_history": "No major issues"
  }
  ```
- `GET /api/patients/{id}/` - Get patient details
- `PUT /api/patients/{id}/` - Update patient
- `DELETE /api/patients/{id}/` - Delete patient

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Add a new doctor
  ```json
  {
      "name": "Dr. Smith",
      "specialization": "Cardiologist",
      "contact": "9876543210",
      "email": "dr.smith@example.com"
  }
  ```
- `GET /api/doctors/{id}/` - Get doctor details
- `PUT /api/doctors/{id}/` - Update doctor
- `DELETE /api/doctors/{id}/` - Delete doctor

### Patient-Doctor Mappings
- `GET /api/mappings/` - List all mappings
- `GET /api/mappings/?patient_id={id}` - Get mappings for specific patient
- `POST /api/mappings/` - Create new mapping
  ```json
  {
      "patient": 1,
      "doctor": 1
  }
  ```
- `DELETE /api/mappings/{id}/` - Delete mapping

## 🔒 Authentication

All endpoints (except registration and login) require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

## 🧪 Testing

Run tests using:
```bash
python manage.py test
```

## 📝 Code Style

This project follows Python's PEP 8 style guide and Django's coding standards. Key features include:
- Type hints for better code clarity
- Comprehensive docstrings
- Clear class and method organization
- Proper error handling
- Security best practices

## 🛡️ Security Features

- JWT-based authentication
- Password hashing
- User-specific data access
- Input validation
- CSRF protection
- Secure password storage
- Request validation


## 🙏 Acknowledgments

- Django documentation
- Django REST Framework documentation
- PostgreSQL documentation
