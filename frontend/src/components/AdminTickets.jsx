import { useState, useEffect } from 'react'
import axios from 'axios'

function AdminTickets({ apiBaseUrl, token }) {
    const [tickets, setTickets] = useState([])
    const [filter, setFilter] = useState('all')
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState({ type: '', text: '' })
    const [adminResponse, setAdminResponse] = useState({})

    const fetchTickets = async (statusFilter = null) => {
        try {
            const url = statusFilter
                ? `${apiBaseUrl}/admin/tickets?status_filter=${statusFilter}`
                : `${apiBaseUrl}/admin/tickets`

            const response = await axios.get(url, {
                headers: { Authorization: `Bearer ${token}` }
            })
            setTickets(response.data)
        } catch (err) {
            console.error('Error fetching tickets:', err)
        }
    }

    useEffect(() => {
        fetchTickets(filter === 'all' ? null : filter)
    }, [filter])

    const handleTicketAction = async (ticketId, status) => {
        setLoading(true)
        setMessage({ type: '', text: '' })

        try {
            await axios.patch(
                `${apiBaseUrl}/admin/tickets/${ticketId}?status=${status}`,
                { admin_response: adminResponse[ticketId] || '' },
                { headers: { Authorization: `Bearer ${token}` } }
            )

            setMessage({ type: 'success', text: `Ticket ${status} successfully!` })
            fetchTickets(filter === 'all' ? null : filter)
            setAdminResponse({ ...adminResponse, [ticketId]: '' })
        } catch (err) {
            setMessage({
                type: 'error',
                text: err.response?.data?.detail || 'Failed to update ticket'
            })
        } finally {
            setLoading(false)
        }
    }

    const getStatusColor = (status) => {
        switch (status) {
            case 'pending': return '#ffa500'
            case 'approved': return '#28a745'
            case 'rejected': return '#dc3545'
            default: return '#666'
        }
    }

    return (
        <div className="admin-tickets">
            <div className="header">
                <h2>Manage Tickets</h2>
                <div className="filter-buttons">
                    <button
                        className={filter === 'all' ? 'active' : ''}
                        onClick={() => setFilter('all')}
                    >
                        All
                    </button>
                    <button
                        className={filter === 'pending' ? 'active' : ''}
                        onClick={() => setFilter('pending')}
                    >
                        Pending
                    </button>
                    <button
                        className={filter === 'approved' ? 'active' : ''}
                        onClick={() => setFilter('approved')}
                    >
                        Approved
                    </button>
                    <button
                        className={filter === 'rejected' ? 'active' : ''}
                        onClick={() => setFilter('rejected')}
                    >
                        Rejected
                    </button>
                </div>
            </div>

            {message.text && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            <div className="tickets-container">
                {tickets.length === 0 ? (
                    <p className="no-data">No tickets found.</p>
                ) : (
                    tickets.map((ticket) => (
                        <div key={ticket.ticket_id} className="ticket-card">
                            <div className="ticket-header-info">
                                <div>
                                    <h3>{ticket.member_name}</h3>
                                    <p className="member-details">
                                        <span>Member ID: {ticket.member_id}</span>
                                        <span className="employee-badge">EMP: {ticket.employee_id}</span>
                                    </p>
                                </div>
                                <span
                                    className="status-badge"
                                    style={{ backgroundColor: getStatusColor(ticket.status) }}
                                >
                                    {ticket.status.toUpperCase()}
                                </span>
                            </div>

                            <div className="ticket-content">
                                <div className="request-details">
                                    <p><strong>Request Type:</strong> {ticket.request_type === 'monthly_amount' ? 'Monthly Amount Change' : 'Due Day Change'}</p>
                                    <p><strong>Current Value:</strong> {ticket.current_value}</p>
                                    <p><strong>Requested Value:</strong> <span className="highlight">{ticket.new_value}</span></p>
                                    <p><strong>Reason:</strong> {ticket.reason}</p>
                                    <p className="date"><small>Submitted: {new Date(ticket.created_at).toLocaleString()}</small></p>
                                </div>

                                {ticket.status === 'pending' && (
                                    <div className="action-section">
                                        <textarea
                                            placeholder="Admin response (optional)..."
                                            value={adminResponse[ticket.ticket_id] || ''}
                                            onChange={(e) => setAdminResponse({
                                                ...adminResponse,
                                                [ticket.ticket_id]: e.target.value
                                            })}
                                            rows="2"
                                        />
                                        <div className="action-buttons">
                                            <button
                                                className="approve-btn"
                                                onClick={() => handleTicketAction(ticket.ticket_id, 'approved')}
                                                disabled={loading}
                                            >
                                                ✓ Approve
                                            </button>
                                            <button
                                                className="reject-btn"
                                                onClick={() => handleTicketAction(ticket.ticket_id, 'rejected')}
                                                disabled={loading}
                                            >
                                                ✕ Reject
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {ticket.admin_response && (
                                    <div className="admin-response-box">
                                        <strong>Admin Response:</strong>
                                        <p>{ticket.admin_response}</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>

            <style jsx>{`
                .admin-tickets {
                    padding: 20px;
                }

                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }

                .filter-buttons button {
                    padding: 8px 16px;
                    margin-right: 8px;
                    border: 1px solid #ddd;
                    background: white;
                    border-radius: 5px;
                    cursor: pointer;
                }

                .filter-buttons button.active {
                    background: #007bff;
                    color: white;
                    border-color: #007bff;
                }

                .tickets-container {
                    display: grid;
                    gap: 20px;
                }

                .ticket-card {
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }

                .ticket-header-info {
                    display: flex;
                    justify-content: space-between;
                    align-items: start;
                    margin-bottom: 15px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #f0f0f0;
                }

                .ticket-header-info h3 {
                    margin: 0 0 8px 0;
                }

                .member-details {
                    color: #666;
                    font-size: 14px;
                    display: flex;
                    gap: 12px;
                }

                .employee-badge {
                    background: #6c757d;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                }

                .status-badge {
                    color: white;
                    padding: 6px 14px;
                    border-radius: 16px;
                    font-size: 12px;
                    font-weight: 600;
                }

                .ticket-content {
                    margin-top: 15px;
                }

                .request-details p {
                    margin: 10px 0;
                }

                .highlight {
                    color: #007bff;
                    font-weight: 600;
                }

                .date {
                    color: #666;
                    margin-top: 12px;
                }

                .action-section {
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                }

                .action-section textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    font-family: inherit;
                }

                .action-buttons {
                    display: flex;
                    gap: 10px;
                }

                .approve-btn, .reject-btn {
                    padding: 10px 24px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: 500;
                    flex: 1;
                }

                .approve-btn {
                    background: #28a745;
                    color: white;
                }

                .approve-btn:hover {
                    background: #218838;
                }

                .reject-btn {
                    background: #dc3545;
                    color: white;
                }

                .reject-btn:hover {
                    background: #c82333;
                }

                .admin-response-box {
                    margin-top: 15px;
                    padding: 12px;
                    background: #e7f3ff;
                    border-left: 4px solid #007bff;
                    border-radius: 4px;
                }

                .admin-response-box strong {
                    display: block;
                    margin-bottom: 8px;
                    color: #007bff;
                }

                .no-data {
                    text-align: center;
                    padding: 60px;
                    color: #666;
                }

                .message {
                    padding: 12px 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }

                .message.success {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }

                .message.error {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
            `}</style>
        </div>
    )
}

export default AdminTickets
