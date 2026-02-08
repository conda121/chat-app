# chat-app
# Real-Time Chat Application

A modern, full-stack real-time chat application built with FastAPI and React. Features include user authentication, channel-based messaging, WebSocket support for instant communication, and a clean, responsive UI.

![Chat App](https://img.shields.io/badge/version-1.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![React](https://img.shields.io/badge/React-19.2.3-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9.5-blue)

## Features

### 🔐 Authentication
- User registration and login
- JWT token-based authentication
- Secure password hashing with bcrypt
- Protected routes and WebSocket connections

### 💬 Real-Time Messaging
- Instant message delivery via WebSockets
- Message history with pagination
- Connection status indicators
- Automatic reconnection on disconnect
- User join/leave notifications

### 📁 Channel Management
- Create channels with custom names and descriptions
- Join and leave channels
- View all channels you're a member of
- Channel-based message isolation

### 🎨 Modern UI
- Clean, responsive design
- Split-panel layout (channels + chat)
- Message grouping by date
- User avatars and timestamps
- Real-time connection status

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **PostgreSQL** - Relational database
- **SQLAlchemy** - SQL toolkit and ORM
- **WebSockets** - Real-time bidirectional communication
- **JWT** - Secure authentication tokens
- **Passlib** - Password hashing

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **WebSocket API** - Real-time communication
- **Context API** - State management

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py              # Dependency injection
│   │   │   └── routes/
│   │   │       ├── auth.py          # Authentication endpoints
│   │   │       ├── channels.py      # Channel endpoints
│   │   │       ├── messages.py      # Message endpoints
│   │   │       ├── users.py         # User endpoints
│   │   │       └── websocket.py     # WebSocket endpoint
│   │   ├── core/
│   │   │   ├── config.py            # Configuration settings
│   │   │   └── security.py          # Security utilities
│   │   ├── models/
│   │   │   ├── user.py              # User model
│   │   │   ├── channel.py           # Channel model
│   │   │   └── message.py           # Message model
│   │   ├── schemas/
│   │   │   ├── user.py              # User schemas
│   │   │   ├── channel.py           # Channel schemas
│   │   │   └── message.py           # Message schemas
│   │   ├── services/
│   │   │   ├── user_service.py      # User business logic
│   │   │   ├── channel_service.py   # Channel business logic
│   │   │   └── message_service.py   # Message business logic
│   │   ├── websocket/
│   │   │   └── connection_manager.py # WebSocket manager
│   │   ├── database.py              # Database configuration
│   │   └── main.py                  # Application entry point
│   ├── requirements.txt             # Python dependencies
│   └── test_websocket.py            # WebSocket testing script
│
└── frontend/
    ├── public/
    │   └── index.html               # HTML template
    ├── src/
    │   ├── components/
    │   │   ├── ChannelList.tsx      # Channel list component
    │   │   ├── ChatWindow.tsx       # Main chat window
    │   │   ├── CreateChannel.tsx    # Channel creation modal
    │   │   ├── MessageInput.tsx     # Message input component
    │   │   └── MessageList.tsx      # Message list component
    │   ├── contexts/
    │   │   └── AuthContext.tsx      # Authentication context
    │   ├── pages/
    │   │   ├── Login.tsx            # Login page
    │   │   ├── Register.tsx         # Registration page
    │   │   └── Chat.tsx             # Main chat page
    │   ├── services/
    │   │   ├── api.ts               # API client
    │   │   └── websocket.ts         # WebSocket service
    │   ├── types/
    │   │   └── index.ts             # TypeScript types
    │   ├── App.tsx                  # Main app component
    │   └── index.tsx                # React entry point
    └── package.json                 # Node dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE chatdb;
   CREATE USER chatuser WITH PASSWORD 'chatpass';
   GRANT ALL PRIVILEGES ON DATABASE chatdb TO chatuser;
   ```

5. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://chatuser:chatpass@localhost:5432/chatdb
   SECRET_KEY=your-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user info

### Channels
- `GET /api/v1/channels/` - Get all channels for current user
- `POST /api/v1/channels/` - Create a new channel
- `GET /api/v1/channels/{channel_id}` - Get specific channel
- `POST /api/v1/channels/{channel_id}/join` - Join a channel
- `POST /api/v1/channels/{channel_id}/leave` - Leave a channel

### Messages
- `GET /api/v1/channels/{channel_id}/messages` - Get channel messages

### WebSocket
- `WS /ws/{channel_id}?token={jwt_token}` - Connect to channel WebSocket

## Usage

### Creating an Account
1. Navigate to the registration page
2. Enter username, email, and password
3. Click "Register" to create your account

### Joining a Chat
1. Log in with your credentials
2. Create a new channel or select an existing one
3. Start chatting in real-time!

### Sending Messages
1. Type your message in the input field at the bottom
2. Press Enter or click "Send"
3. Your message will be delivered instantly to all channel members

## WebSocket Testing

A test script is included to test WebSocket functionality:

```bash
python test_websocket.py <jwt_token> <channel_id> <username>
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `hashed_password` - Bcrypt hashed password
- `created_at` - Account creation timestamp
- `last_seen` - Last activity timestamp

### Channels Table
- `id` - Primary key
- `name` - Unique channel name
- `description` - Optional description
- `created_by` - Foreign key to users
- `created_at` - Channel creation timestamp

### Messages Table
- `id` - Primary key
- `content` - Message text
- `user_id` - Foreign key to users
- `channel_id` - Foreign key to channels
- `created_at` - Message timestamp

### User_Channels Table (Association)
- `user_id` - Foreign key to users
- `channel_id` - Foreign key to channels

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Protected API endpoints
- WebSocket authentication via token
- CORS middleware configuration
- SQL injection protection via SQLAlchemy ORM

## Development

### Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend WebSocket test
cd backend
python test_websocket.py <token> <channel_id> <username>
```

### API Documentation
Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Production Deployment

### Backend
1. Set secure `SECRET_KEY` in environment variables
2. Update `DATABASE_URL` with production database
3. Configure CORS to allow only your frontend domain
4. Use a production WSGI server (e.g., Gunicorn with Uvicorn workers)
5. Set up SSL/TLS certificates

### Frontend
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `build` folder with a web server (Nginx, Apache, etc.)
3. Update API URL to point to production backend

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- FastAPI for the excellent web framework
- React team for the powerful UI library
- SQLAlchemy for robust ORM functionality

## Support

For issues, questions, or contributions, please open an issue in the repository.

---
