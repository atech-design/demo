# Smart Laundry Backend

Django REST API backend for Smart Laundry application with JWT authentication, admin management, and order processing.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Setup

1. **Install Dependencies**
```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers python-dotenv pillow
```

2. **Run Migrations**
```bash
cd laundry-backend
python manage.py makemigrations
python manage.py migrate
```

3. **Create Superuser**
```bash
python manage.py createsuperuser
# Username: admin
# Password: Admin@123
```

4. **Start Server**
```bash
python manage.py runserver 127.0.0.1:5000
```

Server will be available at: `http://127.0.0.1:5000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/send-otp` - Send OTP to email
- `POST /api/auth/verify-otp` - Verify OTP and get JWT token
- `GET /api/auth/google` - Google OAuth (placeholder)

### Services (Public)
- `GET /api/services/` - List all active services
- `GET /api/services/{id}` - Get service details
- `GET /api/categories` - Get service categories

### Services (Admin Only)
- `POST /api/services/create` - Create new service
- `PUT/PATCH /api/services/{id}/update` - Update service
- `DELETE /api/services/{id}/delete` - Delete service

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/decrease` - Decrease item quantity
- `DELETE /api/cart/{id}` - Remove item from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `GET /api/orders/my` - Get user's orders

### Contact
- `POST /api/contact/submit` - Submit contact form

### Admin Panel
- `http://127.0.0.1:5000/admin/` - Django Admin Interface

## 🔐 Authentication

### JWT Token Flow
1. Send OTP: `POST /api/auth/send-otp` with `{"email": "user@example.com"}`
2. Verify OTP: `POST /api/auth/verify-otp` with `{"email": "user@example.com", "otp": "123456"}`
3. Use token in headers: `Authorization: Bearer <token>`

### User Roles
- **Admin** (`is_staff: true`): Full access to admin panel and CRUD operations
- **User** (`is_staff: false`): Standard user access

## 📊 Database Models

### Service
```python
{
  "id": 1,
  "name": "Laundry Service",
  "description": "Professional laundry care",
  "category": "Laundry",
  "price": "299.00",
  "image_url": "https://example.com/image.jpg",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Order
```python
{
  "id": 1,
  "user": 1,
  "status": "pending",
  "total": "299.00",
  "created_at": "2025-01-01T00:00:00Z",
  "items": [
    {
      "id": 1,
      "service": {...},
      "qty": 2,
      "price": "299.00"
    }
  ]
}
```

## 🛠️ Configuration

### Environment Variables
Create `.env` file in `laundry-backend/`:
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:5173
```

### CORS Settings
- `CORS_ALLOW_ALL_ORIGINS=True` (development)
- `CORS_ALLOW_CREDENTIALS=True`

## 🔧 Admin Features

### Service Management
- Create, read, update, delete services
- Set categories, prices, descriptions
- Toggle active/inactive status
- Image upload support

### Order Management
- View all orders with inline order items
- Filter by status, date, user
- Order status tracking

### User Management
- View user accounts
- Manage user permissions
- Staff/admin role assignment

## 📱 Frontend Integration

### Base URL
```javascript
const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: { "Content-Type": "application/json" }
});
```

### Authentication Headers
```javascript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('smartLaundryUser');
  if (token) {
    config.headers.Authorization = `Bearer ${JSON.parse(token).token}`;
  }
  return config;
});
```

## 🚀 Production Deployment

### Security Checklist
- [ ] Change `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` for your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper CORS origins
- [ ] Use environment variables for sensitive data

### Recommended Stack
- **Database**: PostgreSQL
- **Web Server**: Nginx + Gunicorn
- **Static Files**: AWS S3 or CloudFront
- **Media Files**: AWS S3 or Cloudinary

## 📝 API Examples

### Create Service (Admin)
```bash
curl -X POST http://127.0.0.1:5000/api/services/create \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Laundry",
    "description": "High-quality laundry service",
    "category": "Laundry",
    "price": "399.00",
    "image_url": "https://example.com/premium.jpg"
  }'
```

### Add to Cart
```bash
curl -X POST http://127.0.0.1:5000/api/cart/add \
  -H "Authorization: Bearer <user-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "qty": 2,
    "price": 299.00
  }'
```

### Submit Contact Form
```bash
curl -X POST http://127.0.0.1:5000/api/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "subject": "Inquiry",
    "message": "Hello, I have a question about your services."
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure `CORS_ALLOW_ALL_ORIGINS=True` in settings
   - Check frontend URL matches `FRONTEND_URL`

2. **Authentication Issues**
   - Verify JWT token format: `Bearer <token>`
   - Check token expiration (8 hours default)

3. **Admin Access**
   - Ensure user has `is_staff=True`
   - Use correct admin credentials

4. **Database Issues**
   - Run `python manage.py migrate` after model changes
   - Check database file permissions

### Logs
Check server logs for detailed error messages:
```bash
python manage.py runserver 127.0.0.1:5000 --verbosity=2
```

## 📞 Support

For issues or questions:
1. Check this README
2. Review Django logs
3. Verify API endpoint responses
4. Test with Postman/curl

---

**Happy Coding! 🎉**
