# Hotel Booking Platform Backend API

A comprehensive Django REST Framework backend API for a hotel booking platform with user authentication, hotel management, room booking, and review functionality.

## Features

✅ **User Authentication & Authorization**
- JWT token-based authentication
- User registration and login
- Secure password handling
- User profile management

✅ **Hotel Management**
- CRUD operations for hotels
- Search and filter hotels by location
- Hotel ratings and amenities

✅ **Room Management**
- CRUD operations for rooms
- Room types (single, double, suite, deluxe, family)
- Price management and availability tracking
- Advanced search with date-based availability

✅ **Booking System**
- Create, view, update, and cancel bookings
- Automatic price calculation
- Booking status management (pending, confirmed, cancelled, completed)
- Overlap prevention for room bookings
- Special requests handling

✅ **Review System**
- User reviews for hotels
- Rating system (1-5 stars)
- Review management

✅ **Advanced Features**
- Comprehensive input validation
- Error handling and proper HTTP status codes
- Pagination for large datasets
- Search and filtering capabilities
- CORS support for frontend integration
- Admin panel for management

## Technology Stack

- **Backend Framework:** Django 5.2.2
- **API Framework:** Django REST Framework 3.16.0
- **Authentication:** JWT (Simple JWT)
- **Database:** MySQL (configurable)
- **Additional Libraries:**
  - django-cors-headers (CORS support)

## Project Structure

```
PRODIGY_BD_03/
├── RestAPI/                 # Django project settings
│   ├── settings.py          # Main settings file
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── app/                     # Main application
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── api/                     # API URL routing
│   └── urls.py              # API URL patterns
├── sampledata.py            # Sample data creation script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── manage.py                # Django management script
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- MySQL (or SQLite for development)
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd PRODIGY_BD_05
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/Scripts/activate  # On Git Bash
venv/bin/activate  # On Windows Terminal/cmd
source venv/bin/activate  # On Linux/Mac 
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
USER='mysql-username'
MYSQL_PASSWORD='your-mysql-passwor'
ENVIRONMENT='development'
SECRET_KEY='your-secrete-key'
```

### 5. Database Setup

#### For SQLite (Development):
Update `settings.py` to use SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Load Sample Data (Optional)
```bash
python sampledata.py
```

### 9. Run Development Server
```bash
python manage.py runserver http://127.0.0.1:8000
```

The API will be available at: `http://localhost:8000/api/v1/`

## API Endpoints

### Authentication
- `POST /api/v1/public/user/register/` - User registration
- `POST /api/v1/public/user/login/` - User login
- `GET /api/v1/public/user/profile/` - User profile (authenticated)

### Hotels
- `GET /api/v1/hotels/` - List hotels
- `POST /api/v1/hotels/` - Create hotel (admin)
- `GET /api/v1/hotels/{id}/` - Get hotel details
- `PUT/PATCH /api/v1/hotels/{id}/` - Update hotel (admin)
- `DELETE /api/v1/hotels/{id}/` - Delete hotel (admin)

### Rooms
- `GET /api/v1/rooms/` - List rooms
- `GET /api/v1/rooms/search_available/` - Search available rooms
- `POST /api/v1/rooms/` - Create room (admin)
- `GET /api/v1/rooms/{id}/` - Get room details
- `PUT/PATCH /api/v1/rooms/{id}/` - Update room (admin)
- `DELETE /api/v1/rooms/{id}/` - Delete room (admin)

### Bookings
- `GET /api/v1/bookings/` - List user bookings (authenticated)
- `POST /api/v1/bookings/` - Create booking (authenticated)
- `GET /api/v1/bookings/{id}/` - Get booking details (authenticated)
- `PUT/PATCH /api/v1/bookings/{id}/` - Update booking (authenticated)
- `POST /api/v1/bookings/{id}/cancel/` - Cancel booking (authenticated)

### Reviews
- `GET /api/v1/reviews/` - List reviews
- `POST /api/v1/reviews/` - Create review (authenticated)
- `GET /api/v1/reviews/{id}/` - Get review details
- `PUT/PATCH /api/v1/reviews/{id}/` - Update review (authenticated)
- `DELETE /api/v1/reviews/{id}/` - Delete review (authenticated)

## Sample API Usage

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/public/user/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "password123",
    "password2": "password123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/public/user/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### 3. Search Available Rooms
```bash
curl "http://localhost:8000/api/v1/rooms/search_available/?check_in=2025-07-01&check_out=2025-07-05&guests=2&city=New%20York"
```

### 4. Create a Booking
```bash
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "room": 1,
    "check_in_date": "2025-07-01",
    "check_out_date": "2025-07-05",
    "guests": 2,
    "special_requests": "Late check-in requested"
  }'
```

## Admin Panel

Access the Django admin panel at: `http://localhost:8000/admin/`

Default admin credentials (if using sample data):
- Email: admin@example.com
- Password: admin123

## Testing

### Manual Testing
1. Start the development server
2. Use the provided sample data
3. Test endpoints using curl, Postman, or any HTTP client
4. Check the API documentation for detailed examples

### Sample Data
The project includes a `sampledata.py` script that creates:
- 3 sample hotels
- 12 sample rooms
- 2 sample users
- 2 sample bookings
- 1 sample review

## Deployment

### Production Settings
1. Set `ENVIRONMENT=production` in `.env`
2. Configure a production database
3. Set up a proper web server (nginx + gunicorn)
4. Configure static file serving
5. Set up SSL certificates

### Environment Variables for Production
```env
SECRET_KEY=your_production_secret_key
ENVIRONMENT=production
USER='users-username'
MYSQL_PASSWORD='users-password'
```

## Security Features

- JWT token authentication
- Password hashing
- CORS configuration
- Input validation and sanitization
- SQL injection prevention (Django ORM)
- XSS protection
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the API documentation
2. Review the sample data and usage examples
3. Check Django and DRF documentation
4. Create an issue in the repository

## Changelog

### Version 1.0.0
- Initial release
- Complete hotel booking API
- JWT authentication
- Admin panel
- Comprehensive documentation

