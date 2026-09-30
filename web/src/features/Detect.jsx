import React, { useState } from 'react';

export default function Detect() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [conf, setConf] = useState(0.25);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleDetect = async () => {
    if (!selectedFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('conf', conf);

    try {
      const response = await fetch('http://localhost:8000/api/detect', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      alert('Có lỗi xảy ra khi gọi API!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Phát hiện đối tượng (Object Detection - YOLO11n)</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      
      <div style={{ marginTop: '10px' }}>
        <label>Độ tin cậy ngưỡng (Confidence Threshold): {conf}</label>
        <input 
          type="range" min="0.1" max="0.9" step="0.05" 
          value={conf} onChange={(e) => setConf(e.target.value)} 
        />
      </div>

      <button onClick={handleDetect} disabled={!selectedFile || loading} style={{ marginTop: '10px' }}>
        {loading ? 'Đang nhận diện...' : 'Phát hiện đối tượng'}
      </button>

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Kết quả ({result.latency_ms} ms):</h3>
          <img src={result.image} alt="Annotated" style={{ maxWidth: '100%', borderRadius: '8px' }} />
          
          <h4>Tóm tắt đối tượng:</h4>
          <ul>
            {Object.entries(result.summary).map(([label, count]) => (
              <li key={label}><strong>{label}</strong>: {count}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}