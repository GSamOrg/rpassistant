# RPG Campaign Assistant

A web-based role-playing game assistant designed to help Dungeon Masters (DMs) prepare campaigns, generate NPCs on-the-fly during sessions, and create session recaps from audio recordings.

## Features

- **Collaborative Campaign Planning**: Dynamic document editor with AI assistance
- **On-the-Fly NPC Generation**: Interactive chat interface for creating NPCs during sessions
- **Session Recap Generation**: Audio-to-text transcription with AI-generated summaries
- **Discord Integration**: Push session recaps to Discord servers
- **Multi-System Support**: Call of Cthulhu, D&D 5e, Pathfinder, and more

## Tech Stack

- **Backend**: Python FastAPI with PostgreSQL database
- **Frontend**: SvelteJS with TailwindCSS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with OAuth support (Google, Discord)

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL
- Docker (optional)

### Backend Setup

1. Start the database:
```bash
docker-compose up -d postgres
```

2. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── migrations/          # Database migrations
│   └── tests/              # Backend tests
├── frontend/
│   ├── src/
│   │   ├── lib/            # Shared components and stores
│   │   ├── routes/         # SvelteKit routes
│   │   └── app.html        # HTML template
│   └── static/             # Static assets
└── docker-compose.yml      # Development services
```

## Development

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

### API Documentation

The FastAPI backend automatically generates OpenAPI documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.