import { useState, useEffect } from 'react'
import axios from 'axios'

function FailedDashboard({ apiBaseUrl, token }) {
    const [stats, setStats] = useState(null)
    const [failedPayments, setFailedPayments] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchFailedData()
    }, [])

    const fetchFailedData = async () => {
        try {
            const [statsRes, paymentsRes] = await Promise.all([
                axios.get(`${apiBaseUrl}/admin/dashboard/failed-stats`, {
                    headers: { Authorization: `Bearer ${token}` }
                }),
                axios.get(`${apiBaseUrl}/admin/failed-payments`, {
                    headers: { Authorization: `Bearer ${token}` }
                })
            ])

            setStats(statsRes.data)
            setFailedPayments(paymentsRes.data)
        } catch (err) {
            console.error('Error fetching failed payments:', err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return <div className="loading">Loading failed payments data...</div>
    }

    return (
        <div className="failed-dashboard">
            <h2>Failed Payments Dashboard</h2>

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">⚠️</div>
                    <div className="stat-content">
                        <h3>{stats?.total_failed || 0}</h3>
                        <p>Total Failed Payments</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">₹</div>
                    <div className="stat-content">
                        <h3>₹{stats?.total_amount?.toLocaleString() || 0}</h3>
                        <p>Total Amount Pending</p>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">👥</div>
                    <div className="stat-content">
                        <h3>{stats?.members_affected || 0}</h3>
                        <p>Members Affected</p>
                    </div>
                </div>
            </div>

            <div className="failed-payments-section">
                <h3>Detailed Failed Payments</h3>
                {failedPayments.length === 0 ? (
                    <div className="no-data">
                        <p>✓ No failed payments found</p>
                    </div>
                ) : (
                    <div className="table-container">
                        <table className="failed-table">
                            <thead>
                                <tr>
                                    <th>Member Name</th>
                                    <th>Employee ID</th>
                                    <th>Member ID</th>
                                    <th>Due Date</th>
                                    <th>Amount</th>
                                    <th>Delay (Days)</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {failedPayments.map((payment, index) => (
                                    <tr key={payment.contribution_id || index}>
                                        <td>{payment.member_name}</td>
                                        <td>
                                            <span className="employee-badge">{payment.employee_id}</span>
                                        </td>
                                        <td>{payment.member_id}</td>
                                        <td>{new Date(payment.due_date).toLocaleDateString()}</td>
                                        <td className="amount">₹{payment.amount.toLocaleString()}</td>
                                        <td>
                                            <span className="delay-badge">{payment.delay_days} days</span>
                                        </td>
                                        <td>
                                            <span className="status-badge failed">{payment.status}</span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            <style jsx>{`
                .failed-dashboard {
                    padding: 20px;
                }

                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }

                .stat-card {
                    background: white;
                    border-radius: 10px;
                    padding: 24px;
                    display: flex;
                    align-items: center;
                    gap: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    border-left: 4px solid #dc3545;
                }

                .stat-icon {
                    font-size: 48px;
                }

                .stat-content h3 {
                    margin: 0;
                    font-size: 32px;
                    color: #dc3545;
                }

                .stat-content p {
                    margin: 5px 0 0 0;
                    color: #666;
                    font-size: 14px;
                }

                .failed-payments-section {
                    background: white;
                    border-radius: 10px;
                    padding: 24px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }

                .failed-payments-section h3 {
                    margin-top: 0;
                    margin-bottom: 20px;
                }

                .table-container {
                    overflow-x: auto;
                }

                .failed-table {
                    width: 100%;
                    border-collapse: collapse;
                }

                .failed-table th {
                    background: #f8f9fa;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #dee2e6;
                }

                .failed-table td {
                    padding: 12px;
                    border-bottom: 1px solid #dee2e6;
                }

                .failed-table tr:hover {
                    background: #f8f9fa;
                }

                .employee-badge {
                    background: #6c757d;
                    color: white;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 500;
                    display: inline-block;
                }

                .delay-badge {
                    background: #ffc107;
                    color: #000;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 500;
                    display: inline-block;
                }

                .status-badge {
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 500;
                    display: inline-block;
                }

                .status-badge.failed {
                    background: #dc3545;
                    color: white;
                }

                .amount {
                    font-weight: 600;
                    color: #dc3545;
                }

                .no-data {
                    text-align: center;
                    padding: 60px;
                    color: #28a745;
                    font-size: 18px;
                }

                .loading {
                    text-align: center;
                    padding: 60px;
                    color: #666;
                }
            `}</style>
        </div>
    )
}

export default FailedDashboard
