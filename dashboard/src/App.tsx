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

  const API_URL = window.location.origin;

  const fetchData = async () => {
    try {
      const [servicesRes, logsRes, filesRes] = await Promise.all([
        fetch(`${API_URL}/services`),
        fetch(`${API_URL}/logs`),
        fetch(`${API_URL}/files`)
      ]);
      
      if (!servicesRes.ok || !logsRes.ok || !filesRes.ok) throw new Error("Failed to fetch data");
      
      const servicesData = await servicesRes.json();
      const logsData = await logsRes.json();
      const filesData = await filesRes.json();
      
      setServices(servicesData);
      setLogs(logsData);
      setFiles(filesData.files || []);
      setError(null);
    } catch (err) {
      setError("Error connecting to API. Make sure the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 8000);
    return () => clearInterval(interval);
  }, []);

  const handleRestart = async (name: string) => {
    try {
      const res = await fetch(`${API_URL}/services/${name}/restart`, {
        method: 'POST'
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

  return (
    <div className="dashboard">
      <h1>LiteMode Management</h1>
      
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
                    <a href={`${API_URL}/download/${file}`} download className="download-link">Download</a>
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
