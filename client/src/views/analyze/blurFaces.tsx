import { useState } from 'react'
import axios from "axios"

const BlurFaces = () => {
  const [result, setResult] = useState<any>(null)
  const [imgUrl, setImgUrl] = useState<any>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]

    if (!file) {
      alert('Choose file')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    const res = await axios.post("http://127.0.0.1:8000/blur_faces", formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
       responseType: "blob"
    })

    if (res.data) {
      const imageUrl = URL.createObjectURL(res.data)
      setImgUrl(imageUrl)
    }
  }

  return (
    <div className="account-container">
      <fieldset className="fieldset" style={{ margin: '50px 0' }}>
        <legend className="fieldset-legend">Blur Faces</legend>
        <input type="file" accept="" className="file-input" 
          onChange={handleFileUpload}
        />
      </fieldset>

      {imgUrl &&
        <div><img src={imgUrl} alt="" /></div>
      }
      {result && 
        <div>
          <div>Filename: {result.filename}</div>
          <div>Number of faces: {result.num_faces}</div>
          <div>Faces coordinates: <br />
            {result.faces.map((face: any, index: number) => (
              <div key={index}>
                {face.join(', ')}
              </div>              
            ))}
          </div>
        </div>
      }
    </div>
  )
}

export default BlurFaces