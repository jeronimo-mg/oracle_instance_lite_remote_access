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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_URL = `http://${window.location.hostname}:8000`;

  const fetchData = async () => {
    try {
      const [servicesRes, logsRes] = await Promise.all([
        fetch(`${API_URL}/services`),
        fetch(`${API_URL}/logs`)
      ]);
      
      if (!servicesRes.ok || !logsRes.ok) throw new Error("Failed to fetch data");
      
      const servicesData = await servicesRes.json();
      const logsData = await logsRes.json();
      
      setServices(servicesData);
      setLogs(logsData);
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
    const interval = setInterval(fetchData, 5000);
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

  if (loading) return <div className="loading">Loading Dashboard...</div>;

  return (
    <div className="dashboard">
      <h1>LiteMode Management</h1>
      
      {error && <div className="error-banner">{error}</div>}

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
