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
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.98) 0%, rgba(58, 74, 71, 0.95) 50%, rgba(37, 46, 44, 0.98) 100%);
  color: white;
  padding: 4rem 3rem;
  border-radius: 25px;
  margin-bottom: 4rem;
  box-shadow: 0 25px 60px rgba(37, 46, 44, 0.4), 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: introFloat 6s ease-in-out infinite;
}

.intro-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(37, 46, 44, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(58, 74, 71, 0.3) 0%, transparent 50%),
    linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.05) 50%, transparent 70%);
  animation: backgroundShift 8s ease-in-out infinite;
}

.intro-section::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.1), transparent, rgba(255, 255, 255, 0.05), transparent);
  animation: rotate 20s linear infinite;
  opacity: 0.3;
}

.intro-content {
  position: relative;
  z-index: 3;
  text-align: center;
}

.catchy-oneliner {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 2.5rem;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(37, 46, 44, 0.3);
  animation: textGlow 4s ease-in-out infinite;
  letter-spacing: 1px;
  line-height: 1.2;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #e8f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.info-card {
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.95) 0%, rgba(58, 74, 71, 0.9) 100%);
  color: #e8f0f0;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(37, 46, 44, 0.3), 0 5px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(37, 46, 44, 0.2);
}

.info-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 25px 50px rgba(37, 46, 44, 0.4), 0 10px 25px rgba(0, 0, 0, 0.3);
  border-color: rgba(37, 46, 44, 0.4);
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #252E2C, #3a4a47, #252E2C);
  background-size: 200% 100%;
  animation: shimmer 3s ease-in-out infinite;
}

.info-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.info-card:hover::after {
  left: 100%;
}

.card-icon {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #252E2C;
  animation: bounceIn 1s ease-out 0.5s both;
  text-shadow: 0 2px 4px rgba(37, 46, 44, 0.3);
  transition: all 0.3s ease;
}

.info-card:hover .card-icon {
  transform: scale(1.1);
  color: #3a4a47;
}

.card-title {
  font-size: 1.6rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: #f8f9fa;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.card-content {
  line-height: 1.7;
  color: #e8f0f0;
  font-size: 0.95rem;
  opacity: 0.9;
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

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes introFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

@keyframes backgroundShift {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes textGlow {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.1); }
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
  background: linear-gradient(90deg, transparent, #252E2C, transparent);
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
  background: linear-gradient(90deg, transparent, #3a4a47, transparent);
  border-radius: 1px;
}

.personal-note-icon {
  font-size: 1.5rem;
  color: #252E2C;
  margin-bottom: 1.5rem;
  animation: float 3s ease-in-out infinite;
  display: inline-block;
  text-shadow: 0 2px 4px rgba(37, 46, 44, 0.3);
}

.personal-note-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #f8f9fa;
  margin-bottom: 1.5rem;
  font-family: 'Georgia', serif;
  letter-spacing: 1px;
  text-transform: uppercase;
  opacity: 0.9;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.personal-note-content {
  font-size: 0.95rem;
  line-height: 1.8;
  color: #e8f0f0;
  font-family: 'Georgia', serif;
  font-style: italic;
  position: relative;
  padding: 0 1rem;
  opacity: 0.9;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.carousel-posts-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 600;
  color: #f8f9fa;
  margin-bottom: 2rem;
  position: relative;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.5px;
}

.carousel-posts-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #252E2C, #3a4a47);
  border-radius: 2px;
}

.carousel-post-title {
  font-size: 1rem;
  font-weight: 600;
  color: #f8f9fa;
  text-decoration: none;
  display: block;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  transition: color 0.3s ease;
}

.carousel-post-title:hover {
  color: #252E2C;
}

.carousel-post-excerpt {
  color: #e8f0f0;
  font-size: 0.85rem;
  line-height: 1.3;
  display: block;
  margin-bottom: 0.3rem;
  opacity: 0.9;
}

.carousel-post-date {
  color: #cbd5e0;
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.2rem 0.5rem;
  background: rgba(37, 46, 44, 0.3);
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(37, 46, 44, 0.2);
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

/* Applications grid styling for home page */
.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.application-item {
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.9) 0%, rgba(58, 74, 71, 0.8) 100%);
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  position: relative;
  overflow: hidden;
}

.application-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.6s ease;
}

.application-item:hover::before {
  left: 100%;
}

.application-item:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 15px 30px rgba(37, 46, 44, 0.4);
  border-color: rgba(255, 255, 255, 0.2);
}

.application-icon {
  font-size: 1.8rem;
  color: #252E2C;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(37, 46, 44, 0.3);
  transition: all 0.3s ease;
}

.application-item:hover .application-icon {
  transform: scale(1.1);
  color: #3a4a47;
}

.application-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f8f9fa;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
</style>

<div class="intro-section">
  <div class="intro-content">
    <div class="catchy-oneliner">
      <i class="fas fa-rocket" style="margin-right: 1rem; color: #252E2C;"></i>
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
    <div class="applications-grid">
      <div class="application-item">
        <div class="application-icon">
          <i class="fas fa-microchip"></i>
        </div>
        <div class="application-name">High-tech systems</div>
      </div>
      
      <div class="application-item">
        <div class="application-icon">
          <i class="fas fa-brain"></i>
        </div>
        <div class="application-name">Neuro-engineering</div>
      </div>
      
      <div class="application-item">
        <div class="application-icon">
          <i class="fas fa-car"></i>
        </div>
        <div class="application-name">Smart mobility</div>
      </div>
      
      <div class="application-item">
        <div class="application-icon">
          <i class="fas fa-atom"></i>
        </div>
        <div class="application-name">Nuclear fusion</div>
      </div>
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
