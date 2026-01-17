import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// Components
import Login from './components/Login'
import MemberDashboard from './components/MemberDashboard'
import Dashboard from './components/Dashboard'
import MemberRegistration from './components/MemberRegistration'
import PaymentTracking from './components/PaymentTracking'
import ReminderSystem from './components/ReminderSystem'
import HighRiskMembers from './components/HighRiskMembers'
import PredictiveAnalytics from './components/PredictiveAnalytics'
import ImpactDashboard from './components/ImpactDashboard'
import MembersList from './components/MembersList'
import ChangePasswordModal from './components/ChangePasswordModal'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    // Check for existing token
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      verifyToken(storedToken)
    }
  }, [])

  const verifyToken = async (storedToken) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: { 'Authorization': `Bearer ${storedToken}` }
      })
      setUser(response.data)
      setToken(storedToken)
    } catch (err) {
      localStorage.removeItem('token')
    }
  }

  const handleLoginSuccess = (userData) => {
    setUser(userData)
    setToken(localStorage.getItem('token'))
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setUser(null)
    setToken(null)
    setActiveTab('dashboard')
  }

  const refresh = () => {
    setRefreshKey(prev => prev + 1)
  }

  const handlePasswordChanged = async () => {
    // Refresh user data to clear must_change_password flag
    const storedToken = localStorage.getItem('token')
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: { 'Authorization': `Bearer ${storedToken}` }
    })
    setUser(response.data)
  }

  // If not logged in, show login
  if (!user || !token) {
    return <Login onLoginSuccess={handleLoginSuccess} />
  }

  // If password change required, show password change modal
  if (user.must_change_password) {
    return <ChangePasswordModal onPasswordChanged={handlePasswordChanged} />
  }

  // Member view - with navigation
  if (user.role === 'member') {
    return (
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1 className="app-title">
              Community Funding
            </h1>
            <div className="header-actions">
              <span className="user-info">👤 {user.name}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </div>
        </header>

        <nav className="navigation">
          <button
            className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            <span className="nav-icon">🏠</span>
            Dashboard
          </button>
          <button
            className={`nav-button ${activeTab === 'impact' ? 'active' : ''}`}
            onClick={() => setActiveTab('impact')}
          >
            <span className="nav-icon">🌍</span>
            Community Impact
          </button>
        </nav>

        <main className="main-content">
          {activeTab === 'dashboard' && <MemberDashboard user={user} token={token} />}
          {activeTab === 'impact' && <ImpactDashboard apiBaseUrl={API_BASE_URL} />}
        </main>

        <footer className="app-footer">
          <p>© 2026 Community Funding • Member Portal</p>
        </footer>
      </div>
    )
  }

  // Admin view - full dashboard
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            Admin Dashboard
          </h1>
          <div className="header-actions">
            <span className="user-info">👤 {user.name} (Admin)</span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      </header>

      <nav className="navigation">
        <button
          className={`nav-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <span className="nav-icon">📊</span>
          Dashboard
        </button>
        <button
          className={`nav-button ${activeTab === 'predictions' ? 'active' : ''}`}
          onClick={() => setActiveTab('predictions')}
        >
          <span className="nav-icon">🔮</span>
          Predictions
        </button>
        <button
          className={`nav-button ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          <span className="nav-icon">👤</span>
          Registration
        </button>
        <button
          className={`nav-button ${activeTab === 'members-list' ? 'active' : ''}`}
          onClick={() => setActiveTab('members-list')}
        >
          <span className="nav-icon">👥</span>
          Members
        </button>
        <button
          className={`nav-button ${activeTab === 'payments' ? 'active' : ''}`}
          onClick={() => setActiveTab('payments')}
        >
          <span className="nav-icon">💳</span>
          Payments
        </button>
        <button
          className={`nav-button ${activeTab === 'reminders' ? 'active' : ''}`}
          onClick={() => setActiveTab('reminders')}
        >
          <span className="nav-icon">📧</span>
          Reminders
        </button>
        <button
          className={`nav-button ${activeTab === 'high-risk' ? 'active' : ''}`}
          onClick={() => setActiveTab('high-risk')}
        >
          <span className="nav-icon">⚠️</span>
          High-Risk
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' && <Dashboard apiBaseUrl={API_BASE_URL} refreshKey={refreshKey} />}
        {activeTab === 'predictions' && <PredictiveAnalytics token={token} />}
        {activeTab === 'members' && <MemberRegistration apiBaseUrl={API_BASE_URL} onSuccess={refresh} />}
        {activeTab === 'members-list' && <MembersList apiBaseUrl={API_BASE_URL} />}
        {activeTab === 'payments' && <PaymentTracking apiBaseUrl={API_BASE_URL} refreshKey={refreshKey} onUpdate={refresh} />}
        {activeTab === 'reminders' && <ReminderSystem apiBaseUrl={API_BASE_URL} refreshKey={refreshKey} />}
        {activeTab === 'high-risk' && <HighRiskMembers apiBaseUrl={API_BASE_URL} refreshKey={refreshKey} />}
      </main>

      <footer className="app-footer">
        <p>© 2026 Community Funding • Ethical & Transparent Payment Management</p>
      </footer>
    </div>
  )
}

export default App
