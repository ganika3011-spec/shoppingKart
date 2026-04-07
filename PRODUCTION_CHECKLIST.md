# Production Deployment Checklist

## 🔒 Security

- [ ] **Environment Variables**: All sensitive data in `.env` file (SECRET_KEY, database URL, email credentials)
- [ ] **DEBUG = False**: Ensure DEBUG is set to False in production
- [ ] **ALLOWED_HOSTS**: Configure proper domain names
- [ ] **SECRET_KEY**: Use a strong, random SECRET_KEY (never commit the development one)
- [ ] **HTTPS**: Enable SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE
- [ ] **Database**: Switch from SQLite to PostgreSQL
- [ ] **Email**: Use environment variables for email configuration
- [ ] **CORS**: Configure CORS_ALLOWED_ORIGINS if using separate frontend
- [ ] **HSTS**: Enable HTTP Strict Transport Security (SECURE_HSTS_SECONDS)
- [ ] **Content Security Policy**: Review and update security headers
- [ ] **Disable Admin**: Rename or restrict access to `/admin/` URL
- [ ] **Validate Input**: All forms validated server-side
- [ ] **SQL Injection**: Using Django ORM (already protected)
- [ ] **CSRF Protection**: CSRF tokens on all forms

## 🗄️ Database

- [ ] **Migration**: Run `python manage.py migrate` on production
- [ ] **PostgreSQL**: Use PostgreSQL instead of SQLite
- [ ] **Backups**: Set up automated database backups
- [ ] **Indexes**: Database indexes created for frequently queried fields ✅ (Done)
- [ ] **Connection Pooling**: Configure database connection pooling
- [ ] **Read Replicas**: Consider read replicas for scaling

## 📝 Logging

- [ ] **Logging Configured**: Production logging setup in settings.py ✅ (Done)
- [ ] **Log Rotation**: RotatingFileHandler with max file size
- [ ] **Log Files**: Logs stored outside the application directory
- [ ] **Error Tracking**: Sentry integration for error monitoring
- [ ] **Access Logs**: Configure access logging for gunicorn

## 🚀 Performance

- [ ] **Caching**: Redis caching configured for database queries
- [ ] **Static Files**: Collect static files with WhiteNoise or CDN
- [ ] **Select Related**: Query optimization with select_related/prefetch_related ✅ (Done)
- [ ] **Pagination**: Implement pagination for large datasets ✅ (Done)
- [ ] **Compress**: Enable GZIP compression
- [ ] **Database Indexes**: Add indexes on frequently searched fields ✅ (Done)
- [ ] **Minify CSS/JS**: Minify static assets
- [ ] **Image Optimization**: Optimize product images
- [ ] **Lazy Loading**: Implement lazy loading for images
- [ ] **Async Tasks**: Use Celery for long-running tasks

## 🔧 Application

- [ ] **Gunicorn**: Production WSGI server configured
- [ ] **Workers**: Configure appropriate number of workers (2-4 per CPU core)
- [ ] **Timeout**: Set request timeout (30 seconds default)
- [ ] **Health Check**: Implement health check endpoint
- [ ] **Graceful Shutdown**: Handle SIGTERM for graceful shutdown
- [ ] **Admin Users**: Create superuser for production admin
- [ ] **Fixtures**: Load initial data if needed

## 📦 Dependencies

- [ ] **requirements.txt**: Updated with all dependencies ✅ (Done)
- [ ] **Version Pinning**: Pin specific versions for reproducibility
- [ ] **Security Updates**: Regularly check for package updates
- [ ] **Unused Packages**: Remove unused dependencies

## 📧 Email

- [ ] **SMTP Configuration**: Configure proper email backend
- [ ] **From Email**: Set DEFAULT_FROM_EMAIL
- [ ] **Email Testing**: Test email sending
- [ ] **SPF/DKIM**: Configure SPF and DKIM records

## 👤 User Management

- [ ] **Password Hashing**: Django handles password hashing properly
- [ ] **Token Expiration**: Configure session timeout
- [ ] **Reset Password**: Email-based password reset working
- [ ] **2FA**: Consider implementing two-factor authentication

## 📊 Monitoring

- [ ] **Health Checks**: Configure basic health check endpoint
- [ ] **Uptime Monitoring**: External uptime monitoring service
- [ ] **Resource Monitoring**: CPU, memory, disk space monitoring
- [ ] **Database Monitoring**: Monitor slow queries
- [ ] **Error Tracking**: Sentry or similar error tracking service

## 🧪 Testing

- [ ] **Unit Tests**: Write tests for models and views
- [ ] **Integration Tests**: Test database interactions
- [ ] **Load Testing**: Perform load testing before production
- [ ] **Security Testing**: Run security vulnerability scans

## 📱 Frontend

- [ ] **API Security**: Validate all API requests
- [ ] **Rate Limiting**: Implement rate limiting for APIs
- [ ] **CORS**: Properly configured CORS headers
- [ ] **CSP Headers**: Content Security Policy configured

## 🔄 DevOps

- [ ] **Docker**: Dockerize the application
- [ ] **Container Registry**: Push images to registry
- [ ] **CI/CD**: Set up GitHub Actions or GitLab CI
- [ ] **Kubernetes**: Deploy with Kubernetes if using containers
- [ ] **Load Balancer**: Configure load balancer for scaling

## 📋 Deployment Steps

### 1. Pre-Deployment
```bash
# Clone repository
git clone <repo-url>
cd shoppingKart

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with production values
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Launch with Gunicorn
```bash
# Start gunicorn server
gunicorn -w 4 -b 0.0.0.0:8000 Kart.wsgi:application --timeout 30

# Or with systemd service (recommended)
# See gunicorn_systemd.service for systemd configuration
```

### 4. Nginx Configuration
Configure Nginx as reverse proxy (see nginx_config.conf)

### 5. SSL Certificate
- Use Let's Encrypt with Certbot for HTTPS
- Auto-renewal configured

## 🚨 Common Issues

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: Database connection errors
**Solution**: Check DATABASE_URL in .env file

### Issue: Email not sending
**Solution**: Verify EMAIL_* settings and SMTP credentials

### Issue: ALLOWED_HOSTS error
**Solution**: Add domain to ALLOWED_HOSTS in settings.py or .env

## 📞 Support & Resources

- Django Documentation: https://docs.djangoproject.com/
- Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/

## ✅ Post-Deployment

- [ ] Test all critical user flows
- [ ] Monitor error logs
- [ ] Verify email sending
- [ ] Load testing with realistic traffic
- [ ] Database backup verification
- [ ] SSL certificate validity
- [ ] Health check endpoint responding

---

**Last Updated**: April 2026
**Django Version**: 6.0.1
**Python Version**: 3.9+
