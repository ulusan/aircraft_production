# Aircraft Production Application

## Overview
The Aircraft Production Application is a backend-focused project developed with Django to manage the production and assembly of aircraft parts. The application is designed to facilitate CRUD operations for various teams, ensure compliance with part responsibilities, and track the production and assembly processes efficiently.

## Features
- **Personnel Login:** Authentication system to log in personnel.
- **Team Assignment:** Each personnel belongs to a specific team, and multiple personnel can belong to the same team.
- **Part Management:** Teams can create, list, and delete parts based on their responsibilities.
- **Responsibility Enforcement:** Teams cannot produce parts outside their designated responsibilities.
- **Aircraft Assembly:** Combines compatible parts to assemble aircraft.
- **Inventory Warnings:** Alerts users if any required part is missing for assembly.
- **Part Usage Tracking:** Ensures that parts used in one aircraft cannot be reused in another and maintains stock counts.
- **Production History:** Tracks which parts were used in which aircraft.


## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Running the Project](#running-the-project)
4. [Docker Usage](#docker-usage)
5. [API Endpoints](#api-endpoints)

## Application Entities
### Parts
- Wing
- Fuselage
- Tail
- Avionics

### Aircraft
- TB2
- TB3
- AKINCI
- KIZILELMA

### Teams
- Wing Team
- Fuselage Team
- Tail Team
- Avionics Team
- Assembly Team

## Technologies Used
- **Backend:** Python, Django, Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Deployment:** Docker
- **Additional Tools:** Swagger for API documentation

## Installation Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/aircraft-production.git
   cd aircraft-production
   ```
2. **Set Up Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Docker:**
   Ensure Docker is installed and running on your machine. Then, build and run the containers:
   ```bash
   docker compose up --build
   ```
5. **Apply Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the Application:**
   Open `http://127.0.0.1:8000/` in your browser.

## API Usage Examples
### Swagger Documentation
Access Swagger UI for detailed API documentation:
```
http://127.0.0.1:8000/swagger/
```

### Endpoints
- **Parts API:**
  - `GET /api/parts/` - List all parts
  - `POST /api/parts/` - Create a new part
  - `PUT /api/parts/{id}/` - Update an existing part
  - `DELETE /api/parts/{id}/` - Delete a part

- **Teams API:**
  - `GET /api/teams/` - List all teams
  - `POST /api/teams/` - Create a new team

- **Assembly API:**
  - `POST /api/assemble/` - Assemble an aircraft

## Notes
- A simple interface is sufficient; use ready-made templates for the frontend if needed.
- The project duration is 5 days.

## Extras (Bonus Features)
- **Deployment:** Dockerized for seamless deployment.
- **Documentation:** Well-prepared README and Swagger API documentation.
- **Asynchronous Features:** Utilized Ajax for real-time updates.
- **Frontend Enhancements:** Bootstrap and Tailwind CSS used for styling.
- **Additional Django Libraries:** Included Django Debug Toolbar for debugging.

## Contribution
Contributions are welcome! Please fork the repository and create a pull request for major changes.

## License
This project is licensed under the MIT License.

---
For further queries, contact the repository owner at [infoulusan@gmail.com].

# Aircraft Production Application

This README provides instructions to set up and run the Aircraft Production Application using Django and Docker.


## Project Overview

The Aircraft Production Application is a Django-based project for managing aircraft part production, team roles, and assembly processes. It uses PostgreSQL as the database and Django Rest Framework for the API backend.

## Installation and Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Docker and Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ulusan/aircraft_production.git
   cd aircraft-production
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:

   ```bash
   psql -U postgres
   CREATE DATABASE uav_db;
   CREATE USER ulusan WITH PASSWORD 'ulusan';
   GRANT ALL PRIVILEGES ON DATABASE uav_db TO ulusan;
   ```

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser for the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

## Running the Project

### Local Development

1. Start the server:
   ```bash
   python manage.py runserver
   ```
2. Open your browser and navigate to the following URLs:
   - Home: [http://localhost:8000](http://localhost:8000)
   - Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)
   - Swagger API Docs: [http://localhost:8000/swagger](http://localhost:8000/swagger)

## Docker Usage

### Build and Run with Docker Compose

1. Build the Docker image:

   ```bash
   docker compose build
   ```

2. Start the containers:

   ```bash
   docker compose up
   ```

3. The application will be available at:

   - [http://localhost:8000](http://localhost:8000)

4. To stop the containers:

   ```bash
   docker compose down
   ```

## API Endpoints

| Endpoint              | Description                 |
| --------------------- | --------------------------- |
| `/api/token/`         | Obtain JWT token            |
| `/api/token/refresh/` | Refresh JWT token           |
| `/api/register/`      | User registration           |
| `/admin/`             | Admin panel                 |
| `/swagger/`           | API documentation (Swagger) |
| `/assemble-aircraft/` | Assemble an aircraft        |

## Notes

- Ensure the `.env` file is properly set up for Docker configuration if required.
- Debugging tools (like `debug_toolbar`) are enabled only in development mode.

### pgAdmin
pgAdmin is a web-based administration tool for PostgreSQL. Follow these steps to set it up:

1. Access pgAdmin at:
   - [http://localhost:8080](http://localhost:8080) (if Docker is used with default settings).

2. Login with the default credentials:
   - Email: `baykar@baykar.com`
   - Password: `baykar`

3. Add a new server:
   - Hostname: `db`
   - Port: `5432`
   - Username: `ulusan`
   - Password: `ulusan`

### Swagger
Swagger provides interactive API documentation. Access it at:
   - [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

