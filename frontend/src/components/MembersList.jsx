import { useState, useEffect } from 'react'
import axios from 'axios'

function MembersList({ apiBaseUrl }) {
    const [members, setMembers] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [searchTerm, setSearchTerm] = useState('')
    const [statusFilter, setStatusFilter] = useState('all')  // 'all', 'Regular', 'Occasional Delay', 'High-risk Delay'

    useEffect(() => {
        fetchMembers()
    }, [])

    const fetchMembers = async () => {
        try {
            setLoading(true)
            const token = localStorage.getItem('token')
            const response = await axios.get(`${apiBaseUrl}/admin/members`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            setMembers(response.data)
        } catch (err) {
            console.error('Failed to fetch members', err)
            setError('Failed to load members list')
        } finally {
            setLoading(false)
        }
    }

    const filteredMembers = members.filter(member => {
        // Apply search filter
        const searchLower = searchTerm.toLowerCase()
        const matchesSearch = (
            member.name.toLowerCase().includes(searchLower) ||
            member.member_id.toLowerCase().includes(searchLower) ||
            (member.email && member.email.toLowerCase().includes(searchLower)) ||
            (member.phone && member.phone.includes(searchLower))
        )

        // Apply classification filter
        const matchesStatus = statusFilter === 'all' || member.classification === statusFilter

        return matchesSearch && matchesStatus
    })

    const getStatusColor = (classification) => {
        switch (classification) {
            case 'Regular': return 'success'
            case 'Occasional Delay': return 'warning'
            case 'High-risk Delay': return 'danger'
            default: return 'default'
        }
    }

    const getStatusCounts = () => {
        return {
            all: members.length,
            regular: members.filter(m => m.classification === 'Regular').length,
            occasional_delay: members.filter(m => m.classification === 'Occasional Delay').length,
            high_risk: members.filter(m => m.classification === 'High-risk Delay').length
        }
    }

    const statusCounts = getStatusCounts()

    if (loading) return <div className="loading-container"><div className="spinner"></div><p>Loading members...</p></div>
    if (error) return <div className="error-message">{error}</div>

    return (
        <div className="members-list-view">
            <div className="dashboard-header">
                <h2>Members List</h2>
                <div className="header-actions">
                    <div className="search-box">
                        <input
                            type="text"
                            placeholder="🔍 Search members..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <button className="refresh-btn" onClick={fetchMembers}>
                        🔄 Refresh
                    </button>
                </div>
            </div>

            <div className="status-filter-tabs">
                <button
                    className={`filter-tab ${statusFilter === 'all' ? 'active' : ''}`}
                    onClick={() => setStatusFilter('all')}
                >
                    All ({statusCounts.all})
                </button>
                <button
                    className={`filter-tab success ${statusFilter === 'Regular' ? 'active' : ''}`}
                    onClick={() => setStatusFilter('Regular')}
                >
                    ✅ Regular ({statusCounts.regular})
                </button>
                <button
                    className={`filter-tab warning ${statusFilter === 'Occasional Delay' ? 'active' : ''}`}
                    onClick={() => setStatusFilter('Occasional Delay')}
                >
                    ⚠️ Occasional Delay ({statusCounts.occasional_delay})
                </button>
                <button
                    className={`filter-tab danger ${statusFilter === 'High-risk Delay' ? 'active' : ''}`}
                    onClick={() => setStatusFilter('High-risk Delay')}
                >
                    🚨 High Risk ({statusCounts.high_risk})
                </button>
            </div>

            <div className="table-container">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Contact</th>
                            <th>Employee ID</th>
                            <th>Monthly Amount</th>
                            <th>Health</th>
                            <th>Priority</th>
                            <th>Contributions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredMembers.map(member => (
                            <tr key={member.member_id}>
                                <td><span className="id-badge">{member.member_id}</span></td>
                                <td>
                                    <div className="member-name-cell">
                                        <strong>{member.name}</strong>
                                    </div>
                                </td>
                                <td>
                                    <div className="contact-cell">
                                        <span>📞 {member.phone}</span>
                                        {member.email && <span>📧 {member.email}</span>}
                                    </div>
                                </td>
                                <td>{member.employee_id || 'N/A'}</td>
                                <td>₹{member.monthly_amount}</td>
                                <td>
                                    <span className={`status-badge ${getStatusColor(member.classification)}`}>
                                        {member.classification}
                                    </span>
                                </td>
                                <td>
                                    <span className={`priority-badge ${member.priority === 'Early Reminder' ? 'warning' : 'success'}`}>
                                        {member.priority === 'Early Reminder' ? '⚡ Early Reminder' : '✓ Normal'}
                                    </span>
                                </td>
                                <td>
                                    {member.paid_count}/{member.total_contributions}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="list-footer">
                <p>Showing {filteredMembers.length} of {members.length} members</p>
            </div>
        </div>
    )
}

export default MembersList
