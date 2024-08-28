import React, { useState } from 'react';
import { Form, Button }    from 'react-bootstrap';
import axios               from 'axios';
import { useNavigate }     from 'react-router-dom';

import '../../App.css';  

function RegisterForm() {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [message, setMessage]   = useState('');
    const [isError, setIsError]   = useState(false);
    const navigate                = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/auth/register', formData);
            setMessage(response.data.message);
            setIsError(false);
        } catch (error) {
            setMessage(error.response.data.message);
            setIsError(true);
        }
    };

    const switchForm = () => {
        navigate('/login');
    };

    return (
        <div className="login-form-container">
            <Form onSubmit={handleSubmit}>
                <h2 className="text-center mb-4">Register</h2>
                {message && (
                    <p className={`message ${isError ? 'message-error' : 'message-success'}`}>
                        {message}
                    </p>
                )}
                <Form.Group controlId="formUsername" className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                        placeholder="Enter your username"
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formPassword" className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        placeholder="Enter your password"
                        required
                    />
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100">
                    Register
                </Button>
                <p className="text-center mt-3">
                    Already have an account?{' '}
                    <Button variant="link" onClick={switchForm} className="p-0 align-baseline">
                        Login here
                    </Button>
                </p>
            </Form>
        </div>
    );
}

export default RegisterForm;