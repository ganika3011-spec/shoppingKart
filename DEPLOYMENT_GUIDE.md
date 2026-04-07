# Production Deployment Guide

## 🚀 Deployment Methods

Choose one of the following deployment methods based on your infrastructure:

### 1. Traditional VPS Deployment (Ubuntu/Debian)
### 2. Docker Deployment (Recommended)
### 3. Cloud Platform Deployment (AWS, Azure, Heroku)

---

## Method 1: Traditional VPS Deployment

### Prerequisites
- Ubuntu 20.04 LTS or Debian 11
- SSH access to server
- Domain name with DNS configured

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib postgresql-client \
    redis-server nginx git curl wget \
    libpq-dev build-essential

# Install Node.js (optional, for frontend build)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Step 2: Create Application User

```bash
# Create user
sudo useradd -m -s /bin/bash shopping-kart

# Create application directory
sudo mkdir -p /home/shopping-kart/shoppingKart
sudo chown -R shopping-kart:shopping-kart /home/shopping-kart
```

### Step 3: Clone Repository

```bash
sudo su - shopping-kart
cd /home/shopping-kart

# Clone your repository
git clone <your-repo-url> .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with production values
nano .env
```

Edit `.env` with your production settings:
```env
DEBUG=False
SECRET_KEY=your-very-secure-random-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://shopping_kart:password@localhost:5432/shopping_cart
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 5: Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres psql

# In psql:
CREATE DATABASE shopping_cart;
CREATE USER shopping_kart WITH PASSWORD 'secure_password';
ALTER ROLE shopping_kart SET client_encoding TO 'utf8';
ALTER ROLE shopping_kart SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE shopping_cart TO shopping_kart;
\q
```

### Step 6: Django Migrations

```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Setup Gunicorn Service

```bash
# Create systemd service
sudo nano /etc/systemd/system/gunicorn.service
```

Paste the content from `gunicorn_systemd.service`

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

### Step 8: Configure Nginx

```bash
# Copy nginx config
sudo cp nginx_config.conf /etc/nginx/sites-available/shopping-kart
sudo ln -s /etc/nginx/sites-available/shopping-kart /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### Step 9: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal check
sudo systemctl status certbot.timer
```

### Step 10: Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### Step 11: Monitoring & Logs

```bash
# View gunicorn logs
journalctl -u gunicorn -f

# View nginx logs
tail -f /var/log/nginx/shopping_kart_access.log
tail -f /var/log/nginx/shopping_kart_error.log

# View Django logs
tail -f /home/shopping-kart/shoppingKart/logs/django.log
```

---

## Method 2: Docker Deployment

### Prerequisites
- Docker & Docker Compose installed
- Domain with DNS configured
- 2GB+ RAM, 10GB+ storage

### Step 1: Clone & Setup

```bash
# Clone repository
git clone <your-repo-url> shopping-kart
cd shopping-kart

# Create environment file
cp .env.example .env
nano .env
```

### Step 2: Build & Run

```bash
# Build images
docker-compose build

# Run migrations
docker-compose run web python manage.py migrate

# Create superuser
docker-compose run web python manage.py createsuperuser

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### Step 3: Health Checks

```bash
# Check if services are healthy
docker-compose exec web python manage.py check

# Test database connection
docker-compose exec web python manage.py dbshell

# Test static files
docker-compose exec web ls -la staticfiles/
```

### Step 4: Backup Database

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U shopping_kart shopping_cart > backup.sql

# Restore from backup
docker-compose exec -T db psql -U shopping_kart shopping_cart < backup.sql
```

### Step 5: Updates & Deployments

```bash
# Pull latest changes
git pull origin main

# Rebuild images
docker-compose build --no-cache

# Run migrations
docker-compose run web python manage.py migrate

# Restart services
docker-compose up -d
```

---

## Method 3: Cloud Platform Deployment

### AWS EC2 Deployment

```bash
# Launch EC2 instance
# - AMI: Ubuntu 22.04 LTS
# - Instance type: t3.medium or larger
# - Storage: 20GB

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Follow Traditional VPS steps 1-10
```

### PaaS Options (Easier)

#### Heroku Deployment

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create shopping-kart

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

#### Railway.app Deployment

1. Connect GitHub repository
2. Add PostgreSQL plugin
3. Set environment variables
4. Deploy automatically

---

## Post-Deployment Checklist

- [ ] Test homepage loads
- [ ] Test product listing
- [ ] Test user registration/login
- [ ] Test product search
- [ ] Test shopping cart
- [ ] Test checkout process
- [ ] Verify email sending
- [ ] Check SSL certificate
- [ ] Monitor error logs
- [ ] Setup automated backups
- [ ] Configure monitoring (Sentry)
- [ ] Setup uptime monitoring

---

## Maintenance

### Regular Updates

```bash
# Weekly: Check for security updates
pip list --outdated
pip install --upgrade pip

# Monthly: Django security releases
pip install --upgrade Django

# Run migrations
python manage.py migrate

# Restart services
systemctl restart gunicorn
systemctl restart nginx
```

### Database Maintenance

```bash
# Weekly backup
pg_dump shopping_cart > /backups/backup_$(date +%Y%m%d).sql

# Clean old sessions
python manage.py clearsessions

# Optimize database
python manage.py dbshell
# In psql: VACUUM ANALYZE;
```

### Monitoring

```bash
# CPU & Memory
free -h
df -h
top

# Gunicorn
journalctl -u gunicorn -n 100

# Nginx
tail -100 /var/log/nginx/shopping_kart_access.log
```

---

## Troubleshooting

### Issue: 502 Bad Gateway
- Check if Gunicorn is running: `systemctl status gunicorn`
- Check logs: `journalctl -u gunicorn`
- Check socket: `ls -la /run/gunicorn.sock`

### Issue: Static Files Not Loading
- Run: `python manage.py collectstatic`
- Check Nginx config points to correct directory
- Verify file permissions

### Issue: Database Connection Error
- Verify DATABASE_URL in .env
- Check if PostgreSQL is running
- Verify credentials

### Issue: Email Not Sending
- Verify EMAIL_* settings
- Check firewall allows SMTP port 587
- Test with: `python manage.py shell` then `from django.core.mail import send_mail`

---

## Support & Resources

- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
- Let's Encrypt: https://letsencrypt.org/docs/

---

**Last Updated**: April 2026
**Maintained by**: Your Team
