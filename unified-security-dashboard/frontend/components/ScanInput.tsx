'use client';
import { useState } from 'react';
import axios from 'axios';

export default function ScanInput({ onScanComplete }: { onScanComplete: (data: any) => void }) {
  const [inputType, setInputType] = useState("git");
  const [value, setValue] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    setLoading(true);
    try {
      if (inputType === "upload" && file) {
        const formData = new FormData();
        formData.append("file", file);
        const uploadRes = await axios.post("http://localhost:5001/api/upload", formData);
        const scanRes = await axios.post("http://localhost:5001/api/scan", {
          type: "upload",
          value: uploadRes.data.filename,
        });
        onScanComplete(scanRes.data);
      } else {
        const scanRes = await axios.post("http://localhost:5001/api/scan", {
          type: inputType,
          value,
        });
        onScanComplete(scanRes.data);
      }
    } catch (err: any) {
      alert("Scan failed: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="mb-6">
      <select
        value={inputType}
        onChange={(e) => setInputType(e.target.value)}
        className="border p-2 mb-2 rounded w-full"
      >
        <option value="git">Git Repository</option>
        <option value="upload">Upload ZIP</option>
        <option value="path">Local Path</option>
      </select>

      {inputType === "upload" ? (
        <input type="file" accept=".zip" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      ) : (
        <input
          type="text"
          className="border p-2 rounded w-full"
          placeholder={
            inputType === "git"
              ? "https://github.com/user/repo.git"
              : "/absolute/path/to/project"
          }
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      )}

      <button
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleScan}
        disabled={loading}
      >
        {loading ? "Scanning..." : "Start Scan"}
      </button>
    </div>
  );
}
