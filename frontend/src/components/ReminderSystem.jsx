import { useState, useEffect } from 'react'
import axios from 'axios'

function ReminderSystem({ apiBaseUrl, refreshKey }) {
    const [members, setMembers] = useState([])
    const [selectedMember, setSelectedMember] = useState(null)
    const [reminder, setReminder] = useState(null)
    const [loading, setLoading] = useState(true)
    const [loadingReminder, setLoadingReminder] = useState(false)
    const [copySuccess, setCopySuccess] = useState(false)

    useEffect(() => {
        fetchMembers()
    }, [refreshKey])

    const fetchMembers = async () => {
        try {
            setLoading(true)
            const response = await axios.get(`${apiBaseUrl}/members`)
            setMembers(response.data)
        } catch (err) {
            console.error('Failed to load members', err)
        } finally {
            setLoading(false)
        }
    }

    const fetchReminder = async (memberId) => {
        try {
            setLoadingReminder(true)
            setSelectedMember(memberId)
            const response = await axios.get(`${apiBaseUrl}/reminders/${memberId}`)
            setReminder(response.data)
            setCopySuccess(false)
        } catch (err) {
            console.error('Failed to load reminder', err)
            alert('Failed to generate reminder')
        } finally {
            setLoadingReminder(false)
        }
    }

    const handleSendReminder = async () => {
        if (!reminder || !selectedMember) return

        try {
            setLoadingReminder(true)
            const token = localStorage.getItem('token')
            // Using POST to send the edited message
            await axios.post(
                `${apiBaseUrl}/admin/reminders/${selectedMember}`,
                { custom_message: reminder.reminder_message },
                { headers: { 'Authorization': `Bearer ${token}` } }
            )
            alert('✅ Reminder sent successfully!')
        } catch (err) {
            console.error('Failed to send reminder', err)
            alert('❌ Failed to send reminder: ' + (err.response?.data?.detail || err.message))
        } finally {
            setLoadingReminder(false)
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

    if (loading) {
        return (
            <div className="loading-container">
                <div className="spinner"></div>
                <p>Loading members...</p>
            </div>
        )
    }

    return (
        <div className="reminder-system">
            <h2>Ethical Reminder System</h2>
            <p className="subtitle">Generate personalized, respectful reminders for members</p>

            <div className="reminder-content">
                <div className="members-selector">
                    <h3>Select Member</h3>
                    <div className="members-list-reminder">
                        {members.map(member => (
                            <div
                                key={member.member_id}
                                className={`member-item ${selectedMember === member.member_id ? 'active' : ''}`}
                                onClick={() => fetchReminder(member.member_id)}
                            >
                                <div className="member-info">
                                    <strong>{member.name}</strong>
                                    <span className="member-id-small">{member.member_id}</span>
                                </div>
                                <div className="member-badges">
                                    <span className={`classification-badge ${getClassificationColor(member.classification)}`}>
                                        {member.classification}
                                    </span>
                                    {member.missed_count > 0 && (
                                        <span className="missed-badge">
                                            {member.missed_count} missed
                                        </span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="reminder-display">
                    {loadingReminder ? (
                        <div className="loading-container">
                            <div className="spinner"></div>
                            <p>Generating reminder...</p>
                        </div>
                    ) : reminder ? (
                        <div className="reminder-card">
                            <div className="reminder-header">
                                <h3>Reminder for {reminder.member_name}</h3>
                                <span className={`classification-badge ${getClassificationColor(reminder.classification)}`}>
                                    {reminder.classification}
                                </span>
                            </div>

                            <div className="reminder-stats">
                                <div className="reminder-stat">
                                    <span className="label">Missed Payments:</span>
                                    <span className="value">{reminder.missed_payments}</span>
                                </div>
                                <div className="reminder-stat">
                                    <span className="label">Current Delay:</span>
                                    <span className="value">{reminder.delay_days} days</span>
                                </div>
                            </div>

                            <div className="reminder-message">
                                <label>Personalized Message (Editable):</label>
                                <textarea
                                    className="message-box-editable"
                                    value={reminder.reminder_message}
                                    onChange={(e) => setReminder({ ...reminder, reminder_message: e.target.value })}
                                />
                            </div>

                            <div className="reminder-actions">
                                <button className="inspire-btn" onClick={() => fetchReminder(selectedMember)}>
                                    🎲 Inspire Me
                                </button>
                                <button className="send-btn" onClick={handleSendReminder}>
                                    📤 Send Reminder
                                </button>
                                <div className="info-note">
                                    <strong>Note:</strong> Sending will email the member and update their dashboard.
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="no-selection">
                            <div className="empty-state">
                                <span className="empty-icon">📧</span>
                                <h3>No Member Selected</h3>
                                <p>Select a member from the list to generate a personalized reminder</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ReminderSystem
