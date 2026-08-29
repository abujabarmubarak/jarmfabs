import os
from app import app
from models import db, AdminUser, Job, Client, GalleryPhoto

def init_database():
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("[OK] Database tables created successfully.")

        # Seed default admin user if no admin exists
        if AdminUser.query.count() == 0:
            default_user = os.environ.get('ADMIN_USERNAME', 'admin')
            default_pass = os.environ.get('ADMIN_PASSWORD', 'Admin@JarmFabs2026')
            admin = AdminUser(
                username=default_user,
                email='abujabarmubarak24@gmail.com'
            )
            admin.set_password(default_pass)
            db.session.add(admin)
            print(f"[OK] Initial admin created (username: '{default_user}')")

        # Seed initial clients if none exist
        if Client.query.count() == 0:
            clients = [
                Client(
                    name="Mohamed Sathak A J College of Engineering & Architecture",
                    tag="Education",
                    location="Chennai, Tamil Nadu",
                    logo_filename="msaj-sathak.jpeg",
                    website="https://www.msajce-edu.in",
                    description="Academic campus management, student portals, and departmental workflows.",
                    display_order=1
                ),
                Client(
                    name="Al Kabir",
                    tag="Business Solutions",
                    location="Client Partner",
                    logo_filename="akolp.jpg",
                    website="#",
                    description="Enterprise operations, ERP workflow integration, and digital reporting tools.",
                    display_order=2
                ),
                Client(
                    name="Online Learning Platform (OLP)",
                    tag="EdTech / SaaS",
                    location="Global Delivery",
                    logo_filename=None,
                    website="#",
                    description="Scalable cloud learning platform with course management, assessments, and analytics.",
                    display_order=3
                )
            ]
            db.session.add_all(clients)
            print("[OK] Seeded 3 initial client partners.")

        # Seed initial jobs if none exist
        if Job.query.count() == 0:
            jobs = [
                Job(
                    title="Senior Python / Flask Backend Engineer",
                    department="Engineering",
                    location="Tenkasi / Hybrid",
                    job_type="Full-time",
                    experience="2-4 Years",
                    description="Lead the design and development of scalable backend services, RESTful APIs, and database architectures for custom enterprise systems and SaaS applications.",
                    requirements="Proficiency in Python, Flask or Django, PostgreSQL/SQLAlchemy, Docker, Git, and API security best practices.",
                    is_active=True
                ),
                Job(
                    title="AI & Automation Solutions Engineer",
                    department="AI & Innovation",
                    location="Tenkasi / Hybrid",
                    job_type="Full-time",
                    experience="1-3 Years",
                    description="Build intelligent workflow automations, LLM/chat agent integrations, and document intelligence pipelines that reduce manual business bottlenecks.",
                    requirements="Experience with Python, LangChain/LlamaIndex, OpenAI/Gemini APIs, webhook architectures, and process automation tools.",
                    is_active=True
                ),
                Job(
                    title="UI/UX & Frontend Designer",
                    department="Design Studio",
                    location="Tenkasi / Remote",
                    job_type="Full-time",
                    experience="1-3 Years",
                    description="Design intuitive, high-fidelity user interfaces and build responsive, accessible web interfaces reflecting JarmFabs' signature craft and elegance.",
                    requirements="Strong portfolio in Figma, HTML5, CSS3, modern JavaScript, responsive layout principles, and design systems.",
                    is_active=True
                )
            ]
            db.session.add_all(jobs)
            print("[OK] Seeded 3 active career job listings.")

        # Seed initial gallery photo if none exist and file is available
        if GalleryPhoto.query.count() == 0:
            logo_src = os.path.join('static', 'images', 'JarmFabs.png')
            if os.path.exists(logo_src):
                dest = os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], 'jarmfabs_brand_identity.png')
                if not os.path.exists(dest):
                    import shutil
                    shutil.copy2(logo_src, dest)
                
                photo = GalleryPhoto(
                    title="JarmFabs Corporate Identity & Emblem",
                    category="Projects",
                    caption="Official JarmFabs Technologies brand identity — Where Creative Charm Meets Exceptional Technology.",
                    filename="jarmfabs_brand_identity.png",
                    display_order=1
                )
                db.session.add(photo)
                print("[OK] Seeded initial gallery photo.")

        db.session.commit()
        print("[OK] All initial data committed successfully.")

if __name__ == '__main__':
    print("Initializing JarmFabs Technologies Database...")
    init_database()
    print("Database setup complete!")
