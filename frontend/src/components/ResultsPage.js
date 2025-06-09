import React from 'react';

function ResultsPage({ data, reset }) {
  const { images, videoUrl } = data;

  return (
    <div>
      <h2>Generated Ad Variations</h2>
      <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>
        {images && images.map((imgUrl, index) => (
          <div key={index} style={{ textAlign: 'center' }}>
            <img src={imgUrl} alt={`Ad Variation ${index + 1}`} width={256} height={256} />
            <div>
              <a href={imgUrl} download={`ad-variation-${index + 1}.png`}>
                Download Image
              </a>
            </div>
          </div>
        ))}
      </div>
      {videoUrl && (
        <div style={{ marginTop: 20 }}>
          <h3>Video Ad</h3>
          <video width="480" height="270" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <div>
            <a href={videoUrl} download="ad-video.mp4">
              Download Video
            </a>
          </div>
        </div>
      )}
      <button onClick={reset} style={{ marginTop: 20, padding: '10px 20px', fontSize: 16 }}>
        Generate New Ads
      </button>
    </div>
  );
}

export default ResultsPage;
