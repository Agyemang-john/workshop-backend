# Event & Workshop Registration Platform

## Overview
This web application is designed to help students find and register workshops and events efficiently using customizable forms provided by the organisers. And also Organizers can create, edit, and delete workshops, manage registrations, and export attendee data in Excel and other formats.

## Features
- **Filtering for student to easily find workshops** 
- **Search function for student to easily find workshops** 
- **Workshop Detail page for students to easily read more about workshops** (Location, Time, Speaker(s) Completed or Incoming, Duration, etc)
- **Modal for registration with scrolling(if many)** 
- **Alert to Help students know the submission went through or could not submit** 
- **Admin Dashboard** for organizers to manage workshops and registration forms.
- **Custom Form Builder** to modify registration forms anytime.
- **Attendee Management** to view and manage registrants.
- **Data Export** in Excel and other formats for record-keeping.
- **Email Reminders** sent to attendees a day before the workshop.
- **Subscription System** for newsletters.
- **Authentication System** for organizers (Sign In/Up, Password Management).

## Link To Project Video
- `https://drive.google.com/file/d/1z6vbF4toXBhW89rMwFd10Y6pRAjRnFm1/view?usp=sharing`

## Link To Website
- `https://workshop-seven-eta.vercel.app`

## Link To Website Dashboard
- `https://workshop-nfwx.onrender.com/dashboard`

- Email - workshop@gmail.com
- Passowrd - workshop@2025


## Link To Frontend Repo
- `https://github.com/Agyemang-john/workshop-frontend.git`

## Link To Backend Repo
- `https://github.com/Agyemang-john/workshop-backend.git`


## Tech Stack
### Frontend
- Next.js (TypeScript, Tailwind CSS, Material UI)

### Backend
- Django (Django REST Framework, Celery, Jazzmin Admin Theme)

### Database
- PostgreSQL (Production)
- SQLite3 (Development)

## API Endpoints
```python
urlpatterns = [
    path('workshops/', WorkshopListView.as_view(), name='workshops-list'),
    path('workshop/<slug:slug>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('register/', RegistrationView.as_view(), name='workshop-register'),
    path('subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
    path('workshops/search/', WorkshopSearchView.as_view(), name='workshop-search'),
    path('workshop/<int:workshop_id>/fields/', WorkshopFieldsView.as_view(), name='workshop-fields'),
    path('workshop/<int:workshop_id>/register/', RegisterAttendeeView.as_view(), name='workshop-register'),
]
```
- **Authentication**: Session-based for the admin dashboard.
- **Task Scheduling**: Celery beat handles email reminders for attendees.

## Frontend Details
### Pages
- **Home Page**
- **Workshop Details Page**
- **About Page**
- **Admin Dashboard**
  - View all registrants
  - Export registrant details to Excel/other formats
  - Create, edit, and delete workshops
  - Modify custom fields
  - Set email reminders
- **Authentication Pages** (Sign In, Sign Up, Change Password)

## Installation & Setup
### Frontend
1. Install Node.js
2. Clone the repository: `git clone [https://github.com/Agyemang-john/workshop-frontend.git]`
3. Navigate to the directory: `cd frontend`
4. Install dependencies: `npm install`
5. Update API endpoint in `.env` to point to the backend
6. Run the server: `npm run dev`

### Backend
1. Install Python
2. Clone the repository: `git clone [https://github.com/Agyemang-john/workshop-backend.git]`
3. Navigate to the directory: `cd backend`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up database (PostgreSQL/Cloudinary for media storage)
6. Apply migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
8. Run the backend server:
   ```sh
   python manage.py runserver
   ```
9. Start Celery worker and Redis queue:
   ```sh
   celery -A backend worker --loglevel=info
   celery -A backend beat --loglevel=info
   ```

## Usage Instructions
### Logging In
1. Navigate to the login page.
2. Enter your email and password.
3. After logging in, you can create and manage workshops.

### Creating a Workshop & Custom Fields
1. Create a category and speakers.
2. Add a new workshop and input the required fields.
3. Under the **Custom Fields** tab, define attendee form fields.
   - Example:
     ```json
     [
       {"label": "Department", "type": "text", "required": false},
       {"label": "Institution", "type": "dropdown", "choices": ["KNUST", "UCC", "UG"]},
       {"label": "CV", "type": "file", "required": false},
       {"label": "Phone Number", "type": "number", "required": false}
     ]
     ```
4. Uncheck "Required" if the field is optional.

### Viewing Registrants
1. Go to the **Registrations** section.
2. View registrants for each workshop.
3. Use search and sorting features to filter attendees.
4. Add responses or export data.

### Exporting Data to Excel
1. Click the **Export** button on the registrant page.
2. Select the fields to include in the Excel file.
3. Download the file for external use.

## Contributing
This is a public repository, and contributions are welcome! Clone the repo and follow the setup instructions to contribute.

## License
No license assigned.

