import React, { useState } from 'react'
import axios from 'axios'

function Body() {
  const [formData, setFormData] = useState({
    product_name: '',
    description: '',
    target_audience: ''
  })
  const [images, setImages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSelected(null)
    try {
      const response = await axios.post('http://localhost:8000/generate-images', formData)
      setImages(response.data.images)
    } catch (err) {
      setError('Failed to generate images. Please try again.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const downloadImage = (imageUrl, index) => {
    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `ad-variation-${index + 1}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleSelect = (index) => {
    setSelected(index)
  }

  return (
    <>
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="product_name">Product Name</label>
            <input
              type="text"
              id="product_name"
              name="product_name"
              value={formData.product_name}
              onChange={handleInputChange}
              required
              placeholder="e.g., Eco Water Bottle"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Product Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              required
              placeholder="Describe your product features and benefits..."
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="target_audience">Target Audience</label>
            <input
              type="text"
              id="target_audience"
              name="target_audience"
              value={formData.target_audience}
              onChange={handleInputChange}
              required
              placeholder="e.g., College students, Young professionals"
            />
          </div>
          
          <button type="submit" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Ad Variations'}
          </button>
        </form>
      </div>

      {error && <div className="error">{error}</div>}
      
      {loading && <div className="loading">Generating your ad variations...</div>}
      
      {images.length > 0 && (
        <>
        <div className="results">
          {images.map((imageUrl, index) => (
            <div key={index} className={`image-card${selected === index ? ' selected' : ''}`}>
              <img src={imageUrl} alt={`Ad variation ${index + 1}`} />
              <div className="card-content">
                <h3>Ad Variation {index + 1}</h3>
                <button 
                  className="download-btn"
                  onClick={() => downloadImage(imageUrl, index)}
                >
                  Download
                </button>
                <button
                  style={{marginLeft: 10, background: selected === index ? '#ffc107' : '#007bff', color: selected === index ? '#333' : '#fff'}}
                  onClick={() => handleSelect(index)}
                  type="button"
                >
                  {selected === index ? 'Selected as Favorite' : 'Select as Favorite'}
                </button>
              </div>
            </div>
          ))}
        </div>
        {selected !== null && (
          <div className="loading" style={{color: '#ffc107', fontWeight: 600, fontSize: 18, marginTop: 20}}>
            You selected <b>Ad Variation {selected + 1}</b> as your favorite!
          </div>
        )}
        </>
      )}
    </>
  )
}

export default Body 