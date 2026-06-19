# Vulnerability Management Dashboard

A Django web application for tracking vulnerabilities and visualizing security data through interactive dashboard charts.

The project includes user authentication, protected dashboard pages, database-backed vulnerability records, severity-based charts, date-based trends, and AJAX-powered dynamic visualizations using Highcharts.

## Features

- User registration and login
- Protected dashboard pages
- Vulnerability records stored in a database
- Severity-based vulnerability overview
- Vulnerability trends by publication date
- Dynamic charts loaded with AJAX
- Highcharts data visualizations
- Bootstrap-based interface
- Django ORM queries
- Raw SQL example for grouped security data

## Technologies Used

- Python
- Django
- SQLite
- Django ORM
- HTML
- CSS
- Bootstrap
- JavaScript
- jQuery
- AJAX
- Highcharts

## Project Structure

```text
dw/
├── accounts/
├── back/
├── setari/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

## Main Pages

### Home

Landing page that introduces the project and gives access to the dashboard, login, or registration pages.

### Authentication

Users can create an account, log in, and access protected dashboard pages.

### Severity Overview

Displays the total number of vulnerabilities grouped by severity level.

### Severity Timeline

Displays vulnerability severity levels across publication dates.

### Daily Trends

Displays the number of vulnerabilities published on each date.

### Dynamic Charts

Loads chart data dynamically using AJAX and displays multiple vulnerability charts without reloading the page.

## Installation

Clone the repository:

```bash
git clone https://github.com/chrispsk/dw.git
cd dw
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

For local development, create a `.env` file or configure your environment variables manually.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Database Setup

Run migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Usage

1. Register a new user account.
2. Log in using your credentials.
3. Open the dashboard pages from the navigation bar.
4. View vulnerability charts by severity and publication date.
5. Use the dynamic charts page to load chart data with AJAX.

## Data Visualization

The dashboard uses Highcharts to display vulnerability data in different formats:

- Bar chart for vulnerabilities grouped by severity
- Column chart for severity distribution by date
- Column chart for daily vulnerability trends
- AJAX-loaded charts for dynamic dashboard content

## Security Notes

This project is intended for learning and portfolio purposes.

Recommended production improvements:

- Keep `SECRET_KEY` outside the source code
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS`
- Use a production database instead of SQLite
- Add input validation and form error handling
- Add automated tests
- Configure static files properly for deployment

## Possible Improvements

- Add CRUD functionality for vulnerabilities
- Add filtering by severity and date
- Add search functionality
- Add pagination for vulnerability records
- Add role-based permissions
- Add downloadable reports
- Add automated tests
- Improve dashboard styling
- Deploy the project online

## License

This project does not currently include a license.
