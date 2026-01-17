import { useState, useEffect } from 'react'
import axios from 'axios'

function Dashboard({ apiBaseUrl, refreshKey }) {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [generating, setGenerating] = useState(false)
    const [generationMessage, setGenerationMessage] = useState(null)

    useEffect(() => {
        fetchStats()
    }, [refreshKey])

    const fetchStats = async () => {
        try {
            setLoading(true)
            setError(null)
            const response = await axios.get(`${apiBaseUrl}/admin/dashboard/stats`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            })
            setStats(response.data)
        } catch (err) {
            setError('Failed to load dashboard statistics')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }


    const generateMonthlyContributions = async () => {
        try {
            setGenerating(true)
            setGenerationMessage(null)
            const response = await axios.post(
                `${apiBaseUrl}/admin/contributions/generate`,
                {},
                { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
            )

            if (response.data.status === 'success') {
                setGenerationMessage({
                    type: 'success',
                    text: `✅ ${response.data.message}. Created ${response.data.contributions_created} contributions. 📧 Emails sent: ${response.data.emails_sent}, Skipped: ${response.data.emails_skipped}, Errors: ${response.data.email_errors}`
                })
                // Refresh stats after generating
                setTimeout(() => fetchStats(), 1000)
            } else if (response.data.status === 'already_exists') {
                setGenerationMessage({
                    type: 'info',
                    text: `ℹ️ ${response.data.message}`
                })
            }

            // Hide message after 5 seconds
            setTimeout(() => setGenerationMessage(null), 5000)
        } catch (err) {
            setGenerationMessage({
                type: 'error',
                text: `❌ Failed to generate contributions: ${err.response?.data?.detail || err.message}`
            })
            setTimeout(() => setGenerationMessage(null), 5000)
        } finally {
            setGenerating(false)
        }
    }


    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading dashboard...</p>
            </div>
        )
    }

    if (error) {
        return <div className="error-message">{error}</div>
    }

    if (!stats) return null

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h2>Admin Dashboard</h2>
                <div className="header-actions">
                    <button
                        className="generate-btn"
                        onClick={generateMonthlyContributions}
                        disabled={generating}
                    >
                        {generating ? '⏳ Generating...' : '📅 Generate Monthly Contributions'}
                    </button>
                    <button className="refresh-btn" onClick={fetchStats}>
                        🔄 Refresh
                    </button>
                </div>
            </div>

            {generationMessage && (
                <div className={`notification-message ${generationMessage.type}`}>
                    {generationMessage.text}
                </div>
            )}

            <div className="stats-grid">
                <div className="stat-card primary">
                    <div className="stat-icon">👥</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Total Members</h3>
                        <p className="stat-value">{stats.total_members}</p>
                    </div>
                </div>

                <div className="stat-card success">
                    <div className="stat-icon">✅</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Paid Contributions</h3>
                        <p className="stat-value">{stats.paid_contributions}</p>
                    </div>
                </div>

                <div className="stat-card warning">
                    <div className="stat-icon">⏳</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Unpaid Contributions</h3>
                        <p className="stat-value">{stats.unpaid_contributions}</p>
                    </div>
                </div>

                <div className="stat-card danger">
                    <div className="stat-icon">⚠️</div>
                    <div className="stat-content">
                        <h3 className="stat-label">High-Risk Members</h3>
                        <p className="stat-value">{stats.high_risk_members}</p>
                    </div>
                </div>

                <div className="stat-card money">
                    <div className="stat-icon">💰</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Total Collected</h3>
                        <p className="stat-value">₹{stats.total_collected}</p>
                    </div>
                </div>

                <div className="stat-card pending">
                    <div className="stat-icon">💳</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Total Pending</h3>
                        <p className="stat-value">₹{stats.total_pending}</p>
                    </div>
                </div>
            </div>

            <div className="monthly-summary">
                <h3>Current Month Summary ({stats.current_month.month})</h3>
                <div className="monthly-grid">
                    <div className="monthly-stat">
                        <span className="monthly-label">Total Contributions:</span>
                        <span className="monthly-value">{stats.current_month.total_contributions}</span>
                    </div>
                    <div className="monthly-stat">
                        <span className="monthly-label">Paid Contributions:</span>
                        <span className="monthly-value success">{stats.current_month.paid_contributions}</span>
                    </div>
                    <div className="monthly-stat">
                        <span className="monthly-label">Amount Collected:</span>
                        <span className="monthly-value money">₹{stats.current_month.collected_amount}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard
