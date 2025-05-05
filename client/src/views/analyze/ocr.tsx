import { useState } from 'react'
import axios from "axios"

const AnalyzeTextImg = () => {
  const [result, setResult] = useState<any>(null)
  const [imgUrl, setImgUrl] = useState<any>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]

    if(file) {
      setImgUrl(URL.createObjectURL(file))
    }

    if (!file) {
      alert('Choose file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post("http://127.0.0.1:8000/ocr", formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (res.data) {
      setResult(res.data)
      console.log(res.data)
    }
  }

  return (
    <div className="account-container">
      <fieldset className="fieldset" style={{ margin: '50px 0' }}>
        <legend className="fieldset-legend">Analyze Image</legend>
        <input type="file" accept="" className="file-input" 
          onChange={handleFileUpload}
        />
      </fieldset>

      {imgUrl &&
        <div>
          <img style={{ maxWidth: '60vw' }} src={imgUrl} alt="" />
        </div>
      }
      <br />
      {result && 
        <div>
          <h3>Result:</h3>
          {result.text}
        </div>
      }
    </div>
  )
}

export default AnalyzeTextImg