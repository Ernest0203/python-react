import { useState } from 'react'
import axios from "axios"
import PredictionChart from './predictionChart'

const Predict = () => {
  const [result, setResult] = useState<any>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]

    if (!file) {
      alert('Choose file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post("http://127.0.0.1:8000/predict", formData, {
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
        <legend className="fieldset-legend">Predict</legend>
        <input type="file" accept=".csv" className="file-input" 
          onChange={handleFileUpload}
        />
      </fieldset>
      {result && 
        <div>
          <PredictionChart actual={result.actual} predicted={result.predicted} />
        </div>
      }
    </div>
  )
}

export default Predict