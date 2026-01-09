# Foody Project

A Django-based food ordering web application that allows users to browse food items, add them to a cart, place orders, and manage their profiles. The application supports user authentication, social login, and is containerized for easy deployment.

## Features

- **User Authentication**: Registration, login, and social authentication (via social-auth-app-django)
- **Food Menu**: Browse food items categorized into Starters, Main Course, Desserts, and Beverages
- **Shopping Cart**: Add/remove items from cart with quantity management
- **Order Management**: Place orders, view order history, and track order status (Pending, Cancelled, Delivered)
- **User Profiles**: Manage profile information including profile picture, phone, email, and address
- **Payment Integration**: Secure payments using Razorpay
- **Admin Panel**: Django admin interface for managing food items, orders, and users
- **Responsive Design**: Built with HTML, CSS, and JavaScript for a user-friendly interface
- **Docker Support**: Containerized application for easy deployment

## Tech Stack

- **Backend**: Django 5.1.7
- **Database**: SQLite (default), supports MySQL and PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django Auth + Social Auth App Django
- **Payments**: Razorpay
- **Deployment**: Docker + Gunicorn
- **Other Libraries**:
  - python-decouple for environment variables
  - Pillow for image handling
  - argon2-cffi for password hashing

## Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Git

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd foody_project
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root with the following variables:

   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   # Add other configuration variables as needed (e.g., database credentials, Razorpay keys)
   ```

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

## Usage

1. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`

2. **Access admin panel**:
   Go to `http://127.0.0.1:8000/admin/` and log in with superuser credentials

3. **Key URLs**:
   - Home: `/`
   - Login: `/login/`
   - Register: `/register/`
   - Profile: `/profile/`
   - My Orders: `/my-orders/`
   - Cart: `/cart/` (via drawer)
   - Checkout: `/checkout/`

## Deployment

### Using Docker

1. **Build the Docker image**:

   ```bash
   docker build -t foody-project .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 foody-project
   ```

The application will be available at `http://localhost:8000`

### Manual Deployment

For production deployment, ensure:

- Set `DEBUG=False` in settings
- Configure proper `ALLOWED_HOSTS`
- Use a production-grade database (MySQL/PostgreSQL)
- Set up proper static file serving
- Configure environment variables securely

## Project Structure

```
foody_project/
├── foody_project/          # Django project settings
├── main/                   # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL patterns
│   ├── templates/          # HTML templates
│   ├── static/             # Static files (CSS, JS, images)
│   └── migrations/         # Database migrations
├── media/                  # User-uploaded media files
├── staticfiles/            # Collected static files
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── manage.py               # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
