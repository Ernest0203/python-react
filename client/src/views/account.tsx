import axios from "axios"

const Account = () => {
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

    console.log(res)
  }

  return (
    <div className="account-container">
      <fieldset className="fieldset" style={{ marginTop: 50 }}>
        <legend className="fieldset-legend">Pick a csv file</legend>
        <input type="file" accept=".csv" className="file-input" 
          onChange={handleFileUpload}
        />
      </fieldset>
    </div>
  )
}

export default Account