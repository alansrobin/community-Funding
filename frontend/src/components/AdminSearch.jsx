import { useState } from 'react'
import axios from 'axios'

function AdminSearch({ apiBaseUrl, token }) {
    const [searchQuery, setSearchQuery] = useState('')
    const [searchResult, setSearchResult] = useState(null)
    const [searching, setSearching] = useState(false)
    const [error, setError] = useState('')

    const handleSearch = async (e) => {
        e.preventDefault()
        if (!searchQuery.trim()) return

        setSearching(true)
        setError('')
        setSearchResult(null)

        try {
            const response = await axios.get(
                `${apiBaseUrl}/admin/search?employee_id=${encodeURIComponent(searchQuery)}`,
                { headers: { Authorization: `Bearer ${token}` } }
            )
            setSearchResult(response.data)
        } catch (err) {
            setError(err.response?.data?.detail || 'Member not found')
        } finally {
            setSearching(false)
        }
    }

    const copyToClipboard = (text, label) => {
        navigator.clipboard.writeText(text).then(() => {
            alert(`${label} copied to clipboard!`)
        })
    }

    return (
        <div className="admin-search">
            <h2>Search Member by Employee ID</h2>

            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    placeholder="Enter Employee ID (e.g., EMP-20260116-1234)"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="search-input"
                />
                <button type="submit" disabled={searching} className="search-btn">
                    {searching ? '🔍 Searching...' : '🔍 Search'}
                </button>
            </form>

            {error && (
                <div className="search-error">
                    ❌ {error}
                </div>
            )}

            {searchResult && (
                <div className="search-result">
                    <div className="result-header">
                        <h3>{searchResult.name}</h3>
                        <span className={`classification-badge ${searchResult.classification.toLowerCase().replace(/\s+/g, '-')}`}>
                            {searchResult.classification}
                        </span>
                    </div>

                    <div className="result-grid">
                        <div className="result-item">
                            <label>Employee ID:</label>
                            <div className="value-with-copy">
                                <span className="employee-id-text">{searchResult.employee_id}</span>
                                <button
                                    onClick={() => copyToClipboard(searchResult.employee_id, 'Employee ID')}
                                    className="copy-icon-btn"
                                    title="Copy Employee ID"
                                >
                                    📋
                                </button>
                            </div>
                        </div>

                        <div className="result-item">
                            <label>Member ID:</label>
                            <span>{searchResult.member_id}</span>
                        </div>

                        <div className="result-item">
                            <label>Phone Number:</label>
                            <div className="value-with-copy">
                                <span>{searchResult.phone}</span>
                                <button
                                    onClick={() => copyToClipboard(searchResult.phone, 'Phone number')}
                                    className="copy-icon-btn"
                                    title="Copy Phone"
                                >
                                    📋
                                </button>
                            </div>
                        </div>

                        <div className="result-item">
                            <label>Email:</label>
                            <div className="value-with-copy">
                                <span>{searchResult.email || 'N/A'}</span>
                                {searchResult.email && (
                                    <button
                                        onClick={() => copyToClipboard(searchResult.email, 'Email')}
                                        className="copy-icon-btn"
                                        title="Copy Email"
                                    >
                                        📋
                                    </button>
                                )}
                            </div>
                        </div>

                        <div className="result-item">
                            <label>Monthly Amount:</label>
                            <span>₹{searchResult.monthly_amount}</span>
                        </div>

                        <div className="result-item">
                            <label>Due Day:</label>
                            <span>Day {searchResult.due_day} of month</span>
                        </div>

                        <div className="result-item">
                            <label>Total Contributions:</label>
                            <span>{searchResult.total_contributions}</span>
                        </div>

                        <div className="result-item">
                            <label>Paid:</label>
                            <span className="success-text">{searchResult.paid_count}</span>
                        </div>

                        <div className="result-item">
                            <label>Missed:</label>
                            <span className="danger-text">{searchResult.missed_count}</span>
                        </div>

                        <div className="result-item">
                            <label>Average Delay:</label>
                            <span>{searchResult.avg_delay_days} days</span>
                        </div>

                        <div className="result-item">
                            <label>Current Delay:</label>
                            <span className={searchResult.current_delay_days > 30 ? 'danger-text' : ''}>
                                {searchResult.current_delay_days} days
                            </span>
                        </div>
                    </div>
                </div>
            )}

            <style jsx>{`
                .admin-search {
                    background: white;
                    border-radius: 10px;
                    padding: 24px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }

                .admin-search h2 {
                    margin-top: 0;
                    margin-bottom: 20px;
                }

                .search-form {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 20px;
                }

                .search-input {
                    flex: 1;
                    padding: 12px 16px;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-size: 16px;
                }

                .search-input:focus {
                    outline: none;
                    border-color: #007bff;
                }

                .search-btn {
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 500;
                    font-size: 16px;
                }

                .search-btn:hover:not(:disabled) {
                    background: #0056b3;
                }

                .search-btn:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }

                .search-error {
                    background: #f8d7da;
                    color: #721c24;
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid #f5c6cb;
                }

                .search-result {
                    border: 2px solid #007bff;
                    border-radius: 10px;
                    padding: 20px;
                    background: #f8f9fa;
                }

                .result-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #dee2e6;
                }

                .result-header h3 {
                    margin: 0;
                }

                .classification-badge {
                    padding: 6px 14px;
                    border-radius: 16px;
                    font-size: 13px;
                    font-weight: 600;
                }

                .classification-badge.regular {
                    background: #28a745;
                    color: white;
                }

                .classification-badge.occasional-delay {
                    background: #ffc107;
                    color: #000;
                }

                .classification-badge.high-risk-delay {
                    background: #dc3545;
                    color: white;
                }

                .result-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 16px;
                }

                .result-item {
                    background: white;
                    padding: 12px;
                    border-radius: 8px;
                }

                .result-item label {
                    display: block;
                    font-weight: 600;
                    color: #666;
                    margin-bottom: 6px;
                    font-size: 14px;
                }

                .result-item span {
                    font-size: 16px;
                }

                .value-with-copy {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .employee-id-text {
                    font-family: monospace;
                    font-weight: 600;
                    color: #007bff;
                }

                .copy-icon-btn {
                    background: transparent;
                    border: none;
                    cursor: pointer;
                    font-size: 18px;
                    padding: 4px;
                    opacity: 0.6;
                    transition: opacity 0.2s;
                }

                .copy-icon-btn:hover {
                    opacity: 1;
                }

                .success-text {
                    color: #28a745;
                    font-weight: 600;
                }

                .danger-text {
                    color: #dc3545;
                    font-weight: 600;
                }
            `}</style>
        </div>
    )
}

export default AdminSearch
