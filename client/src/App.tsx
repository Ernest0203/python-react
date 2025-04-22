import { useEffect } from 'react'
import { useNavigate, Routes, Route, Navigate 
  } from 'react-router-dom'
import Account from './views/account'
import Signin from './views/signin'

import './App.css'

function App() {
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      navigate('/signin')
    }
    else {
      navigate('/account')
    }

  }, [])

  return (
    <>
      <Routes>
        <Route path="/" element={<Navigate to="/account" replace/>} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/account" element={<Account />} />
      </Routes>
    </>
  )
}

export default App
