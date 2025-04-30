import { useEffect } from 'react'
import { useNavigate, Routes, Route, Navigate 
  } from 'react-router-dom'
import Analyze from './views/analyze/analyze'
import AnalyzeImg from './views/analyze/analyzeImg'
import Predict from './views/predict/predict'
import Signin from './views/signin'
import BlurFaces from './views/analyze/blurFaces'
import { Link } from 'react-router-dom'

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
      <div className=""
        style={{ display: 'flex', gap: 15 }}
      >
        <Link to="/analyze">Analyze</Link>
        <Link to="/predict">Predict</Link>
        <Link to="/analyze_img">Analyze image</Link>
        <Link to="/blur_faces">Blur faces</Link>
      </div>

      <Routes>
        <Route path="/" element={<Navigate to="/analyze" replace/>} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/analyze_img" element={<AnalyzeImg />} />
        <Route path="/blur_faces" element={<BlurFaces />} />
      </Routes>
    </>
  )
}

export default App
