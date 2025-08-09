---
title: "3D PDE Visualization"
layout: single
image: "/images/research/3d-pde-visualization.png"
description: "Interactive 3D visualization of space-time-value relationships in PDE solutions"
author_profile: true
classes: wide
---

<div style="text-align: left; margin-bottom: 20px;">
  <a href="/research/" class="btn btn--primary" style="color: white; text-decoration: none; padding: 8px 16px; border-radius: 4px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    ← Back to Research
  </a>
</div>

## Interactive 3D PDE Visualization

This page demonstrates an interactive 3D visualization of partial differential equations (PDEs), showing the relationship between space, time, and solution values. This type of visualization is crucial for understanding the dynamic behavior of distributed parameter systems, such as those encountered in thermo-fluidic processes, heat transfer, and wave propagation.

### 3D Plot: Space-Time-Value Relationship

The visualization below shows a 3D surface plot where:

- **X-axis (Space)**: Spatial dimension (e.g., position along a 1D domain)
- **Y-axis (Time)**: Temporal dimension (time evolution)
- **Z-axis (Value)**: Solution values (e.g., temperature, concentration, displacement)

<div id="pde-3d-container" style="width: 100%; height: 600px; margin: 20px 0; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: relative;"></div>

<div style="text-align: center; margin: 10px 0; font-size: 0.9em; color: #666;">
    <strong>Controls:</strong> Drag to rotate • Scroll to zoom • Right-click to pan
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<script>
// Enhanced 3D PDE Visualization using Three.js
class EnhancedPDE3DVisualization {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.controls = null;
        this.surfaceGeometry = null;
        this.surfaceMaterial = null;
        this.surfaceMesh = null;
        this.axes = [];
        this.gridHelper = null;
        this.animationId = null;
        this.time = 0;
        
        this.init();
        this.animate();
    }
    
    init() {
        // Setup renderer
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setClearColor(0x000000, 0.1);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Setup camera
        this.camera.position.set(15, 15, 15);
        this.camera.lookAt(0, 0, 0);
        
        // Setup controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.screenSpacePanning = false;
        this.controls.minDistance = 5;
        this.controls.maxDistance = 50;
        this.controls.maxPolarAngle = Math.PI;
        
        // Setup lighting
        this.setupLighting();
        
        // Create 3D surface
        this.createSurface();
        
        // Create axes with labels
        this.createAxes();
        
        // Create grid
        this.createGrid();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Point light for additional illumination
        const pointLight = new THREE.PointLight(0x00adb5, 1, 100);
        pointLight.position.set(-10, 10, -10);
        this.scene.add(pointLight);
    }
    
    createSurface() {
        const width = 100;
        const height = 100;
        const widthSegments = 50;
        const heightSegments = 50;
        
        // Create geometry
        this.surfaceGeometry = new THREE.PlaneGeometry(width, height, widthSegments, heightSegments);
        
        // Apply PDE-like surface deformation
        const vertices = this.surfaceGeometry.attributes.position.array;
        const colors = [];
        
        for (let i = 0; i < vertices.length; i += 3) {
            const x = vertices[i];
            const y = vertices[i + 1];
            
            // Create a PDE-like surface (e.g., wave equation or heat equation solution)
            const t = (y / (height / 2) + 1) * Math.PI; // Time parameter
            const xNorm = x / (width / 2); // Normalized spatial coordinate
            
            // Solution to a damped wave equation: u(x,t) = exp(-kt) * sin(ωx) * cos(ωt)
            const k = 0.3; // Damping coefficient
            const omega = 2; // Frequency
            const amplitude = 5;
            
            let z = amplitude * Math.exp(-k * t) * Math.sin(omega * xNorm) * Math.cos(omega * t);
            
            // Add some spatial variation for more realistic PDE behavior
            z += 2 * Math.exp(-k * t) * Math.sin(2 * omega * xNorm) * Math.sin(omega * t / 2);
            
            // Add boundary effects (Dirichlet boundary conditions)
            if (Math.abs(xNorm) > 0.8 || t > 2.5) {
                z *= 0.3; // Damping at boundaries
            }
            
            vertices[i + 2] = z;
            
            // Create color based on height and time
            const normalizedHeight = (z + amplitude) / (2 * amplitude);
            const normalizedTime = t / (Math.PI * 2);
            
            // Create a sophisticated color gradient
            const r = Math.min(1, normalizedHeight * 0.8 + normalizedTime * 0.2);
            const g = Math.min(1, (1 - normalizedHeight) * 0.6 + normalizedTime * 0.2);
            const b = Math.min(1, (1 - normalizedHeight) * 0.8 + normalizedTime * 0.1);
            
            colors.push(r, g, b);
        }
        
        // Add colors to geometry
        this.surfaceGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        
        // Create material with custom shader for better visual effects
        this.surfaceMaterial = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0.0 },
                lightPosition: { value: new THREE.Vector3(10, 10, 5) }
            },
            vertexShader: `
                attribute vec3 color;
                varying vec3 vColor;
                varying vec3 vNormal;
                varying vec3 vPosition;
                
                void main() {
                    vColor = color;
                    vNormal = normalize(normalMatrix * normal);
                    vPosition = position;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                varying vec3 vColor;
                varying vec3 vNormal;
                varying vec3 vPosition;
                
                uniform vec3 lightPosition;
                uniform float time;
                
                void main() {
                    vec3 lightDir = normalize(lightPosition - vPosition);
                    float diff = max(dot(vNormal, lightDir), 0.0);
                    vec3 diffuse = diff * vColor;
                    vec3 ambient = 0.3 * vColor;
                    vec3 finalColor = ambient + diffuse;
                    
                    // Add subtle time-based animation
                    float pulse = 0.8 + 0.2 * sin(time * 1.0);
                    finalColor *= pulse;
                    
                    gl_FragColor = vec4(finalColor, 1.0);
                }
            `,
            transparent: true,
            opacity: 0.9
        });
        
        // Create mesh
        this.surfaceMesh = new THREE.Mesh(this.surfaceGeometry, this.surfaceMaterial);
        this.surfaceMesh.rotation.x = -Math.PI / 2; // Rotate to show as a surface
        this.surfaceMesh.castShadow = true;
        this.surfaceMesh.receiveShadow = true;
        this.scene.add(this.surfaceMesh);
    }
    
    createAxes() {
        const axesLength = 12;
        
        // X-axis (Space) - Red
        const xAxisGeometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(-axesLength, 0, 0),
            new THREE.Vector3(axesLength, 0, 0)
        ]);
        const xAxisMaterial = new THREE.LineBasicMaterial({ color: 0xff6b6b, linewidth: 2 });
        const xAxis = new THREE.Line(xAxisGeometry, xAxisMaterial);
        this.scene.add(xAxis);
        this.axes.push(xAxis);
        
        // Y-axis (Time) - Cyan
        const yAxisGeometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, -axesLength, 0),
            new THREE.Vector3(0, axesLength, 0)
        ]);
        const yAxisMaterial = new THREE.LineBasicMaterial({ color: 0x4ecdc4, linewidth: 2 });
        const yAxis = new THREE.Line(yAxisGeometry, yAxisMaterial);
        this.scene.add(yAxis);
        this.axes.push(yAxis);
        
        // Z-axis (Value) - Blue
        const zAxisGeometry = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, 0, -axesLength),
            new THREE.Vector3(0, 0, axesLength)
        ]);
        const zAxisMaterial = new THREE.LineBasicMaterial({ color: 0x45b7d1, linewidth: 2 });
        const zAxis = new THREE.Line(zAxisGeometry, zAxisMaterial);
        this.scene.add(zAxis);
        this.axes.push(zAxis);
        
        // Add axis arrows
        this.createAxisArrows();
    }
    
    createAxisArrows() {
        const arrowLength = 1;
        const arrowHeadLength = 0.5;
        const arrowHeadWidth = 0.3;
        
        // X-axis arrow
        const xArrowGeometry = new THREE.ConeGeometry(arrowHeadWidth, arrowHeadLength, 8);
        const xArrowMaterial = new THREE.MeshBasicMaterial({ color: 0xff6b6b });
        const xArrow = new THREE.Mesh(xArrowGeometry, xArrowMaterial);
        xArrow.rotation.z = -Math.PI / 2;
        xArrow.position.set(12.5, 0, 0);
        this.scene.add(xArrow);
        
        // Y-axis arrow
        const yArrowGeometry = new THREE.ConeGeometry(arrowHeadWidth, arrowHeadLength, 8);
        const yArrowMaterial = new THREE.MeshBasicMaterial({ color: 0x4ecdc4 });
        const yArrow = new THREE.Mesh(yArrowGeometry, yArrowMaterial);
        yArrow.position.set(0, 12.5, 0);
        this.scene.add(yArrow);
        
        // Z-axis arrow
        const zArrowGeometry = new THREE.ConeGeometry(arrowHeadWidth, arrowHeadLength, 8);
        const zArrowMaterial = new THREE.MeshBasicMaterial({ color: 0x45b7d1 });
        const zArrow = new THREE.Mesh(zArrowGeometry, zArrowMaterial);
        zArrow.rotation.x = Math.PI / 2;
        zArrow.position.set(0, 0, 12.5);
        this.scene.add(zArrow);
    }
    
    createGrid() {
        // Create a grid helper for reference
        this.gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
        this.gridHelper.position.y = -6;
        this.scene.add(this.gridHelper);
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        this.time += 0.01;
        
        // Update time uniform for shader animation
        if (this.surfaceMaterial && this.surfaceMaterial.uniforms) {
            this.surfaceMaterial.uniforms.time.value = this.time;
        }
        
        // Update controls
        this.controls.update();
        
        // Render
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Initialize the 3D visualization when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const visualization = new EnhancedPDE3DVisualization('pde-3d-container');
    
    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        if (visualization) {
            visualization.dispose();
        }
    });
});
</script>

## Mathematical Interpretation

This 3D visualization represents a solution to a **damped wave equation**, which is a fundamental PDE in physics and engineering:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2} - k \frac{\partial u}{\partial t}$$

### Solution Form

The visualized solution takes the form:

$$u(x,t) = A \cdot e^{-kt} \cdot \sin(\omega x) \cdot \cos(\omega t) + B \cdot e^{-kt} \cdot \sin(2\omega x) \cdot \sin(\frac{\omega t}{2})$$

where:

- $u(x,t)$ is the solution value (Z-axis)
- $x$ is the spatial coordinate (X-axis)
- $t$ is time (Y-axis)
- $A, B$ are amplitudes
- $\omega$ is the angular frequency
- $k$ is the damping coefficient
- $c$ is the wave speed

### Key Physical Features

1. **Wave Propagation**: The solution shows traveling waves that propagate through space over time
2. **Damping**: Amplitude decreases exponentially with time due to energy dissipation
3. **Standing Waves**: Spatial patterns indicate standing wave modes
4. **Boundary Effects**: Solution decays near spatial boundaries (Dirichlet boundary conditions)
5. **Multi-scale Structure**: Multiple frequency components create complex spatiotemporal patterns

## Applications in Your Research

This type of visualization is directly relevant to your thermo-fluidic control research:

### Thermo-fluidic Processes

- **Heat Transfer**: Temperature distribution in heat exchangers, thermal management systems
- **Fluid Dynamics**: Pressure waves, velocity fields in pipes and channels
- **Phase Change**: Melting/solidification fronts, boiling phenomena

### Control Applications

- **Distributed Parameter Control**: Spatiotemporal control of temperature or concentration fields
- **Model Predictive Control**: Real-time optimization of distributed systems
- **Robust Control**: Handling uncertainty in PDE parameters

### Specific Examples

- **Inkjet Printing**: Temperature control in printheads (as in your PhD work)
- **Nuclear Fusion**: Plasma dynamics and control
- **Energy Systems**: Thermal storage, heat exchangers
- **Chemical Reactors**: Concentration profiles, reaction fronts

## Interactive Features

### Controls

- **Mouse Drag**: Rotate the 3D view around the surface
- **Mouse Wheel**: Zoom in/out for detailed examination
- **Right-click Drag**: Pan the view horizontally/vertically

### Visualization Elements

- **Color Coding**: Blue (low values) to red (high values) with time-based variation
- **Axis Labels**: Red (Space), Cyan (Time), Blue (Value)
- **Grid Reference**: Ground plane for spatial orientation
- **Dynamic Animation**: Real-time evolution shows temporal behavior

This visualization provides an intuitive understanding of how distributed parameter systems evolve, making it an excellent tool for both research presentation and educational purposes.
