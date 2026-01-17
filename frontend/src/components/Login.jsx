import { useState } from 'react'
import axios from 'axios'
import '../App.css'

function Login({ onLoginSuccess }) {
    const [isLogin, setIsLogin] = useState(true)
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        name: '',
        phone: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

    const handleChange = (e) => {
        let { name, value } = e.target

        if (name === 'phone') {
            value = value.replace(/\D/g, '').slice(0, 10)
        }

        setFormData({
            ...formData,
            [name]: value
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            const endpoint = isLogin ? '/auth/login' : '/auth/register'
            const payload = isLogin
                ? { email: formData.email, password: formData.password }
                : formData

            const response = await axios.post(`${API_BASE_URL}${endpoint}`, payload)

            // Store token
            localStorage.setItem('token', response.data.access_token)

            // Get user profile
            const profileResponse = await axios.get(`${API_BASE_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${response.data.access_token}` }
            })

            // Pass user data and must_change_password flag to parent
            onLoginSuccess({
                ...profileResponse.data,
                must_change_password: response.data.must_change_password || false
            })
        } catch (err) {
            setError(err.response?.data?.detail || 'Authentication failed')
        } finally {
            setLoading(false)
        }
    }

    const fillDemoCredentials = (role) => {
        if (role === 'admin') {
            setFormData({ ...formData, email: 'admin@contribution.com', password: 'admin123' })
        } else {
            setFormData({ ...formData, email: 'arun.kumar@email.com', password: 'password123' })
        }
    }

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h1>Community Funding</h1>
                    <p>Smart Payment Management System</p>
                </div>

                <div className="login-tabs">
                    <button
                        className={isLogin ? 'active' : ''}
                        onClick={() => setIsLogin(true)}
                    >
                        Login
                    </button>
                    <button
                        className={!isLogin ? 'active' : ''}
                        onClick={() => setIsLogin(false)}
                    >
                        Register
                    </button>
                </div>

                {error && <div className="error-message">{error}</div>}


                <form onSubmit={handleSubmit} className="login-form">
                    {!isLogin && (
                        <>
                            <input
                                type="text"
                                name="name"
                                placeholder="Full Name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />
                            <input
                                type="tel"
                                name="phone"
                                placeholder="Phone Number (10 digits)"
                                value={formData.phone}
                                onChange={handleChange}
                                required
                            />
                        </>
                    )}

                    <input
                        type="email"
                        name="email"
                        placeholder="Email Address"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />

                    <button type="submit" className="login-btn" disabled={loading}>
                        {loading ? 'Processing...' : (isLogin ? 'Login' : 'Register')}
                    </button>
                </form>

                {isLogin && (
                    <div className="demo-credentials">
                        <p>🔐 Demo Credentials:</p>
                        <button onClick={() => fillDemoCredentials('admin')} className="demo-btn">
                            Admin Login
                        </button>
                        <button onClick={() => fillDemoCredentials('member')} className="demo-btn">
                            Member Login
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Login
