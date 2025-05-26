const fs = require('fs');
const path = require('path');

const analyticsFile = path.join(__dirname, '../data/analytics.json');

function trackEvent(eventType, adId) {
  const data = fs.existsSync(analyticsFile) 
    ? JSON.parse(fs.readFileSync(analyticsFile))
    : {};
    
  if (!data[eventType]) data[eventType] = {};
  data[eventType][adId] = (data[eventType][adId] || 0) + 1;
  
  fs.writeFileSync(analyticsFile, JSON.stringify(data));
}

function getAnalytics() {
  return fs.existsSync(analyticsFile)
    ? JSON.parse(fs.readFileSync(analyticsFile))
    : {};
}

module.exports = { trackEvent, getAnalytics }; 