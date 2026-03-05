import { useState, useEffect } from 'react'
import './App.css'

interface ServiceStatus {
  [key: string]: string;
}

interface LogEntry {
  id: number;
  timestamp: string;
  service_name: string;
  message: string;
}

function App() {
  const [services, setServices] = useState<ServiceStatus>({});
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [passwordInput, setPasswordInput] = useState('');
  const [authKey, setAuthKey] = useState<string | null>(localStorage.getItem('dashboard_key'));

  const API_URL = window.location.origin;

  const fetchData = async () => {
    if (!authKey) {
      setLoading(false);
      return;
    }

    try {
      const headers = { 'X-Dashboard-Key': authKey };
      const [servicesRes, logsRes, filesRes] = await Promise.all([
        fetch(`${API_URL}/services`, { headers }),
        fetch(`${API_URL}/logs`, { headers }),
        fetch(`${API_URL}/files`, { headers })
      ]);
      
      if (servicesRes.status === 401) {
        handleLogout();
        return;
      }

      if (!servicesRes.ok || !logsRes.ok || !filesRes.ok) throw new Error("Failed to fetch data");
      
      const servicesData = await servicesRes.json();
      const logsData = await logsRes.json();
      const filesData = await filesRes.json();
      
      setServices(servicesData);
      setLogs(logsData);
      setFiles(filesData.files || []);
      setError(null);
      setIsAuthenticated(true);
    } catch (err) {
      setError("Error connecting to API. Make sure the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      if (authKey) fetchData();
    }, 8000);
    return () => clearInterval(interval);
  }, [authKey]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: passwordInput })
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('dashboard_key', data.token);
        setAuthKey(data.token);
        setIsAuthenticated(true);
        setPasswordInput('');
      } else {
        alert("Senha incorreta");
      }
    } catch (err) {
      alert("Erro ao conectar com o servidor");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('dashboard_key');
    setAuthKey(null);
    setIsAuthenticated(false);
  };

  const handleRestart = async (name: string) => {
    try {
      const res = await fetch(`${API_URL}/services/${name}/restart`, {
        method: 'POST',
        headers: { 'X-Dashboard-Key': authKey || '' }
      });
      if (!res.ok) throw new Error("Restart failed");
      alert(`${name} restart initiated`);
      fetchData();
    } catch (err) {
      alert(`Error restarting ${name}`);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        headers: { 'X-Dashboard-Key': authKey || '' },
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      fetchData();
    } catch (err) {
      alert("Error uploading file");
    } finally {
      setUploading(false);
    }
  };

  if (loading) return <div className="loading">Loading Dashboard...</div>;

  if (!isAuthenticated) {
    return (
      <div className="login-container">
        <form className="login-form" onSubmit={handleLogin}>
          <h1>LiteMode Access</h1>
          <p>Please enter the dashboard password</p>
          <input 
            type="password" 
            placeholder="Password" 
            value={passwordInput}
            onChange={(e) => setPasswordInput(e.target.value)}
            required
          />
          <button type="submit">Unlock Dashboard</button>
        </form>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dash-header">
        <h1>LiteMode Management</h1>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </header>
      
      {error && <div className="error-banner">{error}</div>}

      <div className="main-grid">
        <section className="services">
          <h2>System Services</h2>
          <div className="service-grid">
            {Object.entries(services).map(([name, status]) => (
              <div key={name} className={`service-card ${status}`}>
                <h3>{name}</h3>
                <p>Status: <strong>{status}</strong></p>
                <button onClick={() => handleRestart(name)}>Restart</button>
              </div>
            ))}
          </div>
        </section>

        <section className="files">
          <h2>File Transfer</h2>
          <div className="file-box">
            <input 
              type="file" 
              id="file-upload" 
              onChange={handleFileUpload} 
              disabled={uploading}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-upload" className="upload-btn">
              {uploading ? "Uploading..." : "Upload New File"}
            </label>

            <ul className="file-list">
              {files.length === 0 ? <p>No files uploaded yet.</p> : 
                files.map(file => (
                  <li key={file}>
                    <span>{file}</span>
                    <a 
                      href={`${API_URL}/download/${file}?x-dashboard-key=${authKey}`} 
                      onClick={async (e) => {
                         e.preventDefault();
                         const response = await fetch(`${API_URL}/download/${file}`, {
                           headers: { 'X-Dashboard-Key': authKey || '' }
                         });
                         const blob = await response.blob();
                         const url = window.URL.createObjectURL(blob);
                         const a = document.createElement('a');
                         a.href = url;
                         a.download = file;
                         a.click();
                      }}
                      className="download-link"
                    >Download</a>
                  </li>
                ))
              }
            </ul>
          </div>
        </section>
      </div>

      <section className="logs">
        <h2>Activity Logs</h2>
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Service</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
                <td>{log.service_name}</td>
                <td>{log.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  )
}

export default App

