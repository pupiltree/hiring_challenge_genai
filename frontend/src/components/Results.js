import ABTest from './ABTest'; // Import the ABTest component
import { useState } from 'react'; // Import useState

export default function Results({ images, video, onRegenerate }) {
  // State to manage which images are being A/B tested
  const [abTestImages, setAbTestImages] = useState(null);
  const [abTestError, setAbTestError] = useState(null); // State for A/B test errors

  // Function to start A/B testing with two random images
  const startABTest = () => {
    if (images.length < 2) return; // Need at least 2 images for A/B test
    const shuffled = [...images].sort(() => 0.5 - Math.random());
    setAbTestImages(shuffled.slice(0, 2));
    setAbTestError(null); // Clear any previous errors
  };

  // Function to handle A/B test selection
  const handleABTestSelect = async (selectedOption) => {
    try {
      const response = await fetch('/api/ab-test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selectedOption })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to track A/B test selection');
      }

      console.log(`Selected option: ${selectedOption} - Tracked successfully`);
      setAbTestImages(null); // Reset A/B test state after successful tracking
    } catch (err) {
      console.error('Error tracking A/B test:', err);
      setAbTestError(err.message); // Set error state
      // Optionally, keep the A/B test active if tracking fails
      // setAbTestImages(null); // Or reset it
    }
  };

  return (
    <div className="results-container">
      <h2>Generated Ad Variations</h2>
      
      <div className="image-results">
        <h3>Image Ads</h3>
        <div className="image-grid">
          {images.map((img, idx) => (
            <div key={idx} className="image-card">
              <img src={img.url} alt={`Ad variation ${idx+1}`} />
              <a href={img.url} download={`ad-image-${idx+1}.jpg`}>
                Download
              </a>
            </div>
          ))}
        </div>
        {/* Add a button to start A/B testing */}
        {images.length >= 2 && !abTestImages && (
          <button onClick={startABTest}>Start A/B Test</button>
        )}
      </div>
      
      {/* Render the A/B test component if active */}
      {abTestImages && (
        <>
          <ABTest
            imageA={abTestImages[0].url}
            imageB={abTestImages[1].url}
            onSelect={handleABTestSelect}
          />
          {abTestError && <div style={{ color: 'red' }}>Error: {abTestError}</div>}
        </>
      )}
      
      <div className="video-result">
        <h3>Video Ad</h3>
        <video controls src={video.url} />
        <a href={video.url} download="ad-video.mp4">
          Download Video
        </a>
      </div>
      
      <button onClick={onRegenerate}>Generate New Variations</button>
    </div>
  );
} 