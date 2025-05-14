import { useEffect, memo } from 'react'
import { useNavigate, Routes, Route, Navigate 
  } from 'react-router-dom'
import Analyze from './views/analyze/analyze'
import AnalyzeImg from './views/analyze/analyzeImg'
import Predict from './views/predict/predict'
import Signin from './views/signin'
import BlurFaces from './views/analyze/blurFaces'
import AnalyzeTextImg from './views/analyze/ocr'
import CryptoChart from './views/analyze/crypto'
import ReactTricks from './views/reactTricks'
import { Link } from 'react-router-dom'

import './App.css'

const NavBar = memo(() => {
  return (
    <div style={{ display: 'flex', gap: 15 }}>
      <Link to="/analyze">Analyze</Link>
      <Link to="/predict">Predict</Link>
      <Link to="/analyze_img">Analyze image</Link>
      <Link to="/blur_faces">Blur faces</Link>
      <Link to="/analyze_text">Analyze text</Link>
      <Link to="/crypto">Crypto predict</Link>
      <Link to="/react_tricks">React tricks</Link>
    </div>
  )
})

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
      <NavBar />

      <Routes>
        <Route path="/" element={<Navigate to="/analyze" replace/>} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/analyze_img" element={<AnalyzeImg />} />
        <Route path="/blur_faces" element={<BlurFaces />} />
        <Route path="/analyze_text" element={<AnalyzeTextImg />} />
        <Route path="/crypto" element={<CryptoChart />} />
        <Route path="/react_tricks" element={<ReactTricks />} />
      </Routes>
    </>
  )
}

export default App
