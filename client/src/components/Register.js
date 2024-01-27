import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = event => {
    event.preventDefault();
  
    axios.post('http://localhost:5555/register', {
      email: email,
      username: username,
      password: password
    })
    .then(response => {
      console.log('Register Response:', response.data);
  
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        navigate('/');
      } else {
        alert('Registration failed');
      }
    })
    .catch(error => console.error('Error registering', error));
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email:
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      </label>
      <label>
        Username:
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
      </label>
      <label>
        Password:
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      </label>
      <input type="submit" value="Register" />
    </form>
  );
}

export default Register;
