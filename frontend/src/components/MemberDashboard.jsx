import { useState, useEffect } from 'react'
import axios from 'axios'

function MemberDashboard({ user, token }) {
    const [dashboardData, setDashboardData] = useState(null)
    const [contributions, setContributions] = useState([])
    const [impactStats, setImpactStats] = useState(null)
    const [notifications, setNotifications] = useState([])
    const [loading, setLoading] = useState(true)
    const [showPayModal, setShowPayModal] = useState(false)

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = async () => {
        try {
            setLoading(true)
            const headers = { 'Authorization': `Bearer ${token}` }

            const [dashboardRes, contributionsRes, impactRes, notificationsRes] = await Promise.all([
                axios.get('http://localhost:8000/member/dashboard', { headers }),
                axios.get('http://localhost:8000/member/contributions', { headers }),
                axios.get('http://localhost:8000/member/impact/stats', { headers }),
                axios.get('http://localhost:8000/member/notifications', { headers })
            ])

            setDashboardData(dashboardRes.data)
            setContributions(contributionsRes.data)
            setImpactStats(impactRes.data)
            setNotifications(notificationsRes.data)
        } catch (err) {
            console.error('Failed to load member data', err)
        } finally {
            setLoading(false)
        }
    }

    const handlePayNow = async () => {
        try {
            const headers = { 'Authorization': `Bearer ${token}` }
            const response = await axios.post('http://localhost:8000/contributions/pay-all', {}, { headers })

            // Show success message
            alert(response.data.message || 'Successfully paid!')

            // Close modal and refresh data
            setShowPayModal(false)
            await fetchData()
        } catch (err) {
            console.error('Payment failed:', err)
            alert('Failed to process payment. Please try again.')
        }
    }

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading your dashboard...</p>
            </div>
        )
    }

    if (!dashboardData) return null

    const getStatusColor = (status) => {
        switch (status) {
            case 'Paid': return 'success'
            case 'Pending': return 'info'
            case 'Unpaid': return 'warning'
            case 'Delayed': return 'danger'
            default: return 'default'
        }
    }

    const getClassificationColor = (classification) => {
        switch (classification) {
            case 'Regular': return 'success'
            case 'Occasional Delay': return 'warning'
            case 'High-risk Delay': return 'danger'
            default: return 'default'
        }
    }

    return (
        <div className="member-dashboard">
            {/* 1. Email-like Header */}
            <div className="welcome-card-enhanced">
                <div className="welcome-content">
                    <h2>Hello, {dashboardData.member_info.name}! 👋</h2>
                    <p>Member ID: {dashboardData.member_info.member_id}</p>
                    <div className="welcome-badges">
                        <span className="badge-pill">
                            {dashboardData.statistics.classification === 'Regular' ? '🌟 Super Supporter' : 'Member'}
                        </span>
                        {dashboardData.statistics.missed_count === 0 && (
                            <span className="badge-pill">🔥 {contributions.length}-Month Streak</span>
                        )}
                    </div>
                </div>
            </div>

            {/* Notification Banner */}
            {notifications.length > 0 && (
                <div className="notification-banner">
                    <div className="notification-icon">🔔</div>
                    <div className="notification-content">
                        <h4 className="notification-title">New Message from Admin</h4>
                        <p className="notification-message">{notifications[0].message}</p>
                        <span className="notification-time">
                            {new Date(notifications[0].sent_at).toLocaleDateString()}
                        </span>
                    </div>
                </div>
            )}

            {/* 2. Main Stats Grid */}
            <div className="stats-grid">
                <div className="stat-card primary">
                    <div className="stat-icon">📊</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Total Contributions</h3>
                        <p className="stat-value">{dashboardData.statistics.total_contributions}</p>
                    </div>
                </div>

                <div className="stat-card money">
                    <div className="stat-icon">💰</div>
                    <div className="stat-content">
                        <h3 className="stat-label">Pending Amount</h3>
                        <p className="stat-value">₹{dashboardData.total_pending}</p>
                        {dashboardData.total_pending > 0 ? (
                            <button className="pay-now-btn" onClick={() => setShowPayModal(true)}>
                                Pay Now 💳
                            </button>
                        ) : (
                            <button className="already-paid-btn" disabled>
                                Already Paid ✅
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* 3. Current Funding Program Chart */}
            {impactStats && (
                <div className="funding-section-enhanced">
                    <h3>🚀 Current Community Goal: {impactStats.active_initiatives[0]?.name || "General Fund"}</h3>
                    <p className="funding-subtitle">Your contributions are directly analyzing this goal</p>

                    <div className="funding-chart-container">
                        <div className="funding-info">
                            <span>Raised: ₹{impactStats.total_raised.toLocaleString()}</span>
                            <span>Goal: ₹{impactStats.monthly_goal.toLocaleString()}</span>
                        </div>
                        <div className="progress-bg-large">
                            <div
                                className="progress-fill-large"
                                style={{
                                    width: `${impactStats.progress_percentage}%`,
                                    background: 'linear-gradient(90deg, #6366f1, #a855f7)'
                                }}
                            >
                                <span className="progress-text">{impactStats.progress_percentage}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* 4. Upcoming Dues */}
            {dashboardData.upcoming_dues.length > 0 && (
                <div className="upcoming-section">
                    <h3>📅 Upcoming Dues</h3>
                    <div className="upcoming-grid">
                        {dashboardData.upcoming_dues.map(due => (
                            <div key={due.contribution_id} className={`upcoming-card ${due.status === 'overdue' ? 'overdue' : ''}`}>
                                <div className="upcoming-header">
                                    <span className="upcoming-status">
                                        {due.status === 'overdue' ? '🔴 Overdue' : '⏰ Due Soon'}
                                    </span>
                                    <span className="upcoming-amount">₹{due.amount}</span>
                                </div>
                                <div className="upcoming-details">
                                    <p><strong>Due Date:</strong> {due.due_date}</p>
                                    <p><strong>Days:</strong> {Math.abs(due.days_until)} days {due.status === 'overdue' ? 'overdue' : 'remaining'}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* 5. Pay Now Modal */}
            {showPayModal && (
                <div className="modal-overlay" onClick={() => setShowPayModal(false)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Scan to Pay</h3>
                            <button className="close-btn" onClick={() => setShowPayModal(false)}>×</button>
                        </div>
                        <div className="qr-container">
                            <img
                                src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=church@upi&pn=CommunityFund&am={dashboardData.total_pending}"
                                alt="Payment QR"
                                className="qr-code"
                            />
                            <p>Scan with any UPI App</p>
                            <div className="amount-display">
                                Paying: ₹{dashboardData.total_pending}
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button className="secondary-btn" onClick={() => setShowPayModal(false)}>Close</button>
                            <button className="primary-btn" onClick={handlePayNow}>
                                pay now
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Styles for new elements */}
            <style>{`
                .welcome-card-enhanced {
                    background: linear-gradient(135deg, #6366f1, #4f46e5);
                    padding: 2.5rem;
                    border-radius: 1rem;
                    color: white;
                    margin-bottom: 2rem;
                    box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
                    position: relative;
                    overflow: hidden;
                }
                .welcome-card-enhanced::after {
                    content: '';
                    position: absolute;
                    top: -50%;
                    right: -20%;
                    width: 300px;
                    height: 300px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 50%;
                }
                .welcome-content h2 { margin: 0; font-size: 2rem; }
                .welcome-badges { display: flex; gap: 10px; margin-top: 15px; }
                .badge-pill { background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; backdrop-filter: blur(5px); }
                
                .pay-now-btn {
                    margin-top: 10px;
                    background: white;
                    color: #8b5cf6;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.2s;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                .pay-now-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 10px rgba(0,0,0,0.15); }

                .already-paid-btn {
                    margin-top: 10px;
                    padding: 8px 16px;
                    background: linear-gradient(135deg, #6b7280, #4b5563);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 700;
                    cursor: not-allowed;
                    opacity: 0.7;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }

                .funding-section-enhanced {
                    background: var(--bg-card);
                    padding: 2rem;
                    border-radius: 1rem;
                    margin-bottom: 2rem;
                    border: 1px solid var(--border);
                }
                .funding-chart-container { margin-top: 1.5rem; }
                .funding-info { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: 600; }
                .progress-bg-large { height: 24px; background: var(--bg-secondary); border-radius: 12px; overflow: hidden; }
                .progress-fill-large { height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.8rem; font-weight: bold; transition: width 1s ease-out; }

                /* Modal */
                .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(5px); }
                .modal-content { background: var(--bg-card); padding: 2rem; border-radius: 1rem; width: 90%; max-width: 400px; animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1); border: 1px solid var(--border); }
                .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
                .close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary); }
                .qr-container { text-align: center; margin-bottom: 1.5rem; }
                .qr-code { border-radius: 10px; border: 5px solid white; margin-bottom: 1rem; }
                .amount-display { font-size: 1.5rem; font-weight: 800; color: var(--primary); margin-top: 10px; }
                .modal-footer { display: flex; gap: 10px; justify-content: flex-end; }
                .primary-btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; }
                .secondary-btn { background: transparent; color: var(--text-secondary); border: 1px solid var(--border); padding: 10px 20px; border-radius: 8px; cursor: pointer; }

                @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            `}</style>
        </div>
    )
}

export default MemberDashboard
