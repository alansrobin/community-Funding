import { useState, useEffect } from 'react'
import axios from 'axios'

function HighRiskMembers({ apiBaseUrl, refreshKey }) {
    const [highRiskMembers, setHighRiskMembers] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchHighRiskMembers()
    }, [refreshKey])

    const fetchHighRiskMembers = async () => {
        try {
            setLoading(true)
            setError(null)
            const response = await axios.get(`${apiBaseUrl}/dashboard/high-risk`)
            setHighRiskMembers(response.data)
        } catch (err) {
            setError('Failed to load high-risk members')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading high-risk members...</p>
            </div>
        )
    }

    if (error) {
        return <div className="error-message">{error}</div>
    }

    return (
        <div className="high-risk">
            <div className="high-risk-header">
                <div>
                    <h2>High-Risk Members (Private View)</h2>
                    <p className="subtitle">Members requiring attention - For admin use only</p>
                </div>
                <div className="high-risk-count">
                    <span className="count-badge">{highRiskMembers.length}</span>
                    <span className="count-label">High-Risk Members</span>
                </div>
            </div>

            {highRiskMembers.length === 0 ? (
                <div className="no-high-risk">
                    <div className="success-state">
                        <span className="success-icon">✅</span>
                        <h3>Great News!</h3>
                        <p>No high-risk members at this time. All members are up to date or have minimal delays.</p>
                    </div>
                </div>
            ) : (
                <>
                    <div className="alert-box warning">
                        <strong>⚠️ Confidential Information:</strong> This data is private and should be handled with care.
                        Use ethically and respectfully when contacting members.
                    </div>

                    <div className="high-risk-grid">
                        {highRiskMembers.map(member => (
                            <div key={member.member_id} className="high-risk-card">
                                <div className="card-header">
                                    <div>
                                        <h3>{member.name}</h3>
                                        <p className="member-id">{member.member_id}</p>
                                    </div>
                                    <span className="risk-badge">High Risk</span>
                                </div>

                                <div className="card-body">
                                    <div className="contact-info">
                                        <div className="contact-item">
                                            <span className="icon">📞</span>
                                            <span>{member.phone}</span>
                                        </div>
                                    </div>

                                    <div className="risk-stats">
                                        <div className="risk-stat">
                                            <span className="stat-icon">❌</span>
                                            <div>
                                                <span className="stat-value">{member.missed_payments}</span>
                                                <span className="stat-label">Missed Payments</span>
                                            </div>
                                        </div>

                                        <div className="risk-stat">
                                            <span className="stat-icon">⏱️</span>
                                            <div>
                                                <span className="stat-value">{member.current_delay_days}</span>
                                                <span className="stat-label">Days Delayed</span>
                                            </div>
                                        </div>

                                        <div className="risk-stat">
                                            <span className="stat-icon">💰</span>
                                            <div>
                                                <span className="stat-value">₹{member.total_pending}</span>
                                                <span className="stat-label">Total Pending</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="card-footer">
                                    <small>💡 Consider reaching out with a supportive, non-punitive message</small>
                                </div>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    )
}

export default HighRiskMembers
