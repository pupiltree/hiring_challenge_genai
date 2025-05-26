import { useState } from 'react';

export default function AdForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    productName: '',
    description: '',
    audience: 'Young Adults',
    style: 'Modern'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={formData.productName}
        onChange={(e) => setFormData({...formData, productName: e.target.value})}
        placeholder="Product Name"
        required
      />
      <textarea
        value={formData.description}
        onChange={(e) => setFormData({...formData, description: e.target.value})}
        placeholder="Product Description"
        required
      />
      <select 
        value={formData.audience}
        onChange={(e) => setFormData({...formData, audience: e.target.value})}
      >
        <option value="Young Adults">Young Adults</option>
        <option value="Professionals">Professionals</option>
        <option value="Parents">Parents</option>
      </select>
      <button type="submit">Generate Ads</button>
    </form>
  );
} 