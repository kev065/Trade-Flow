import React, { useState } from 'react';
import axios from 'axios';

function Login({ setIsLoggedIn }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = event => {
    event.preventDefault();

    axios.post('http://localhost:5555/login', {
      username: username,
      password: password
    })
    .then(response => {
      if (response.data.authenticated) {
        setIsLoggedIn(true);
        localStorage.setItem('token', response.data.token);
      } else {
        alert('Invalid username or password');
      }
    })
    .catch(error => console.error('Error logging in', error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Username:
        <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
      </label>
      <label>
        Password:
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      </label>
      <input type="submit" value="Log in" />
    </form>
  );
}

export default Login;
