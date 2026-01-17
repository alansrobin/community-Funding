# Frontend - Ethical Fund Collection System

**The member-facing portal for the Behavior-Aware and Ethical Automated Fund Collection System.**

A modern React-based web application designed to foster trust and transparency. It provides members with personal dashboards to view their impact, while giving administrators ethical, AI-driven tools to manage community funds without coercion.

## 🚀 Features

- **User Authentication**
  - Secure login system with JWT tokens
  - Persistent authentication state
  - Auto-logout on token expiration

- **Role-Based Access**
  - **Member Portal**: Personal dashboard with contribution history
  - **Admin Dashboard**: Full management interface with analytics

- **Member View**
  - Personal contribution overview
  - Payment history and status
  - Notification history
  - Preference management

- **Admin View**
  - Dashboard with statistics and insights
  - Predictive analytics for payment delays
  - Member registration and management
  - Payment tracking and recording
  - Automated reminder system
  - High-risk member identification

- **Modern UI/UX**
  - Clean, intuitive interface
  - Responsive design
  - Real-time data updates
  - Visual statistics and charts

## 📋 Prerequisites

- Node.js 16.x or higher
- npm or yarn package manager
- Backend API running (see backend README)

## 🛠️ Installation

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure API endpoint**
   
   Update the `API_BASE_URL` in `src/App.jsx`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000'
   ```
   
   > Change this to your backend server URL if different

## 🚀 Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🔐 Login Credentials

Use the demo accounts created by the backend initialization:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Member Account:**
- Username: `member1`
- Password: `member123`

## 📁 Project Structure

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── components/           # React components
│   │   ├── Login.jsx        # Login page
│   │   ├── Dashboard.jsx    # Admin dashboard
│   │   ├── MemberDashboard.jsx         # Member personal view
│   │   ├── MemberRegistration.jsx      # Member registration form
│   │   ├── PaymentTracking.jsx         # Payment management
│   │   ├── ReminderSystem.jsx          # Reminder interface
│   │   ├── HighRiskMembers.jsx         # High-risk member list
│   │   └── PredictiveAnalytics.jsx     # Analytics dashboard
│   ├── App.jsx              # Main application component
│   ├── App.css              # Styles
│   ├── main.jsx             # Application entry point
│   └── index.css            # Global styles
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration
└── README.md                # This file
```

## 🎨 Components Overview

### Login.jsx
- Handles user authentication
- Form validation
- Token storage
- Error handling

### MemberDashboard.jsx
- Personal contribution overview
- Payment status visualization
- Notification center
- User preferences

### Dashboard.jsx (Admin)
- System-wide statistics
- Recent contributions overview
- Quick actions panel
- Member summary

### PredictiveAnalytics.jsx (Admin)
- AI-powered delay predictions
- Member risk classification
- Payment trend analysis
- Insights and recommendations

### MemberRegistration.jsx (Admin)
- New member registration form
- Form validation
- Role assignment
- Preference setup

### PaymentTracking.jsx (Admin)
- All members payment status
- Payment recording
- Status updates
- Payment history

### ReminderSystem.jsx (Admin)
- Manual reminder triggers
- Notification history
- Batch reminder sending
- Template customization

### HighRiskMembers.jsx (Admin)
- Identifies at-risk members
- Payment pattern analysis
- Quick action buttons
- Priority alerts

## 🔑 Key Features by Role

### Member Portal Features
- ✅ View personal contribution history
- ✅ Check payment status
- ✅ See upcoming payments
- ✅ View notification history
- ✅ Update preferences

### Admin Portal Features
- ✅ Dashboard with comprehensive statistics
- ✅ Predictive analytics and insights
- ✅ Member registration and management
- ✅ Payment tracking and recording
- ✅ Automated and manual reminder system
- ✅ High-risk member identification
- ✅ Batch operations
- ✅ Historical data analysis

## 🎯 User Workflows

### Member Login Flow
1. Login with credentials
2. Auto-redirect to personal dashboard
3. View contributions and payments
4. Check notifications
5. Update preferences (optional)

### Admin Login Flow
1. Login with admin credentials
2. Access full admin dashboard
3. Navigate tabs for different functions:
   - 📊 Dashboard - Overview and stats
   - 🔮 Predictions - AI-powered insights
   - 👥 Registration - Add new members
   - 💳 Payments - Track and record
   - 📧 Reminders - Send notifications
   - ⚠️ High-Risk - Identify issues

## 🛠️ Configuration

### API Connection
Edit `API_BASE_URL` in `src/App.jsx` to point to your backend:
```javascript
const API_BASE_URL = 'http://your-backend-url:8000'
```

### Authentication
The app uses JWT tokens stored in `localStorage`:
- Token key: `'token'`
- Auto-verification on app load
- Auto-logout on invalid token

## 🎨 Styling

The application uses vanilla CSS with:
- Custom properties for theming
- Responsive design patterns
- Modern UI components
- Smooth animations and transitions

Main style file: `src/App.css`

## 📱 Responsive Design

The application is responsive and works on:
- 💻 Desktop (1920x1080 and above)
- 💼 Laptop (1366x768)
- 📱 Tablet (768x1024)
- 📱 Mobile (375x667 and above)

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Adding New Components

1. Create component in `src/components/`
2. Import in `App.jsx`
3. Add to appropriate view (admin/member)
4. Update navigation if needed

### State Management

The app uses React hooks for state management:
- `useState` - Component state
- `useEffect` - Side effects and API calls
- Props drilling for component communication

## 🐛 Troubleshooting

### Login Issues
- Check backend is running
- Verify `API_BASE_URL` is correct
- Check browser console for errors
- Clear localStorage: `localStorage.clear()`

### API Connection Errors
- Ensure CORS is configured in backend
- Check network tab in browser DevTools
- Verify backend URL and port
- Check firewall settings

### Build Errors
- Delete `node_modules` and reinstall: `npm install`
- Clear cache: `npm cache clean --force`
- Update Node.js to latest LTS version

### Display Issues
- Hard refresh: `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
- Clear browser cache
- Try different browser

## 📦 Dependencies

### Core
- **React** 19.2.0 - UI framework
- **React-DOM** 19.2.0 - React rendering
- **Axios** 1.13.2 - HTTP client

### Development
- **Vite** 7.2.4 - Build tool and dev server
- **ESLint** 9.39.1 - Code linting
- **@vitejs/plugin-react** 5.1.1 - React support for Vite

## 🚀 Deployment

### Build Production Assets
```bash
npm run build
```

### Deploy Options
1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
   - Upload `dist/` folder
   - Configure redirect rules for SPA

2. **Traditional Server** (Apache, Nginx)
   - Copy `dist/` to web root
   - Configure fallback to `index.html`

3. **Docker**
   - Create Dockerfile with Node.js
   - Build and serve with nginx

### Environment Variables
For production, update:
- API_BASE_URL to production backend URL
- Enable HTTPS
- Configure proper CORS origins

## 🔒 Security Considerations

- Always use HTTPS in production
- Implement rate limiting on backend
- Validate all user inputs
- Sanitize data before display
- Keep dependencies updated
- Use environment variables for sensitive data
- Implement proper CORS policies

## 📝 Code Style

The project follows:
- ESLint configuration
- React best practices
- Functional components with hooks
- Consistent naming conventions

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
npm update
```

### Check for Outdated Packages
```bash
npm outdated
```

### Security Audit
```bash
npm audit
npm audit fix
```

## 📄 License

This project is proprietary software for church management.

## 👥 Support

For issues or questions, contact the development team.

## 🎓 Learning Resources

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Axios Documentation](https://axios-http.com/docs/intro)

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Built with**: React + Vite
