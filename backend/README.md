# Behavior-Aware and Ethical Automated Fund Collection System

**A human-centric, AI-driven platform for community welfare organizations.**

Traditional automated systems treat all members identically, issuing fixed reminders that often lead to fatigue and reduced trust. This system is different. It functions as a decision-support and engagement platform, analyzing member behavior to predict delays and delivering personalized, non-coercive "nudges" that encourage timely contributions while preserving dignity and privacy.

## 🌟 Innovation Highlights

- **Behavior-Aware Intelligence**: Moves beyond rule-based logic to understand individual payment patterns.
- **Predictive Fund Management**: Anticipates delays before they happen using behavioral analytics.
- **Ethical Nudging**: Generates personalized, respectful reminders grounded in behavioral economics—no generic spam.
- **Explainable Insights**: Provides administrators with clear, privacy-conscious visibility into contribution trends.
- **Human-Centric Design**: Prioritizes member trust and community health over punitive enforcement.

## 🎯 Core Objectives

- **Automate** fund collection and tracking without losing the personal touch.
- **Model** individual member behavior to understand "why" payments are delayed.
- **Predict** likely delays to enable proactive, empathetic intervention.
- **Nudge** members ethically, increasing consistency without pressure.
- **Strengthen** community trust by linking contributions to impact.

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local or MongoDB Atlas)
- SMTP server for email notifications (Gmail recommended)

## 🛠️ Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   
   Create a `.env` file in the backend directory:
   ```env
   # MongoDB Configuration
   MONGO_URI=mongodb://localhost:27017/
   # or for MongoDB Atlas:
   # MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

   # JWT Configuration
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24

   # CORS Configuration
   FRONTEND_URL=http://localhost:5173

   # Email Configuration (Gmail SMTP)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-specific-password
   EMAIL_FROM=your-email@gmail.com

   # SMS Configuration (optional)
   SMS_API_KEY=your-sms-api-key
   SMS_SENDER_ID=your-sender-id
   ```

   > **Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

6. **Initialize the database** (optional - creates demo data)
   ```bash
   python init_db.py
   ```

## 🚀 Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### Demo Credentials

After running `init_db.py`, you can use these demo accounts:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Member Account:**
- Username: `member1`
- Password: `member123`

### API Authentication Flow

1. **Login**: POST `/auth/login`
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```

2. **Use the token**: Include in headers
   ```
   Authorization: Bearer <your-token>
   ```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                # Main FastAPI application with lifespan management
│   ├── auth.py                # JWT utilities and password hashing
│   ├── models.py              # Pydantic models
│   ├── db.py                  # MongoDB connection and collections
│   ├── dependencies.py        # FastAPI dependencies (auth, etc.)
│   ├── utilities.py           # Helper functions (validation, classification)
│   ├── intelligence.py        # Predictive analytics & adaptive messaging
│   ├── notifications.py       # Email and SMS notification engine
│   ├── scheduler.py           # Automated reminder scheduler (NEW)
│   └── routers/
│       ├── auth_routes.py     # Authentication endpoints
│       ├── member_routes.py   # Member dashboard endpoints
│       ├── admin_routes.py    # Admin management endpoints
│       ├── contribution_routes.py  # Payment tracking
│       ├── ticket_routes.py   # Member support tickets
│       ├── prediction_routes.py    # Analytics endpoints
│       └── password_routes.py      # Password management
├── scripts/
│   ├── init_db.py             # Database initialization
│   └── verify_vision.py       # System verification script
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (create this)
```

## 🔑 Key Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `GET /auth/me` - Get current user profile

### Member Interface
- `GET /member/dashboard` - Member's personal dashboard
- `GET /member/contributions` - Member's contribution history
- `GET /member/notifications` - Member's notification history
- `PUT /member/preferences` - Update notification preferences

### Admin Interface
- `POST /admin/members` - Register new member
- `GET /admin/members` - Get all members with statistics
- `GET /admin/predictions` - Get payment delay predictions
- `GET /admin/member/{member_id}/insights` - Deep insights for a member
- `POST /admin/reminder/{member_id}` - Send manual reminder
- `GET /admin/dashboard/stats` - Dashboard statistics

### Automated Reminder System (NEW)
- `GET /admin/reminders/schedule` - View automated scheduler status
- `POST /admin/reminders/trigger` - Manually trigger reminder check
- `GET /admin/reminders/history` - View reminder sending history

## 🤖 Predictive Analytics

The system uses a machine learning-based approach to predict payment delays:

- Analyzes historical payment patterns
- Calculates average delay days
- Counts missed payments
- Predicts next payment delay probability
- Classifies members as Regular / Occasional Delay / High-risk Delay

## 📧 Automated Reminder System

### Priority-Based Sending

The system includes an intelligent, automated reminder scheduler that sends emails based on member risk level:

**High-Risk Members ("Early Reminder" Priority)**
- Receive reminders **7 days before** due date
- Proactive approach to improve collection timeliness
- Classified as "High-risk Delay" based on payment history

**Regular Members ("Normal" Priority)**
- Receive reminders **3 days before** due date
- Standard reminder timeline
- Includes "Regular" and "Occasional Delay" classifications

### Features

- **✅ Automated Daily Execution**: Runs every day at 9:00 AM
- **✅ Manual Trigger**: Admin can trigger immediately via dashboard
- **✅ Intelligent Content**: Uses behavioral economics for ethical nudging
- **✅ Duplicate Prevention**: Won't send multiple reminders within 2 days
- **✅ Full Logging**: Every reminder logged to MongoDB
- **✅ Error Resilience**: Handles database connection issues gracefully
- **✅ SMTP Integration**: Beautiful HTML emails via Gmail

### Technical Implementation

- **Scheduler**: APScheduler (AsyncIOScheduler)
- **Email Engine**: aiosmtplib with HTML templates  
- **Content Generation**: Intelligence engine with psychological frameworks
- **Storage**: notifications_collection in MongoDB

### Notification System

Features include:
- Automated reminders for upcoming and overdue payments
- **Priority-based timing** (7 days vs 3 days)
- Personalized messages based on member history and classification
- Support for email and SMS (SMS requires API key)
- Member preference management (opt-in/opt-out for email)
- Manual trigger capability for admins
- Complete audit trail via reminder history endpoint

## 🔒 Security Best Practices

- Change `JWT_SECRET` to a strong, random value in production
- Use environment variables for all sensitive data
- Enable HTTPS in production
- Configure CORS properly for your frontend domain
- Use MongoDB Atlas with IP whitelisting in production
- Regularly rotate JWT secrets
- Implement rate limiting (recommended for production)

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MongoDB is running: `mongod --version`
- Check `MONGO_URI` in `.env` file
- For Atlas, ensure IP whitelist is configured

### Email Not Sending
- Verify Gmail App Password is correct
- Check firewall settings for port 587
- Ensure "Less secure app access" is disabled (use App Passwords)

### Authentication Errors
- Clear browser localStorage
- Verify JWT_SECRET is consistent
- Check token expiration settings

## 📝 Database Schema

The system uses three main collections:

1. **members** - User accounts and profiles
2. **contributions** - Payment records and tracking
3. **notifications** - Notification history and preferences
4. **predictions** - ML-generated payment predictions

## 🔄 Development

### Adding New Endpoints
1. Add route in `main.py`
2. Create Pydantic models in `models.py`
3. Update documentation strings
4. Test with Swagger UI

### Modifying Prediction Algorithm
- Edit `intelligence.py`
- Adjust weights and thresholds as needed
- Test with various payment patterns

## 📦 Dependencies

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **PyMongo** - MongoDB driver
- **Pydantic** - Data validation
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **aiosmtplib** - Async email sending

## 📄 License

This project is proprietary software for church management.

## 👥 Support

For issues or questions, contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: January 2026
