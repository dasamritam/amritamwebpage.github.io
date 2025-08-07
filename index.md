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
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
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

/* Elegant personal note style */
.personal-note {
  text-align: center;
  margin: 3rem auto;
  max-width: 700px;
  position: relative;
  padding: 2rem 0;
}

.personal-note::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  border-radius: 2px;
}

.personal-note::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #764ba2, transparent);
  border-radius: 1px;
}

.personal-note-icon {
  font-size: 1.5rem;
  color: #667eea;
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
  display: inline-block;
}

.personal-note-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-family: 'Georgia', serif;
  letter-spacing: 1px;
  text-transform: uppercase;
  opacity: 0.8;
}

.personal-note-content {
  font-size: 0.95rem;
  line-height: 1.8;
  color: #6b7fa6;
  font-family: 'Georgia', serif;
  font-style: italic;
  position: relative;
  padding: 0 1rem;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.personal-note:hover .personal-note-icon {
  animation: pulse 1s ease-in-out;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
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
      My undergraduate study (2010-2014) was in Mechatronics. My completed both masters (2014-2016) and PhD (2016-2020) in <strong> in Systems & Control </strong> from <a href="https://www.tue.nl/en/" style="color: #667eea; text-decoration: none;">Eindhoven University of Technology</a>. After PhD, I held post-doctoral fellowships at <strong>KTH Royal Institute of Technology</strong>, Sweden and the <strong>University of Cambridge</strong>, UK. 
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

<div class="personal-note">
  <div class="personal-note-icon">
    <i class="fas fa-home"></i>
  </div>
  <div class="personal-note-title">A Personal Note</div>
  <div class="personal-note-content">
    I am originally from <strong>West Bengal, India</strong>. I feel incredibly privileged growing up with the most diverse culture, profound sense of values, and exceptional cuisine that India has to offer. Outside work, I am passionate about <strong>effective altruism</strong>, <strong>vedic philosophy</strong>, and <strong>backgammon</strong>.
  </div>
</div>
