import { useState } from 'react';
import axios from 'axios';
import { Upload, FileType, AlertCircle, CheckCircle2, AlertTriangle, FileUp } from 'lucide-react';
import './App.css';

interface Violation {
  section: string;
  description: string;
  suggestion: string;
}

interface ComplianceReport {
  status: string;
  violations: Violation[];
  approved_elements: string[];
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<ComplianceReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type !== 'application/pdf') {
        setError('Please upload a valid PDF file.');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError(null);
      setReport(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    setLoading(true);
    setError(null);
    setReport(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // In a real scenario, this would point to the deployed Go API URL
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';
      const response = await axios.post(`${API_URL}/api/analyze-plan`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setReport(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred while analyzing the plan. Please make sure the backend services are running.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return 'text-green-600 bg-green-50 border-green-200';
      case 'changes suggested': return 'text-amber-600 bg-amber-50 border-amber-200';
      case 'rejected': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return <CheckCircle2 className="w-6 h-6 text-green-600" />;
      case 'changes suggested': return <AlertTriangle className="w-6 h-6 text-amber-600" />;
      case 'rejected': return <AlertCircle className="w-6 h-6 text-red-600" />;
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            Santa Clara County
          </h1>
          <p className="mt-2 text-xl text-gray-600">
            Building Plan AI Compliance Checker
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white shadow-sm rounded-xl p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                Upload your building plan (PDF) for automated code review
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-xl hover:border-blue-400 transition-colors">
                <div className="space-y-2 text-center">
                  <div className="flex justify-center">
                    {file ? (
                      <FileType className="mx-auto h-12 w-12 text-blue-500" />
                    ) : (
                      <FileUp className="mx-auto h-12 w-12 text-gray-400" />
                    )}
                  </div>
                  <div className="flex text-sm text-gray-600 justify-center">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                    >
                      <span>{file ? 'Change file' : 'Upload a file'}</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        accept=".pdf"
                        className="sr-only"
                        onChange={handleFileChange}
                      />
                    </label>
                  </div>
                  <p className="text-xs text-gray-500">
                    {file ? file.name : 'PDF up to 50MB'}
                  </p>
                </div>
              </div>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 p-4 border border-red-200">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <AlertCircle className="h-5 w-5 text-red-400" aria-hidden="true" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">{error}</h3>
                  </div>
                </div>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={!file || loading}
                className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white ${
                  !file || loading
                    ? 'bg-blue-300 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
                } transition-colors`}
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing Plan...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <Upload className="w-5 h-5 mr-2" />
                    Analyze Plan Compliance
                  </span>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        {report && (
          <div className="bg-white shadow-sm rounded-xl overflow-hidden border border-gray-100 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className={`px-6 py-5 border-b flex items-center space-x-3 ${getStatusColor(report.status)}`}>
              {getStatusIcon(report.status)}
              <h2 className="text-xl font-bold">Status: {report.status}</h2>
            </div>

            <div className="p-6 space-y-8">
              {/* Violations */}
              {report.violations && report.violations.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <AlertTriangle className="w-5 h-5 text-amber-500 mr-2" />
                    Required Changes & Violations
                  </h3>
                  <div className="space-y-4">
                    {report.violations.map((violation, index) => (
                      <div key={index} className="bg-amber-50 border border-amber-200 rounded-lg p-5">
                        <div className="font-semibold text-amber-900 mb-2 font-mono text-sm bg-amber-100 inline-block px-2 py-1 rounded">
                          {violation.section}
                        </div>
                        <p className="text-gray-800 font-medium mb-3">{violation.description}</p>
                        <div className="bg-white bg-opacity-60 rounded p-3 text-sm text-gray-700">
                          <strong>Suggestion:</strong> {violation.suggestion}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Approved Elements */}
              {report.approved_elements && report.approved_elements.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" />
                    Compliant Elements
                  </h3>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {report.approved_elements.map((element, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle2 className="w-5 h-5 text-green-400 mr-2 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{element}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
