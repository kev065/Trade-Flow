import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Login({ setIsLoggedIn }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = event => {
    event.preventDefault();
  
    axios.post('http://localhost:5555/login', {
      username: username,
      password: password
    })
    .then(response => {
      console.log('Login Response:', response.data);
  
      if (response.data.access_token) {
        setIsLoggedIn(true);
        localStorage.setItem('token', response.data.access_token);
        navigate('/');
      } else {
        alert('Invalid username or password');
      }
    })
    .catch(error => console.error('Error logging in', error));
  };
  

  return (
    <div className="login-form">
      <h2>User Log In Form</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label>Username:</label>
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
        </div>
        <div className="input-group">
          <label>Password:</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <input type="submit" value="Log in" />
      </form>
      <Link to="/register">Go to Registration Page</Link>
    </div>
  );
}

export default Login;
