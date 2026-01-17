import { useState, useEffect } from 'react'
import axios from 'axios'

function PaymentTracking({ apiBaseUrl, refreshKey, onUpdate }) {
    const [members, setMembers] = useState([])
    const [paymentStatuses, setPaymentStatuses] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [filterClassification, setFilterClassification] = useState('all')
    const [searchTerm, setSearchTerm] = useState('')

    useEffect(() => {
        fetchData()
    }, [refreshKey])

    const fetchData = async () => {
        try {
            setLoading(true)
            setError(null)
            const [membersRes, statusesRes] = await Promise.all([
                axios.get(`${apiBaseUrl}/members`),
                axios.get(`${apiBaseUrl}/contributions/status`)
            ])
            setMembers(membersRes.data)
            setPaymentStatuses(statusesRes.data)
        } catch (err) {
            setError('Failed to load payment data')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handlePayment = async (contributionId, memberId) => {
        const today = new Date().toISOString().split('T')[0]

        try {
            await axios.post(`${apiBaseUrl}/contributions/payment`, {
                member_id: memberId,
                contribution_id: contributionId,
                paid_date: today
            })

            fetchData()
            if (onUpdate) onUpdate()
        } catch (err) {
            alert('Failed to record payment')
            console.error(err)
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

    const getStatusColor = (status) => {
        switch (status) {
            case 'Paid': return 'success'
            case 'Pending': return 'info'
            case 'Unpaid': return 'warning'
            case 'Delayed': return 'danger'
            default: return 'default'
        }
    }

    // Filter members
    const filteredMembers = members.filter(member => {
        const matchesClassification = filterClassification === 'all' || member.classification === filterClassification
        const matchesSearch = member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            member.member_id.toLowerCase().includes(searchTerm.toLowerCase())
        return matchesClassification && matchesSearch
    })

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading payment data...</p>
            </div>
        )
    }

    if (error) {
        return <div className="error-message">{error}</div>
    }

    return (
        <div className="payment-tracking">
            <h2>Payment Tracking</h2>

            <div className="filters-section">
                <div className="search-box">
                    <input
                        type="text"
                        placeholder="🔍 Search by name or ID..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="filter-buttons">
                    <button
                        className={filterClassification === 'all' ? 'active' : ''}
                        onClick={() => setFilterClassification('all')}
                    >
                        All Members
                    </button>
                    <button
                        className={filterClassification === 'Regular' ? 'active success' : ''}
                        onClick={() => setFilterClassification('Regular')}
                    >
                        Regular
                    </button>
                    <button
                        className={filterClassification === 'Occasional Delay' ? 'active warning' : ''}
                        onClick={() => setFilterClassification('Occasional Delay')}
                    >
                        Occasional Delay
                    </button>
                    <button
                        className={filterClassification === 'High-risk Delay' ? 'active danger' : ''}
                        onClick={() => setFilterClassification('High-risk Delay')}
                    >
                        High-risk
                    </button>
                </div>
            </div>

            <div className="members-list">
                {filteredMembers.map(member => {
                    const memberPayments = paymentStatuses.filter(p => p.member_id === member.member_id)

                    return (
                        <div key={member.member_id} className="member-card">
                            <div className="member-header">
                                <div className="member-info">
                                    <h3>{member.name}</h3>
                                    <p className="member-id">{member.member_id}</p>
                                    <p className="member-contact">{member.phone}</p>
                                </div>
                                <div className="member-stats">
                                    <span className={`classification-badge ${getClassificationColor(member.classification)}`}>
                                        {member.classification}
                                    </span>
                                    <div className="stat-item">
                                        <span className="stat-label">Paid:</span>
                                        <span className="stat-value">{member.paid_count}/{member.total_contributions}</span>
                                    </div>
                                    <div className="stat-item">
                                        <span className="stat-label">Missed:</span>
                                        <span className="stat-value danger">{member.missed_count}</span>
                                    </div>
                                    {member.current_delay_days > 0 && (
                                        <div className="stat-item">
                                            <span className="stat-label">Delay:</span>
                                            <span className="stat-value warning">{member.current_delay_days} days</span>
                                        </div>
                                    )}
                                </div>
                            </div>

                            <div className="payments-table">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Due Date</th>
                                            <th>Paid Date</th>
                                            <th>Amount</th>
                                            <th>Status</th>
                                            <th>Delay</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {memberPayments.map(payment => (
                                            <tr key={payment.contribution_id}>
                                                <td>{payment.due_date}</td>
                                                <td>{payment.paid_date || '-'}</td>
                                                <td>₹{payment.amount}</td>
                                                <td>
                                                    <span className={`status-badge ${getStatusColor(payment.status)}`}>
                                                        {payment.status}
                                                    </span>
                                                </td>
                                                <td>
                                                    {payment.delay_days > 0 ? (
                                                        <span className="delay-badge">{payment.delay_days} days</span>
                                                    ) : '-'}
                                                </td>
                                                <td>
                                                    {!payment.paid_date && (
                                                        <button
                                                            className="pay-btn"
                                                            onClick={() => handlePayment(payment.contribution_id, member.member_id)}
                                                        >
                                                            Mark Paid
                                                        </button>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )
                })}
            </div>

            {filteredMembers.length === 0 && (
                <div className="no-results">
                    <p>No members found matching your criteria.</p>
                </div>
            )}
        </div>
    )
}

export default PaymentTracking
