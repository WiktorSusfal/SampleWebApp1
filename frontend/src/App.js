import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'

import MainPage      from './components/main/main_page';
import LoginForm     from './components/auth/login_form';
import RegisterForm  from './components/auth/register_form';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login"    element={<LoginForm />} />
                <Route path="/register" element={<RegisterForm />} />
                <Route path="/main"     element={<MainPage />} />
                <Route path="*"         element={<Navigate to="/main" />} />
            </Routes>
        </Router>
    );
}

export default App;