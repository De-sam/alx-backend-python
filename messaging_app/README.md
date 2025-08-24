# Hey! Messaging App

A modern, secure messaging application built with Django REST Framework featuring OAuth2 authentication and real-time messaging capabilities.

## Key Features

### Authentication & Security
- **OAuth2 Provider Integration** - Secure API authentication with PKCE (Proof Key for Code Exchange)
- **Custom User Model** - Extended user model with email, phone number, and profile information
- **Token-based Authentication** - Access tokens with configurable expiration and refresh tokens
- **Scope-based Permissions** - Granular access control for different API operations

### Messaging Features
- **Real-time Conversations** - Create and manage multi-participant conversations
- **Message Status Tracking** - Track message delivery status (pending, sent, delivered, read)
- **Message History** - Complete chat history with pagination support
- **Nested API Endpoints** - RESTful API with nested conversation-message relationships

### Technical Architecture
- **Django REST Framework** - Robust API development with serializers and viewsets
- **Custom Permissions** - Role-based access control and conversation participant validation
- **Database Optimization** - Efficient queries with proper indexing and relationships
- **API Documentation** - Self-documenting API with browsable endpoints

## Technology Stack

- **Backend**: Django 5.2.4, Django REST Framework
- **Authentication**: OAuth2 Provider with PKCE
- **Database**: SQLite (development), supports PostgreSQL/MySQL
- **API**: RESTful API with nested routing
- **Pagination**: Page-based pagination with configurable page size

## API Endpoints

### Authentication
- `POST /o/token/` - OAuth2 token endpoint
- `POST /o/revoke_token/` - Token revocation
- `GET /o/authorize/` - OAuth2 authorization

### Core API
- `GET/POST /api/users/` - User management
- `GET/POST /api/conversations/` - Conversation management
- `GET/POST /api/messages/` - Message operations
- `GET /api/chats/` - Chat history

### Nested Endpoints
- `GET/POST /api/conversations/{id}/messages/` - Messages within conversations

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd messaging_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv msg_venv
   source msg_venv/bin/activate  # On Windows: msg_venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

##  OAuth2 Configuration

The application uses OAuth2 with the following scopes:
- `read:messages` - Read user messages
- `send:messages` - Send messages on behalf of the user
- `manage:conversations` - Create, update, or delete conversations

### Token Settings
- **Access Token Expiration**: 1 hour
- **Refresh Token Expiration**: 1 week
- **PKCE Required**: Yes (for enhanced security)
- **Token Rotation**: Enabled

## Data Models

### User Model
- Custom user model extending `AbstractBaseUser`
- Email-based authentication
- Phone number and profile information
- Staff and active status flags

### Conversation Model
- Multi-participant conversations
- Automatic timestamp tracking
- Participant management

### Message Model
- Message content and metadata
- Status tracking (pending, sent, delivered, read)
- Conversation association
- Timestamp tracking

### Chat Model
- Chat history and metadata
- Message association
- Timestamp tracking

## Security Features

- **PKCE Implementation** - Prevents authorization code interception attacks
- **Token Expiration** - Short-lived access tokens with refresh capability
- **Scope Validation** - Granular permission control
- **Participant Validation** - Users can only access conversations they're part of
- **Input Validation** - Comprehensive message content validation

## Testing

The application includes comprehensive test coverage:
- Model validation tests
- API endpoint tests
- Permission and authentication tests
- Serializer validation tests

## API Examples

### Create a Conversation
```json
POST /api/conversations/
{
    "participants": [1, 2]
}
```

### Send a Message
```json
POST /api/messages/
{
    "conversation": 14,
    "message_body": "Hello, how are you?"
}
```

### Get Conversation Messages
```
GET /api/conversations/14/messages/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.


 
