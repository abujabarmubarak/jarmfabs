# JarmFabs Technologies — Full-Stack Web Application

Official web platform for **JarmFabs Technologies** — an IT and digital solutions company headquartered in Kadayanallur, Tenkasi, Tamil Nadu, India.

### 🌐 Official Social Channels
- **LinkedIn**: [linkedin.com/company/jarmfabstechnologies](https://www.linkedin.com/company/jarmfabstechnologies/)
- **X (Twitter)**: [x.com/jarmfabstech](https://x.com/jarmfabstech)
- **Instagram**: [instagram.com/jarmfabstechnologies](https://www.instagram.com/jarmfabstechnologies/)

---

## 🌟 Key Features

1. **Dedicated Separate Pages for All Sections**:
   - `GET /` — Home page with interactive 3D hero, services highlights, client partners, gallery photos, and active jobs.
   - `GET /explore` — Corporate overview, founding story ("Jarm" + "Fabs" rationale), registered office details, and company values.
   - `GET /services` — Comprehensive breakdown of all 8 core disciplines with specifications and inquiry shortcuts.
   - `GET /industries` — 10 sector-specific solutions (Higher Education, Healthcare, Retail, Manufacturing, Logistics, etc.).
   - `GET /clients` — Real client partner portfolio dynamically loaded from database (including Mohamed Sathak A J College, Al Kabir, etc.).
   - `GET /innovation` — Applied AI, workflow automation, modern cloud stack, and technical architecture.
   - `GET /insights` — In-depth engineering articles, ERP blueprints, and industrial design insights.
   - `GET /careers` — Dynamic job listings loaded from database with modal application workflow.
   - `GET /gallery` — Photo gallery with category filtering and interactive lightbox viewer. Uploaded photos appear immediately.
   - `GET /contact` — Direct phone (`+91 63819 78782`), email, WhatsApp quick chat, Google Maps location, and message submission.

2. **Executive Admin Dashboard (`/admin`)**:
   - Secure authentication (`/admin/login`, `/admin/logout`).
   - Metric overview cards for quick stats.
   - **Career Jobs Manager**: Add, edit, delete, and toggle active/closed status for job postings.
   - **Client Partners Manager**: Add, edit, and delete organizations with logo uploads.
   - **Photo Gallery Manager**: Upload photos with title, category, and caption — saved to disk and visible immediately on the public gallery.
   - **Job Applications Inbox**: Review candidate applications and portfolio links.
   - **Contact Inquiries Inbox**: Review incoming client messages and project briefs.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+ (Tested on Python 3.13)
- PostgreSQL (or SQLite fallback)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration (PostgreSQL)
Set the `DATABASE_URL` environment variable or edit `.env`:
```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/jarmfabs_db
```
*(Note: If `DATABASE_URL` is omitted, the application automatically uses `sqlite:///jarmfabs.db` without errors).*

### 4. Initialize Database & Seed Data
```bash
python setup_db.py
```
This script creates all database tables and seeds initial clients, career openings, and default admin credentials.

### 5. Run the Server
```bash
python app.py
```
Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🔐 Admin Access

- **URL**: `/admin/login`
- **Manage Credentials**: Use `python change_admin.py` or set `ADMIN_USERNAME` and `ADMIN_PASSWORD` in your `.env` file.

---

## 📁 Project Structure

```
JARMFABS/
├── app.py                      # Flask application factory, routes & upload handlers
├── models.py                   # SQLAlchemy models (Job, Client, GalleryPhoto, etc.)
├── config.py                   # Application configuration & upload directories
├── setup_db.py                 # Database initialization & seeding script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── sitemap.xml                 # Search engine sitemap with dedicated URLs
├── robots.txt                  # Search engine crawler instructions
├── static/
│   ├── css/
│   │   ├── main.css            # Master design system & responsive styling
│   │   └── admin.css           # Admin dashboard stylesheet
│   ├── js/
│   │   ├── main.js             # Three.js 3D particles, lightbox, filter logic
│   │   └── admin.js            # Image upload previews & form validations
│   ├── images/                 # Brand assets (JarmFabs.png, logos)
│   └── uploads/
│       ├── gallery/            # Uploaded photo gallery files
│       └── clients/            # Uploaded client logo files
└── templates/
    ├── base.html               # Master website layout
    ├── index.html              # Home page
    ├── explore.html            # Explore Us
    ├── services.html           # Services Ecosystem
    ├── industries.html         # Target Industries
    ├── clients.html            # Client Partners
    ├── innovation.html         # Innovation Lab
    ├── insights.html           # Insights & Perspectives
    ├── careers.html            # Careers & Application Modal
    ├── gallery.html            # Photo Gallery & Lightbox
    ├── contact.html            # Contact & WhatsApp
    └── admin/
        ├── base_admin.html     # Admin layout
        ├── login.html          # Admin login
        ├── dashboard.html      # Admin dashboard
        ├── jobs.html           # Job openings list
        ├── job_form.html       # Job create/edit form
        ├── clients.html        # Client partners list
        ├── client_form.html    # Client create/edit form
        ├── gallery.html        # Gallery photo upload & manager
        ├── applications.html   # Candidate applications
        └── messages.html       # Contact inquiries
```

---

## 🛡️ Security Best Practices
- Passwords are encrypted using Werkzeug's PBKDF2/SHA-256 cryptographic hashing.
- File uploads are validated for allowed extensions (`.jpg`, `.png`, `.webp`, `.gif`, `.svg`) and sanitized using `secure_filename` with unique UUIDs to prevent directory traversal and name collisions.
- Upload file sizes are capped at 16 MB.
- All administrative routes are protected by the `@admin_required` session verification decorator.
