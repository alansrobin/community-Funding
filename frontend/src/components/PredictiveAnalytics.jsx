import { useState, useEffect } from 'react'
import axios from 'axios'

function PredictiveAnalytics({ token }) {
    const [predictions, setPredictions] = useState([])
    const [selectedMember, setSelectedMember] = useState(null)
    const [insights, setInsights] = useState(null)
    const [loading, setLoading] = useState(true)
    const [sendingReminder, setSendingReminder] = useState(false)

    useEffect(() => {
        fetchPredictions()
    }, [])

    const fetchPredictions = async () => {
        try {
            setLoading(true)
            const headers = { 'Authorization': `Bearer ${token}` }
            const response = await axios.get('http://localhost:8000/admin/predictions/', { headers })
            setPredictions(response.data)
        } catch (err) {
            console.error('Failed to load predictions', err)
        } finally {
            setLoading(false)
        }
    }

    const fetchMemberInsights = async (memberId) => {
        try {
            const headers = { 'Authorization': `Bearer ${token}` }
            const response = await axios.get(`http://localhost:8000/admin/predictions/insights/${memberId}`, { headers })
            setInsights(response.data)
            setSelectedMember(memberId)
        } catch (err) {
            console.error('Failed to load insights', err)
        }
    }

    const sendReminder = async (memberId) => {
        try {
            setSendingReminder(true)
            const headers = { 'Authorization': `Bearer ${token}` }
            await axios.post(`http://localhost:8000/admin/send-reminder/${memberId}`, {}, { headers })
            alert('Reminder sent successfully!')
        } catch (err) {
            alert('Failed to send reminder')
        } finally {
            setSendingReminder(false)
        }
    }

    const getRiskColor = (score) => {
        if (score < 30) return 'success'
        if (score < 60) return 'warning'
        return 'danger'
    }

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading predictions...</p>
            </div>
        )
    }

    return (
        <div className="predictive-analytics">
            <h2>🔮 Predictive Analytics & Insights</h2>
            <p className="subtitle">AI-powered delay predictions and member insights</p>

            <div className="predictions-content">
                <div className="predictions-list">
                    <h3>Members at Risk ({predictions.length})</h3>
                    {predictions.length === 0 ? (
                        <div className="no-predictions">
                            <span className="success-icon">✅</span>
                            <p>No members predicted to delay!</p>
                        </div>
                    ) : (
                        <div className="predictions-grid">
                            {predictions.map(pred => (
                                <div
                                    key={pred.member_id}
                                    className={`prediction-card ${selectedMember === pred.member_id ? 'active' : ''}`}
                                    onClick={() => fetchMemberInsights(pred.member_id)}
                                >
                                    <div className="prediction-header">
                                        <strong>{pred.member_name}</strong>
                                        <span className={`risk-score-badge ${getRiskColor(pred.risk_score)}`}>
                                            Risk: {pred.risk_score}
                                        </span>
                                    </div>
                                    <div className="prediction-details">
                                        <div className="detail-item">
                                            <span className="label">Will Delay:</span>
                                            <span className="value">{pred.will_delay ? '⚠️ Yes' : '✅ No'}</span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="label">Estimated Delay:</span>
                                            <span className="value">{pred.estimated_delay_days} days</span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="label">Confidence:</span>
                                            <span className="value">{(pred.confidence * 100).toFixed(0)}%</span>
                                        </div>
                                    </div>
                                    <div className="prediction-factors">
                                        {pred.factors.map((factor, idx) => (
                                            <span key={idx} className="factor-tag">{factor}</span>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div className="insights-panel">
                    {!insights ? (
                        <div className="no-selection">
                            <span className="empty-icon">📊</span>
                            <h3>Select a Member</h3>
                            <p>Click on a member from the list to view detailed insights</p>
                        </div>
                    ) : (
                        <div className="insights-content">
                            <h3>Detailed Insights</h3>

                            <div className="insight-card">
                                <h4>Risk Assessment</h4>
                                <div className="risk-meter">
                                    <div className="risk-score-display">
                                        <span className={`score-large ${getRiskColor(insights.risk_score)}`}>
                                            {insights.risk_score}
                                        </span>
                                        <span className="score-label">/ 100</span>
                                    </div>
                                    <div className={`health-status ${getRiskColor(insights.risk_score)}`}>
                                        {insights.health_status}
                                    </div>
                                </div>
                            </div>

                            <div className="insight-card">
                                <h4>Payment Stats</h4>
                                <div className="stats-row">
                                    <div className="stat">
                                        <span className="stat-number">{insights.total_contributions}</span>
                                        <span className="stat-text">Total</span>
                                    </div>
                                    <div className="stat">
                                        <span className="stat-number">{insights.paid_count}</span>
                                        <span className="stat-text">Paid</span>
                                    </div>
                                    <div className="stat">
                                        <span className="stat-number success">{insights.success_rate}%</span>
                                        <span className="stat-text">Success Rate</span>
                                    </div>
                                </div>
                            </div>

                            <div className="insight-card">
                                <h4>Payment Patterns</h4>
                                <div className="pattern-details">
                                    <div className="pattern-item">
                                        <strong>Pattern:</strong> {insights.payment_patterns.pattern}
                                    </div>
                                    <div className="pattern-item">
                                        <strong>Avg Delay:</strong> {insights.payment_patterns.average_delay} days
                                    </div>
                                    <div className="pattern-item">
                                        <strong>Consistency:</strong> {insights.payment_patterns.consistency}
                                    </div>
                                </div>
                            </div>

                            <div className="insight-card">
                                <h4>Prediction</h4>
                                <div className="prediction-info">
                                    <p><strong>Will Delay:</strong> {insights.prediction.will_delay ? '⚠️ Yes' : '✅ No'}</p>
                                    <p><strong>Estimated Delay:</strong> {insights.prediction.estimated_delay_days} days</p>
                                    <p><strong>Confidence:</strong> {(insights.prediction.confidence * 100).toFixed(0)}%</p>
                                    <div className="factors-list">
                                        <strong>Contributing Factors:</strong>
                                        <ul>
                                            {insights.prediction.factors.map((factor, idx) => (
                                                <li key={idx}>{factor}</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <div className="insight-card recommendation">
                                <h4>💡 Recommendation</h4>
                                <p>{insights.recommendation}</p>
                                <button
                                    className="send-reminder-btn"
                                    onClick={() => sendReminder(selectedMember)}
                                    disabled={sendingReminder}
                                >
                                    {sendingReminder ? 'Sending...' : '📧 Send Reminder Now'}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default PredictiveAnalytics
