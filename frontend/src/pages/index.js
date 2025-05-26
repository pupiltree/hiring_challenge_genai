import { useState } from 'react';
import AdForm from '../components/AdForm';
import Results from '../components/Results';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setResults(null); // Clear previous results
    
    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Generation failed');
      }
      
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    setResults(null); // Go back to the form
    setError(null);
  };

  return (
    <>
      <div className="header">Ad Variation Generator</div>
      <div className="container">
        <div className="card">
          {error && <div className="error">Error: {error}</div>}
          {isLoading ? (
            <div className="loader">Generating your ads... This may take 1-2 minutes</div>
          ) : results ? (
            <Results images={results.images} video={results.video} onRegenerate={handleRegenerate} />
          ) : (
            <AdForm onSubmit={handleSubmit} />
          )}
        </div>
      </div>
    </>
  );
} 