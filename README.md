# UniTrade

A Django web app where students in a university community can list, browse and buy second-hand items from each other safely.

![UniTrade screenshot](https://github.com/adamazmy/UniTrade2/assets/65075339/9320b026-4b45-4f83-bdb0-d46b32daef24)

Built in 2024 as a university team project. Authorship of individual views and modules is noted in the source.

## Features

- **Accounts:** sign-up with email and password using a custom user model (email as the username). New accounts stay inactive until the user follows a verification link sent by email.
- **Listings:** signed-in users can create listings with a title, brand, department, price, condition and description, and upload several images per listing.
- **Manage your listings:** a "current listings" page shows the user's own items; sellers can edit their listings and delete them (only the seller can edit or delete).
- **Browsing:** an all-products page, a page per department (Books & Literature, Tech, Sports & Leisure, Electronics & Computers, Education, Home Equipment, Film/TV/Music) and an item detail page with an image gallery.
- **Search:** search listings by title or department name.
- **Comments:** signed-in users can comment on a listing.
- **Admin:** products, images, departments, comments and users are registered in the Django admin.
- Static pages: about us, FAQ, terms and conditions, privacy policy.

## Tech stack

- Python 3.10+, Django 5.0
- SQLite (default Django database)
- Django templates with Bootstrap 5 and Font Awesome (via CDN)
- Pillow for image uploads
- Gmail SMTP (or any SMTP server) for verification emails

## Running locally

```bash
cd UniTrade/UniTrade

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configuration is read from environment variables; see .env.example.
export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY="any-long-random-string"
# Print verification emails to the terminal instead of sending them:
export EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

Notes:

- Department pages filter by department name, so create the departments in the admin (http://127.0.0.1:8000/admin/) before adding listings: `Books & Literature`, `Tech`, `Sports & Leisure`, `Electronics & Computers`, `Education`, `Home Equipments`, `Film, Tv, Music`.
- With the console email backend, copy the activation link from the terminal output to activate a new account.

## Project structure

```
UniTrade/UniTrade/
├── manage.py
├── requirements.txt
├── .env.example
├── UniTrade/        # Project settings and root URL configuration
├── accounts/        # Custom user model, sign-up, email verification, login
├── marketplace/     # Products, images, departments, comments, search; views and templates
├── static/          # Site images; uploaded product images are stored here (MEDIA_ROOT)
└── staticfiles/     # Output of collectstatic
```

## Limitations

This was a coursework project and is not production-ready. For example, there are no automated tests, and the search page only filters by title and department name.
