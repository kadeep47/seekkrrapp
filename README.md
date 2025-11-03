# Seeker Platform

A modular, scalable location-based questing platform that supports web applications, mobile applications (Android and iOS), and a backend API.

## Project Structure

```
seeker/
├── content/                    # React web application
├── backend/                   # FastAPI backend server
├── apps/mobile/              # Flutter mobile application
├── .github/workflows/        # CI/CD pipelines
├── docker-compose.yml        # Local development environment
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for web development)
- Python 3.11+ (for backend development)
- Flutter 3.16+ (for mobile development)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd seeker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Redis cache on port 6379
   - Backend API on port 8000
   - Web application on port 3000

4. **Access the applications**
   - Web App: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - API Redoc: http://localhost:8000/redoc

### Individual Component Setup

#### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Web Development

```bash
cd content
npm install
npm run dev
```

#### Mobile Development

```bash
cd apps/mobile
flutter pub get
flutter run
```

## Architecture

The Seeker platform follows a modern, scalable architecture:

- **Backend**: FastAPI with PostgreSQL and Redis
- **Web**: React with TypeScript, Vite, and Tailwind CSS
- **Mobile**: Flutter with BLoC pattern and Material Design 3
- **API-First**: All functionality exposed through well-defined REST APIs
- **Containerized**: Docker support for consistent development environments

## Features

- 🔐 **Authentication**: JWT-based auth with OAuth support
- 🗺️ **Location-Based Quests**: GPS-enabled quest participation
- 🏆 **Rewards & Achievements**: Point system and leaderboards
- 👥 **Social Features**: Groups, friends, and activity feeds
- 📱 **Cross-Platform**: Web and mobile applications
- 🚀 **Scalable**: Designed to grow from MVP to enterprise

## Development Workflow

1. **Backend First**: Implement API endpoints and business logic
2. **API Documentation**: Maintain OpenAPI specifications
3. **Client Development**: Build web and mobile interfaces
4. **Testing**: Unit, integration, and end-to-end tests
5. **Deployment**: Automated CI/CD pipelines

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions and support, please open an issue in the GitHub repository.