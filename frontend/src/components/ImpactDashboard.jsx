import { useState, useEffect } from 'react'
import axios from 'axios'

function ImpactDashboard({ apiBaseUrl }) {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchImpactStats()
    }, [])

    const fetchImpactStats = async () => {
        try {
            const token = localStorage.getItem('token')
            const response = await axios.get(`${apiBaseUrl}/member/impact/stats`, {
                headers: { 'Authorization': `Bearer ${token}` }
            })
            setStats(response.data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <div className="loading-container"><div className="spinner"></div></div>

    // Helper for simple bar chart
    const AllocationBar = ({ label, value, color }) => (
        <div className="allocation-item">
            <div className="allocation-header">
                <span>{label}</span>
                <span>{value}%</span>
            </div>
            <div className="progress-bg">
                <div
                    className="progress-fill"
                    style={{ width: `${value}%`, backgroundColor: color }}
                ></div>
            </div>
        </div>
    )

    return (
        <div className="impact-dashboard">
            <div className="impact-hero">
                <div className="impact-header-content">
                    <h1>🌍 Community Impact</h1>
                    <p>{stats.impact_message}</p>
                </div>
            </div>

            <div className="impact-grid">
                {/* Total Progress Card */}
                <div className="stat-card primary impact-card">
                    <div className="stat-content">
                        <span className="stat-label">Total Community Fund</span>
                        <div className="stat-value">₹{stats.total_raised.toLocaleString()}</div>
                        <div className="goal-progress">
                            <div className="progress-bg">
                                <div
                                    className="progress-fill"
                                    style={{ width: `${stats.progress_percentage}%`, backgroundColor: 'var(--success)' }}
                                ></div>
                            </div>
                            <small>{stats.progress_percentage}% of ₹{stats.monthly_goal.toLocaleString()} Goal</small>
                        </div>
                    </div>
                    <span className="stat-icon">📈</span>
                </div>

                {/* Transparency Card */}
                <div className="monthly-summary impact-card">
                    <h3>📊 Fund Transparency</h3>
                    <div className="allocation-list">
                        <AllocationBar label="🎓 Education" value={stats.fund_allocation.Education} color="var(--info)" />
                        <AllocationBar label="🏥 Medical Aid" value={stats.fund_allocation.Medical} color="var(--danger)" />
                        <AllocationBar label="🏗️ Infrastructure" value={stats.fund_allocation.Infrastructure} color="var(--warning)" />
                        <AllocationBar label="🛡️ Reserves" value={stats.fund_allocation.Reserves} color="var(--success)" />
                    </div>
                </div>
            </div>

            {/* Initiatives Section */}
            <div className="initiatives-section">
                <h2>Active Initiatives</h2>
                <div className="initiatives-grid">
                    {stats.active_initiatives.map(project => (
                        <div key={project.id} className="member-card initiative-card">
                            <div className="member-header">
                                <div className="member-info">
                                    <h3>{project.name}</h3>
                                    <p className="member-contact">{project.description}</p>
                                </div>
                                <span className={`status-badge ${project.status === 'Active' ? 'success' : 'info'}`}>
                                    {project.status}
                                </span>
                            </div>
                            <div className="member-stats" style={{ padding: '20px' }}>
                                <div style={{ width: '100%' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                                        <small>Funded</small>
                                        <small>₹{project.raised.toLocaleString()} / ₹{project.target.toLocaleString()}</small>
                                    </div>
                                    <div className="progress-bg">
                                        <div
                                            className="progress-fill"
                                            style={{
                                                width: `${(project.raised / project.target) * 100}%`,
                                                backgroundColor: 'var(--primary)'
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <style>{`
                .impact-dashboard { animation: fadeIn 0.5s ease-in; }
                .impact-hero { 
                    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
                    padding: 40px;
                    border-radius: 20px;
                    color: white;
                    margin-bottom: 30px;
                    text-align: center;
                    box-shadow: var(--shadow-lg);
                }
                .impact-hero h1 { font-size: 2.5rem; margin-bottom: 10px; }
                .impact-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-bottom: 40px; }
                .progress-bg { background: var(--bg-primary); height: 10px; border-radius: 5px; overflow: hidden; margin-top: 10px; }
                .progress-fill { height: 100%; transition: width 1s ease-out; }
                .allocation-list { display: flex; flex-direction: column; gap: 15px; }
                .allocation-header { display: flex; justify-content: space-between; font-weight: 600; color: var(--text-secondary); }
                .initiatives-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .initiative-card { border-left: 5px solid var(--primary); }
            `}</style>
        </div>
    )
}

export default ImpactDashboard
