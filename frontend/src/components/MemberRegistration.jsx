import { useState } from 'react'
import axios from 'axios'

function MemberRegistration({ apiBaseUrl, onSuccess }) {
    const [formData, setFormData] = useState({
        name: '',
        phone: '',
        email: ''
    })
    const [loading, setLoading] = useState(false)
    const [message, setMessage] = useState({ type: '', text: '' })
    const [generatedIds, setGeneratedIds] = useState({ memberId: '', employeeId: '' })
    const [validationErrors, setValidationErrors] = useState({})

    const validatePhone = (phone) => {
        const cleaned = phone.replace(/[\s\-+]/g, '')
        return /^\d{10}$/.test(cleaned)
    }

    const validateEmail = (email) => {
        if (!email) return true // Optional field
        const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
        return pattern.test(email)
    }

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData({
            ...formData,
            [name]: value
        })

        // Clear validation error for this field
        if (validationErrors[name]) {
            setValidationErrors({
                ...validationErrors,
                [name]: ''
            })
        }
    }

    const handleBlur = (e) => {
        const { name, value } = e.target
        const errors = { ...validationErrors }

        if (name === 'phone' && value && !validatePhone(value)) {
            errors.phone = 'Phone must be exactly 10 digits'
        }

        if (name === 'email' && value && !validateEmail(value)) {
            errors.email = 'Invalid email format'
        }

        setValidationErrors(errors)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setMessage({ type: '', text: '' })
        setGeneratedIds({ memberId: '', employeeId: '' })

        // Final validation
        const errors = {}
        if (!validatePhone(formData.phone)) {
            errors.phone = 'Phone must be exactly 10 digits'
        }
        if (formData.email && !validateEmail(formData.email)) {
            errors.email = 'Invalid email format'
        }

        if (Object.keys(errors).length > 0) {
            setValidationErrors(errors)
            setLoading(false)
            return
        }

        try {
            const payload = {
                name: formData.name,
                phone: formData.phone,
                email: formData.email || null
                // monthly_amount and due_day will use backend defaults (₹500 on 5th)
            }

            const token = localStorage.getItem('token')
            const response = await axios.post(`${apiBaseUrl}/admin/members`, payload, {
                headers: { 'Authorization': `Bearer ${token}` }
            })

            setMessage({
                type: 'success',
                text: `Member registered successfully! Member ID: ${response.data.member_id} | Employee ID: ${response.data.employee_id}`
            })
            setGeneratedIds({
                memberId: response.data.member_id,
                employeeId: response.data.employee_id
            })
            setFormData({
                name: '',
                phone: '',
                email: ''
            })

            // Call success callback to refresh other components
            if (onSuccess) onSuccess()

        } catch (err) {
            setMessage({
                type: 'error',
                text: err.response?.data?.detail || 'Failed to register member'
            })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="registration">
            <h2>Register New Member</h2>

            {message.text && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            {generatedIds.memberId && (
                <div className="employee-id-display">
                    <strong>Member ID:</strong>
                    <span className="employee-id">{generatedIds.memberId}</span>
                    <span style={{ margin: '0 10px' }}>|</span>
                    <strong>Employee ID:</strong>
                    <span className="employee-id">{generatedIds.employeeId}</span>
                    <button
                        type="button"
                        onClick={() => {
                            navigator.clipboard.writeText(`${generatedIds.memberId} | ${generatedIds.employeeId}`)
                            alert('IDs copied!')
                        }}
                        className="copy-btn-small"
                    >
                        📋 Copy Both
                    </button>
                </div>
            )}

            <form onSubmit={handleSubmit} className="registration-form">
                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="name">Full Name *</label>
                        <input
                            id="name"
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="Enter full name"
                            required
                        />
                    </div>
                </div>

                <p style={{ color: '#10b981', fontSize: '14px', marginTop: '-10px', marginBottom: '15px' }}>
                    ℹ️ Member ID, Employee ID auto-generated | All members contribute <strong>₹500 on 5th</strong> of each month
                </p>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="phone">Phone Number * (10 digits)</label>
                        <input
                            id="phone"
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            onBlur={handleBlur}
                            placeholder="9876543210"
                            required
                            className={validationErrors.phone ? 'error' : ''}
                        />
                        {validationErrors.phone && (
                            <small className="error-text">{validationErrors.phone}</small>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email (Optional)</label>
                        <input
                            id="email"
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            onBlur={handleBlur}
                            placeholder="email@example.com"
                            className={validationErrors.email ? 'error' : ''}
                        />
                        {validationErrors.email && (
                            <small className="error-text">{validationErrors.email}</small>
                        )}
                    </div>
                </div>

                <button type="submit" className="submit-btn" disabled={loading}>
                    {loading ? 'Registering...' : '✓ Register Member'}
                </button>
            </form>

            <style jsx>{`
                .employee-id-display {
                    background: #e7f3ff;
                    border: 2px solid #007bff;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }

                .employee-id {
                    font-family: monospace;
                    font-size: 18px;
                    font-weight: bold;
                    color: #007bff;
                    background: white;
                    padding: 8px 12px;
                    border-radius: 4px;
                }

                .copy-btn-small {
                    padding: 6px 12px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 12px;
                }

                .copy-btn-small:hover {
                    background: #0056b3;
                }

                .form-group input.error,
                .form-group textarea.error {
                    border-color: #dc3545;
                    background-color: #fff5f5;
                }

                .error-text {
                    color: #dc3545;
                    font-size: 12px;
                    margin-top: 4px;
                    display: block;
                }
            `}</style>
        </div>
    )
}

export default MemberRegistration
