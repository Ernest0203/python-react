import { useState } from 'react'
import axios from "axios"
import AnalyzeResult from "./analyzeResult"
import AnalyzeScatter from './analyzeScatter'

const Analyze = () => {
  const [result, setResult] = useState<any>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]

    if (!file) {
      alert('Choose file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post("http://127.0.0.1:8000/analyze", formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (res.data) {
      setResult(res.data)
    }
  }

  return (
    <div className="account-container">
      <fieldset className="fieldset" style={{ marginTop: 50 }}>
        <legend className="fieldset-legend">Analyze</legend>
        <input type="file" accept=".csv" className="file-input" 
          onChange={handleFileUpload}
        />
      </fieldset>
      {result && 
        <div>
          <AnalyzeResult result={result} />
          <AnalyzeScatter result={result} />
        </div>
      }
    </div>
  )
}

export default Analyze