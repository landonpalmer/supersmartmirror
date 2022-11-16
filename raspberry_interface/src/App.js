import './App.css';
import {useEffect, useState} from 'react';
import axios from 'axios'
function App() {
  const [test, setTest] = useState("");
  useEffect(() => {
    axios.get("http://localhost:5000/").then(res => setTest(res.data.test))
  }, []);
  return (
    <div>
      <h1>Super Smart Mirror running on Linux Rasperry (Hopefully)</h1>
      <p>{test}</p>
    </div>
  );
}

export default App;
