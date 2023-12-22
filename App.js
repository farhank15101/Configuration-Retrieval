import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [result, setResult] = useState('');

  const handleGetAptConfigs = () => {
    setResult('');
    axios
      .get('http://localhost:8080/get-apt-configs')
      .then((response) => {
        setResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error) => {
        setResult(`Error: ${error.message}`);
      });
  };

  const handleGetSnapConfigs = () => {
    setResult('');
    axios
      .get('http://localhost:8080/get-snap-configs')
      .then((response) => {
        setResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error) => {
        setResult(`Error: ${error.message}`);
      });
  };

  const handleGetJavaConfigs = () => {
    setResult('');
    axios
      .get('http://localhost:8080/get-java-configs')
      .then((response) => {
        setResult(JSON.stringify(response.data, null, 2));
      })
      .catch((error) => {
        setResult(`Error: ${error.message}`);
      });
  };

  return (
    <div className="App">
      <h1>Configuration Retrieval App</h1>
      <button onClick={handleGetAptConfigs}>Get Apt Configs</button>
      <button onClick={handleGetSnapConfigs}>Get Snap Configs</button>
      <button onClick={handleGetJavaConfigs}>Get Java Configs</button>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
