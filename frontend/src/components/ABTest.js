export default function ABTest({ imageA, imageB, onSelect }) {
  return (
    <div className="ab-test">
      <h3>Which ad do you prefer?</h3>
      <div className="test-options">
        <div className="option" onClick={() => onSelect('A')}>
          <img src={imageA} alt="Option A" />
          <button>Select A</button>
        </div>
        <div className="option" onClick={() => onSelect('B')}>
          <img src={imageB} alt="Option B" />
          <button>Select B</button>
        </div>
      </div>
    </div>
  );
} 