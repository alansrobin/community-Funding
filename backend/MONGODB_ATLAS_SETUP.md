# MongoDB Atlas Setup Guide

## Quick Setup Steps

### 1. Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a **FREE** account (no credit card required)
3. Create a new project (e.g., "Contribution Tracking")

### 2. Create a Cluster
1. Click **"Build a Database"**
2. Choose **"M0 FREE"** tier (512MB storage - perfect for development)
3. Select a cloud provider and region closest to you
4. Click **"Create"**

### 3. Create Database User
1. Click **"Database Access"** in left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Set credentials:
   - Username: `demo`
   - Password: `test123` (or your preferred password)
5. Set **"Built-in Role"** to **"Read and write to any database"**
6. Click **"Add User"**

### 4. Whitelist Your IP Address
1. Click **"Network Access"** in left sidebar
2. Click **"Add IP Address"**
3. Choose **"Allow Access from Anywhere"** (0.0.0.0/0) for development
   - ⚠️ For production, add only your specific IP addresses
4. Click **"Confirm"**

### 5. Get Your Connection String
1. Go back to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Select **"Python"** and version **"3.12 or later"**
5. Copy the connection string - it looks like:
   ```
   mongodb+srv://demo:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password (e.g., `test123`)

### 6. Update Your `.env` File

Replace the connection string in your `.env`:

```env
# Option 3: MongoDB Atlas (Cloud) - ACTIVE
MONGO_URI=mongodb+srv://demo:test123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

# Option 2: Local MongoDB with authentication
# MONGO_URI=mongodb://demo:test@localhost:27017/

# Option 1: Local MongoDB without authentication
# MONGO_URI=mongodb://localhost:27017/

DATABASE_NAME=contribution_tracking_db
```

⚠️ **Important**: Replace the entire connection string with YOUR actual Atlas connection string!

## Example Connection Strings

### With specific database name:
```
mongodb+srv://demo:test123@cluster0.abc123.mongodb.net/contribution_tracking_db?retryWrites=true&w=majority
```

### Without specific database (recommended):
```
mongodb+srv://demo:test123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

## Troubleshooting

### Connection Failed?
1. **Check IP whitelist**: Ensure 0.0.0.0/0 is allowed in Network Access
2. **Verify credentials**: Username and password must match exactly
3. **Password special characters**: If password has special characters, URL-encode them:
   - `@` → `%40`
   - `#` → `%23`
   - `!` → `%21`

### Can't see your cluster?
- Wait 1-2 minutes for cluster to finish deploying (shows green dot when ready)

### Database not created?
- MongoDB Atlas creates the database automatically on first write
- Just make sure `DATABASE_NAME=contribution_tracking_db` is set in `.env`

## Verify Connection

Once configured, your backend will automatically:
1. Connect to MongoDB Atlas on startup
2. Create the database on first write
3. Store all data in the cloud

Check backend logs for successful connection:
```
INFO:     Application startup complete.
```

## Benefits of MongoDB Atlas

✅ **No local MongoDB needed** - Everything in the cloud
✅ **Automatic backups** - Free tier includes backups
✅ **Monitoring & alerts** - Real-time performance metrics
✅ **Global access** - Access from anywhere
✅ **Free 512MB storage** - Enough for thousands of records

## Next Steps

After updating `.env`:
1. Backend will auto-reload
2. Database will be created on first API call
3. Run `init_db_enhanced.py` to populate demo data (if needed)
