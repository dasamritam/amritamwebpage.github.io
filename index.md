---
title: "Welcome to my website!"
layout: home
author_profile: true
classes: wide
---

<!-- Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<style>
.intro-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem 2rem;
  border-radius: 20px;
  margin-bottom: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.intro-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.intro-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.catchy-oneliner {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 1s ease-out;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.info-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #667eea;
  animation: bounceIn 1s ease-out 0.5s both;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #2d3748;
}

.card-content {
  line-height: 1.6;
  color: #4a5568;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .catchy-oneliner {
    font-size: 2rem;
  }
  
  .info-cards {
    grid-template-columns: 1fr;
  }
}

/* Picture frame card style */
.picture-frame-card {
  background: linear-gradient(135deg, #fef5e7 0%, #fed7aa 100%);
  color: #4a5568;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  position: relative;
  max-width: 600px;
  margin: 2rem auto;
  border: 8px solid #d69e2e;
  transform: rotate(-1deg);
}

.picture-frame-card:hover {
  transform: rotate(0deg) translateY(-5px);
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.picture-frame-card::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #d69e2e, #f6ad55, #d69e2e);
  border-radius: 12px;
  z-index: -1;
}

.picture-frame-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #d69e2e;
  animation: bounceIn 1s ease-out 0.5s both;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.picture-frame-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #744210;
  font-family: 'Georgia', serif;
  text-align: center;
}

.picture-frame-content {
  line-height: 1.6;
  color: #4a5568;
  font-size: 1rem;
  font-family: 'Georgia', serif;
  text-align: center;
}
</style>

<div class="intro-section">
  <div class="intro-content">
    <div class="catchy-oneliner">
      <i class="fas fa-rocket" style="margin-right: 1rem; color: #ffd700;"></i>
      Advancing Control Theory for Real-World Impact
    </div>
  </div>
</div>

<div class="info-cards">
  <div class="info-card">
    <div class="card-icon">
      <i class="fas fa-microscope"></i>
    </div>
    <div class="card-title">Research Focus</div>
    <div class="card-content">
      I conduct cutting-edge research in <strong>control theory</strong> and its applications. My expertise spans <strong>Control of PDEs</strong>, <strong>Physics Informed Learning</strong>, <strong>Passivity Theory</strong>, and <strong>Model Reduction</strong>. What excites me most is that control theory, despite being applied mathematics, is always inspired by concrete, real-world applications.
    </div>
  </div>

  <div class="info-card">
    <div class="card-icon">
      <i class="fas fa-graduation-cap"></i>
    </div>
    <div class="card-title">Academic Background</div>
    <div class="card-content">
      I am an <strong>Assistant Professor</strong> at <a href="https://www.tue.nl/en/" style="color: #667eea; text-decoration: none;">Eindhoven University of Technology</a>, part of the Control Systems (CS) group. Previously, I held post-doctoral fellowships at <strong>KTH Royal Institute of Technology</strong>, Sweden and the <strong>University of Cambridge</strong>, UK. I received my <strong>PhD in Electrical Engineering (2020)</strong> and <strong>MSc in Systems & Control (2016)</strong> from TU Eindhoven.
    </div>
  </div>

  <div class="info-card">
    <div class="card-icon">
      <i class="fas fa-cogs"></i>
    </div>
    <div class="card-title">Research Applications</div>
    <div class="card-content">
      My research focuses on <em>designing controllers for complex multi-physical systems</em>. I complement new theories with applications of societal and industrial importance. There are two kinds of applications that I work on, as shown in the thematic depiction of my research below:
    </div>
  </div>
</div>

<div class="picture-frame-card">
  <div class="picture-frame-icon">
    <i class="fas fa-image"></i>
  </div>
  <div class="picture-frame-title">A Personal Note</div>
  <div class="picture-frame-content">
    I am originally from <strong>West Bengal, India</strong>. I feel incredibly privileged growing up with the most diverse culture, profound sense of values, and exceptional cuisine that India has to offer. Outside work, I am passionate about <strong>effective altruism</strong>, <strong>vedic philosophy</strong>, and <strong>backgammon</strong>.
  </div>
</div>
