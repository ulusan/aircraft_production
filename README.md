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

