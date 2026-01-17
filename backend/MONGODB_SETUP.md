# MongoDB Configuration Guide

## Overview

The application now uses environment variables for MongoDB connection, allowing you to easily switch between local MongoDB, MongoDB with authentication, or MongoDB Atlas (cloud).

## Configuration Options

### 1. Local MongoDB (Default)

For a local MongoDB instance running on your machine:

```env
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=contribution_tracking_db
```

This is the default configuration and works with MongoDB running locally on port 27017.

### 2. MongoDB Atlas (Cloud)

For MongoDB Atlas cloud database:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=contribution_tracking_db
```

**Steps to set up MongoDB Atlas:**

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new cluster
4. Create a database user (Database Access → Add New Database User)
5. Whitelist your IP address (Network Access → Add IP Address)
6. Get your connection string (Clusters → Connect → Connect your application)
7. Replace `<username>`, `<password>`, and `<cluster>` in the URI

### 3. MongoDB with Authentication

For local MongoDB with username/password:

```env
MONGO_URI=mongodb://<username>:<password>@localhost:27017/
DATABASE_NAME=contribution_tracking_db
```

### 4. MongoDB with Custom Host/Port

For MongoDB running on a different host or port:

```env
MONGO_URI=mongodb://192.168.1.100:27017/
DATABASE_NAME=contribution_tracking_db
```

## Environment File Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your MongoDB connection details

3. **Keep `.env.example` as a template** for other developers (without real credentials)

## Important Notes

- ✅ `.env` is in `.gitignore` - your credentials won't be committed to git
- ✅ `.env.example` should be committed - it serves as a template
- ✅ Never share your `.env` file or commit it to version control
- ✅ The application falls back to `mongodb://localhost:27017/` if `MONGO_URI` is not set

## Testing the Connection

After updating your `.env` file, restart the backend server:

```bash
python -m uvicorn app.main:app --reload
```

If the connection is successful, you should see:
- No MongoDB connection errors in the console
- API endpoints responding normally
- Data being saved/retrieved from your database

## Troubleshooting

### Connection Refused
- Make sure MongoDB is running (`mongod` service)
- Check if the port is correct (default: 27017)

### Authentication Failed
- Verify username and password are correct
- Ensure the user has the correct permissions on the database

### MongoDB Atlas Connection Issues
- Check your IP is whitelisted in Network Access
- Verify the connection string is complete
- Ensure your database user has read/write permissions

## Complete `.env` Example

```env
# ================================
# DATABASE CONFIGURATION
# ================================

# Choose ONE of the following:

# Option 1: Local MongoDB (Default)
MONGO_URI=mongodb://localhost:27017/

# Option 2: MongoDB Atlas
# MONGO_URI=mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority

# Option 3: Local with Auth
# MONGO_URI=mongodb://admin:password123@localhost:27017/

DATABASE_NAME=contribution_tracking_db

# ================================
# OTHER SETTINGS
# ================================

JWT_SECRET_KEY=your-secret-key-change-this-in-production-123456789
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Next Steps

1. Choose your MongoDB setup (local, Atlas, or authenticated)
2. Update your `.env` file with the appropriate `MONGO_URI`
3. Restart the backend server
4. Your application will now connect to your chosen MongoDB instance!
