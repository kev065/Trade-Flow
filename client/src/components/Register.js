import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import zxcvbn from 'zxcvbn';

function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const navigate = useNavigate();

  const handleSubmit = async event => {
    event.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match. Please enter matching passwords.');
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post('http://localhost:5555/register', {
        email: email,
        username: username,
        password: password
      });

      console.log('Register Response:', response.data);

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        navigate('/login');
      } else {
        alert('Registration failed');
      }
    } catch (error) {
      console.error('Error registering', error);
      alert('Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = event => {
    const newPassword = event.target.value;
    setPassword(newPassword);
    const result = zxcvbn(newPassword);
    setPasswordStrength(result.score); 
  };

  return (
    <div className="register-form">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Email:</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </div>
        <div className="input-group">
          <label>Username:</label>
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} required />
        </div>
        <div className="input-group">
          <label>Password:</label>
          <input type="password" value={password} onChange={handlePasswordChange} required />
          <meter max="4" value={passwordStrength} />
        </div>
        <div className="input-group">
          <label>Confirm Password:</label>
          <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
    </div>
  );
  
}

export default Register;
