import { useEffect } from 'react'
import { useNavigate, Routes, Route, Navigate 
  } from 'react-router-dom'
import Analyze from './views/analyze/analyze'
import Predict from './views/predict/predict'
import Signin from './views/signin'

import './App.css'

function App() {
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (!token) {
      navigate('/signin')
    }
    // else {
    //   navigate('/analyze')
    // }

  }, [])

  return (
    <>
      <Routes>
        <Route path="/" element={<Navigate to="/analyze" replace/>} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/predict" element={<Predict />} />
      </Routes>
    </>
  )
}

export default App
