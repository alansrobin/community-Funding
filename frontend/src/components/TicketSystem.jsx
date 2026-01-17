import { useState, useEffect } from 'react'
import axios from 'axios'

function TicketSystem({ apiBaseUrl, token }) {
    const [tickets, setTickets] = useState([])
    const [showForm, setShowForm] = useState(false)
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState({ type: '', text: '' })
    const [formData, setFormData] = useState({
        request_type: 'monthly_amount',
        reason: '',
        new_value: ''
    })

    const fetchTickets = async () => {
        try {
            const response = await axios.get(`${apiBaseUrl}/member/tickets`, {
                headers: { Authorization: `Bearer ${token}` }
            })
            setTickets(response.data)
        } catch (err) {
            console.error('Error fetching tickets:', err)
        }
    }

    useEffect(() => {
        fetchTickets()
    }, [])

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setMessage({ type: '', text: '' })

        try {
            await axios.post(`${apiBaseUrl}/member/tickets`, {
                ...formData,
                new_value: parseFloat(formData.new_value)
            }, {
                headers: { Authorization: `Bearer ${token}` }
            })

            setMessage({ type: 'success', text: 'Ticket created successfully!' })
            setFormData({ request_type: 'monthly_amount', reason: '', new_value: '' })
            setShowForm(false)
            fetchTickets()
        } catch (err) {
            setMessage({
                type: 'error',
                text: err.response?.data?.detail || 'Failed to create ticket'
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
        <div className="ticket-system">
            <div className="ticket-header">
                <h2>Support Tickets</h2>
                <button
                    className="create-ticket-btn"
                    onClick={() => setShowForm(!showForm)}
                >
                    {showForm ? '✕ Cancel' : '+ Create Ticket'}
                </button>
            </div>

            {message.text && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            {showForm && (
                <form onSubmit={handleSubmit} className="ticket-form">
                    <h3>Request Change</h3>

                    <div className="form-group">
                        <label>Request Type</label>
                        <select
                            value={formData.request_type}
                            onChange={(e) => setFormData({ ...formData, request_type: e.target.value })}
                            required
                        >
                            <option value="monthly_amount">Monthly Amount</option>
                            <option value="due_day">Due Day</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Reason for Change</label>
                        <textarea
                            value={formData.reason}
                            onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                            placeholder="Please explain why you need this change..."
                            rows="3"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>New Value</label>
                        <input
                            type="number"
                            value={formData.new_value}
                            onChange={(e) => setFormData({ ...formData, new_value: e.target.value })}
                            placeholder={formData.request_type === 'monthly_amount' ? 'Enter new amount' : 'Enter day (1-31)'}
                            min={formData.request_type === 'due_day' ? '1' : '1'}
                            max={formData.request_type === 'due_day' ? '31' : undefined}
                            step={formData.request_type === 'monthly_amount' ? '0.01' : '1'}
                            required
                        />
                    </div>

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? 'Submitting...' : 'Submit Ticket'}
                    </button>
                </form>
            )}

            <div className="tickets-list">
                <h3>My Tickets</h3>
                {tickets.length === 0 ? (
                    <p className="no-tickets">No tickets yet. Create one to request changes.</p>
                ) : (
                    <div className="tickets-grid">
                        {tickets.map((ticket) => (
                            <div key={ticket.ticket_id} className="ticket-card">
                                <div className="ticket-header-row">
                                    <span className="ticket-id">#{ticket.ticket_id.slice(0, 8)}</span>
                                    <span className="employee-id-badge">EMP: {ticket.employee_id}</span>
                                    <span
                                        className="ticket-status"
                                        style={{ backgroundColor: getStatusColor(ticket.status) }}
                                    >
                                        {ticket.status.toUpperCase()}
                                    </span>
                                </div>

                                <div className="ticket-info">
                                    <p><strong>Type:</strong> {ticket.request_type === 'monthly_amount' ? 'Monthly Amount Change' : 'Due Day Change'}</p>
                                    <p><strong>Current Value:</strong> {ticket.current_value}</p>
                                    <p><strong>Requested Value:</strong> {ticket.new_value}</p>
                                    <p><strong>Reason:</strong> {ticket.reason}</p>
                                    <p className="ticket-date">
                                        <small>Created: {new Date(ticket.created_at).toLocaleDateString()}</small>
                                    </p>
                                    {ticket.admin_response && (
                                        <div className="admin-response">
                                            <strong>Admin Response:</strong>
                                            <p>{ticket.admin_response}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <style jsx>{`
                .ticket-system {
                    padding: 20px;
                }
                
                .ticket-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                
                .create-ticket-btn {
                    padding: 10px 20px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: 500;
                }
                
                .create-ticket-btn:hover {
                    background: #0056b3;
                }
                
                .ticket-form {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 30px;
                }
                
                .form-group {
                    margin-bottom: 15px;
                }
                
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 500;
                }
                
                .form-group input,
                .form-group select,
                .form-group textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                }
                
                .tickets-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 20px;
                }
                
                .ticket-card {
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 15px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .ticket-header-row {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #eee;
                }
                
                .ticket-id {
                    font-family: monospace;
                    font-size: 12px;
                    color: #666;
                }
                
                .employee-id-badge {
                    background: #6c757d;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                }
                
                .ticket-status {
                    color: white;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                }
                
                .ticket-info p {
                    margin: 8px 0;
                    font-size: 14px;
                }
                
                .ticket-date {
                    color: #666;
                    margin-top: 10px;
                }
                
                .admin-response {
                    margin-top: 15px;
                    padding: 10px;
                    background: #e7f3ff;
                    border-left: 3px solid #007bff;
                    border-radius: 4px;
                }
                
                .admin-response strong {
                    display: block;
                    margin-bottom: 5px;
                    color: #007bff;
                }
                
                .no-tickets {
                    text-align: center;
                    color: #666;
                    padding: 40px;
                }
                
                .message {
                    padding: 12px;
                    border-radius: 5px;
                    margin-bottom: 15px;
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

export default TicketSystem
