---
layout: research
title: "Unlocking the secrets of high-performance in distributed systems"
permalink: /research/
author_profile: true
classes: wide
---

<style>
/* Ultra-sophisticated research page styling */
.research-hero {
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.95) 0%, rgba(58, 74, 71, 0.9) 100%);
  padding: 4rem 3rem;
  border-radius: 25px;
  margin-bottom: 4rem;
  box-shadow: 0 25px 60px rgba(37, 46, 44, 0.4), 0 10px 30px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: researchFloat 8s ease-in-out infinite;
}

.research-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(37, 46, 44, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(58, 74, 71, 0.3) 0%, transparent 50%);
  animation: researchShift 10s ease-in-out infinite;
}

.research-hero::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.05), transparent);
  animation: researchRotate 25s linear infinite;
  opacity: 0.2;
}

.research-content {
  position: relative;
  z-index: 3;
  color: #f8f9fa;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.research-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 2rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #e8f0f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  letter-spacing: 1px;
  animation: titleGlow 4s ease-in-out infinite;
}

.research-description {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 2rem;
  text-align: justify;
  color: #e8f0f0;
  opacity: 0.95;
}



.themes-section {
  margin: 3rem 0;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.8) 0%, rgba(58, 74, 71, 0.7) 100%);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 15px 35px rgba(37, 46, 44, 0.3);
}

.themes-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #f8f9fa;
  margin-bottom: 1.5rem;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

@keyframes researchFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

@keyframes researchShift {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes researchRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes titleGlow {
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.05); }
}

/* Enhanced research grid styling */
.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
  margin: 3rem 0;
}

.research-item {
  background: linear-gradient(145deg, rgba(37, 46, 44, 0.95) 0%, rgba(58, 74, 71, 0.9) 50%, rgba(37, 46, 44, 0.95) 100%);
  padding: 3rem 2.5rem;
  border-radius: 25px;
  text-align: center;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  box-shadow: 
    0 20px 40px rgba(37, 46, 44, 0.4),
    0 8px 16px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.research-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #252E2C, #3a4a47, #667eea, #764ba2, #252E2C);
  background-size: 300% 100%;
  animation: shimmer 4s ease-in-out infinite;
}

.research-item::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.03), transparent);
  animation: researchRotate 30s linear infinite;
  opacity: 0.3;
}

.research-item:hover {
  transform: translateY(-12px) scale(1.03) rotateX(2deg);
  box-shadow: 
    0 35px 70px rgba(37, 46, 44, 0.5),
    0 15px 30px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.research-item:hover::after {
  animation: researchRotate 8s linear infinite;
}

.research-item img {
  max-width: 80%;
  height: auto;
  margin-bottom: 2rem;
  border-radius: 15px;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.3),
    0 5px 15px rgba(37, 46, 44, 0.2);
  filter: brightness(0.9) contrast(1.1);
}

.research-item:hover img {
  transform: scale(1.08) translateY(-5px);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.4),
    0 10px 25px rgba(37, 46, 44, 0.3);
  filter: brightness(1.1) contrast(1.2);
}

.research-item h3 {
  color: #f8f9fa !important;
  font-style: italic;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-shadow: 0 3px 6px rgba(0, 0, 0, 0.4);
  transition: all 0.4s ease;
  letter-spacing: 0.5px;
  position: relative;
}

.research-item h3::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #00adb5, #393e46);
  transition: width 0.4s ease;
  border-radius: 1px;
}

.research-item:hover h3::after {
  width: 60px;
}

.research-item:hover h3 {
  color: #ffffff !important;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  transform: scale(1.02);
}

.research-item p {
  color: #e8f0f0 !important;
  font-size: 1rem;
  line-height: 1.7;
  opacity: 0.9;
  margin-bottom: 1.5rem;
  font-weight: 400;
  transition: all 0.3s ease;
}

.research-item:hover p {
  opacity: 1;
  color: #f8f9fa !important;
}

.research-item .details {
  color: #cbd5e0 !important;
  font-size: 0.9rem;
  line-height: 1.6;
  opacity: 0.8;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(37, 46, 44, 0.4) 0%, rgba(58, 74, 71, 0.3) 100%);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  transform: translateY(10px);
  opacity: 0;
  max-height: 0;
  overflow: hidden;
}

.research-item .details.show {
  opacity: 1;
  transform: translateY(0);
  max-height: 500px;
}

/* Unique floating animation for research cards */
@keyframes researchFloat {
  0%, 100% { transform: translateY(0px) rotateX(0deg); }
  50% { transform: translateY(-8px) rotateX(1deg); }
}

.research-item {
  animation: researchFloat 6s ease-in-out infinite;
}

.research-item:nth-child(2) {
  animation-delay: 1.5s;
}

.research-item:nth-child(3) {
  animation-delay: 3s;
}

.research-item:nth-child(4) {
  animation-delay: 4.5s;
}

/* Enhanced shimmer effect */
@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Particle effect for research cards */
.research-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #252E2C, #3a4a47, #00adb5, #393e46, #252E2C);
  background-size: 300% 100%;
  animation: shimmer 4s ease-in-out infinite;
}



/* Glow effect on hover */
.research-item:hover {
  box-shadow: 
    0 35px 70px rgba(37, 46, 44, 0.5),
    0 15px 30px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 173, 181, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}
</style>

<div class="research-hero">
  <div class="research-content">
    <h1 class="research-title">{{ page.title }}</h1>
    
    <div class="research-description">
      My research seeks answer to the question: <em>How can we combine known invariants with real-world data to guarantee the best performance of physical systems?</em> My focus is on dynamical systems where behaviors emerge from vast networks of interacting objects spread across different locations. These behaviors are driven by partial integro-differential equations equations that are tough to solve, and observing them is often limited by budget constraints on sensors and their placements.
    </div>
    
    <div class="research-description">
      To tackle these challenges, I develop powerful computational tools grounded on optimization, control theory, and machine learning.
    </div>
  </div>
</div>

<div class="themes-section">
  <h2 class="themes-title">Current research themes in our lab:</h2>
</div>

<!-- Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
