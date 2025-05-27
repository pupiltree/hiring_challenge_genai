import React, { useState } from 'react';
import axios from 'axios';

function InputForm({ setGeneratedData, setLoading, setError }) {
  const [productName, setProductName] = useState('');
  const [description, setDescription] = useState('');
  const [targetAudience, setTargetAudience] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setGeneratedData(null);

    try {
      const imageResponse = await axios.post(`/generate-images`, {
        productName,
        description,
        targetAudience,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const videoResponse = await axios.post(`/generate-video`, {
        productName,
        description,
        targetAudience,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      setGeneratedData({
        images: imageResponse.data.images,
        videoUrl: videoResponse.data.videoUrl,
      });
    } catch (error) {
      console.error('Error from backend:', error.response ? error.response.data : error.message);
      setError('Failed to generate ads. Please try again. ' + (error.response ? error.response.data.error : ''));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <label>
        Product Name:
        <input
          type="text"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
          required
          style={{ width: '100%', padding: 8 }}
        />
      </label>
      <label>
        Description:
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          style={{ width: '100%', padding: 8 }}
        />
      </label>
      <label>
        Target Audience:
        <input
          type="text"
          value={targetAudience}
          onChange={(e) => setTargetAudience(e.target.value)}
          required
          style={{ width: '100%', padding: 8 }}
        />
      </label>
      <button type="submit" style={{ padding: 10, fontSize: 16 }}>
        Generate Ads
      </button>
    </form>
  );
}

export default InputForm;
