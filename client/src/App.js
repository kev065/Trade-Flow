import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './components/LandingPage';
import OrderForm from './components/OrderForm';
import Login from './components/Login';
import Signup from './components/Signup';
import './light.css';
import './dark.css';
import './App.css';

function App() {
  const [theme, setTheme] = useState('light'); 
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  };

  const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route {...rest} render={(props) => (
      isAuthenticated === true
        ? <Component {...props} />
        : <Redirect to='/login' />
    )} />
  );

  return (
    <Router>
      <div className={`App ${theme}`}>
        <Header toggleTheme={toggleTheme} />
        <div className="chart">
          <Switch>
            <Route path="/login" component={Login} />
            <Route path="/signup" component={Signup} />
            <PrivateRoute path="/orderform" component={OrderForm} />
            <Route path="/" component={LandingPage} />
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;

