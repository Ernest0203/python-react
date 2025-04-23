import { useState } from "react"
import axios from "axios"

const Signin = () => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const login = async () => {
    const res = await axios.post("http://127.0.0.1:8000/auth/login", {
        email: username,
        password: password,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        withCredentials: true,
      }  
    )
    if (res.data.access_token) {
      localStorage.setItem("token", res.data.access_token)
      window.open("/account", "_self")
    } else {
      alert("Invalid credentials")
    }
  }

  const register = async () => {
    const res = await axios.post("http://127.0.0.1:8000/auth/register", {
        email: username,
        password: password,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        withCredentials: true,
      }  
    )
    if (res.data) {
      await login()
    } else {
      alert("Invalid credentials")
    }
  }

  return (
    <div>
      <fieldset className="fieldset">
        <legend className="fieldset-legend">Signin</legend>
        <input type="text" className="input" placeholder="Username" 
          onChange={(e) => setUsername(e.target.value)} 
          value={username}
        />
        <br />
        <br />
        <input type="password" className="input" placeholder="Password" 
          onChange={(e) => setPassword(e.target.value)} 
          value={password}  
        />
        <br />
        <br />
        <button className="btn" onClick={login}>Signin</button>
      </fieldset>

      <br />

      <fieldset className="fieldset">
        <legend className="fieldset-legend">Signup</legend>
        <input type="text" className="input" placeholder="Username" />
        <br />
        <br />
        <input type="password" className="input" placeholder="Password" />
        <br />
        <br />
        <button className="btn" onClick={register}>Signup</button>
      </fieldset>
    </div>
  )
}

export default Signin