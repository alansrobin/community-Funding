import { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function ChangePasswordModal({ onPasswordChanged }) {
    const [currentPassword, setCurrentPassword] = useState('')
    const [newPassword, setNewPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')

        // Validation
        if (newPassword.length < 6) {
            setError('New password must be at least 6 characters long')
            return
        }

        if (newPassword !== confirmPassword) {
            setError('New passwords do not match')
            return
        }

        try {
            setLoading(true)
            const token = localStorage.getItem('token')

            await axios.post(
                `${API_BASE_URL}/auth/change-password`,
                {
                    current_password: currentPassword,
                    new_password: newPassword
                },
                {
                    headers: { 'Authorization': `Bearer ${token}` }
                }
            )

            // Notify parent component
            onPasswordChanged()
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to change password')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="modal-overlay">
            <div className="modal-content password-change-modal">
                <div className="modal-header">
                    <h2>🔒 Change Your Password</h2>
                    <p className="modal-subtitle">
                        You are using a default password. Please change it for security.
                    </p>
                </div>

                {error && <div className="error-message-inline">{error}</div>}

                <form onSubmit={handleSubmit} className="password-form">
                    <div className="form-group">
                        <label htmlFor="current">Current Password</label>
                        <input
                            id="current"
                            type="password"
                            value={currentPassword}
                            onChange={(e) => setCurrentPassword(e.target.value)}
                            placeholder="pass123"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="new">New Password</label>
                        <input
                            id="new"
                            type="password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            placeholder="At least 6 characters"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="confirm">Confirm New Password</label>
                        <input
                            id="confirm"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Re-enter new password"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="submit-btn"
                        disabled={loading}
                    >
                        {loading ? 'Changing Password...' : '✓ Change Password'}
                    </button>
                </form>
            </div>
        </div>
    )
}

export default ChangePasswordModal
