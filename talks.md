---
layout: archive
title: "Talks"
permalink: /talks/
author_profile: true
classes: wide
---

### PhD Defense Talk

- _Digital twin for controlling thermo-fluidic processes._\
  TU Eindhoven, Eindhoven, the Netherlands, November 2020. [[Slides](/files/Slides/Slides-phd.pdf)][[Video](https://www.youtube.com/watch?v=h9y8sntrbBI)]

### Invited Seminars

- _Ode to +/- signs in feedback control._\
  CS Group, TU Eindhoven, Eindhoven, the Netherlands, July 2022. [[Slides](/files/Slides/Slides-tue.pdf)]
- _Keeping feedback in neural networks._\
  Pappas Group, University of Pennsylvania, Philadelphia, USA, April 2021. [[Slides](/files/Slides/Slides-upenn.pdf)]
- _Digital twin for industrial processes._\
  Control Group, University of Cambridge, Cambridge, UK, November 2020. [[Video](https://www.youtube.com/watch?v=za0Q_whXYRI)]
- _Analysis and control of networked infinite-dimensional systems._\
  Max Planck Institute for Dynamics of Complex Technical Systems, Magdeburg, Germany, March 2020. [[Slides](/files/Slides/Slides-mpi.pdf)]
- _Controlling thermal effects in DoD inkjet printhead._\
  ASML N.V., Veldhoven, The Netherlands, November 2019. [[Slides](/files/Slides/Slides-thermQ.pdf)]
- _Thermo-fluidic processes in spatially interconnected structures._\
  Canon Production Printing B.V., Venlo, The Netherlands, October 2018. [[Slides](/files/Slides/Slides-cpp.pdf)]

### Conference Presentations

- _Learning Flows of Control Systems._\
  c3.ai DTI Workshop on Data, Learning, and Markets, Urbana, USA, October 2022. [[Poster](/files/Slides/DTI_Poster_Amritam_.pdf)]
- _Splitting algorithm for i/o analysis of negative resistance circuits._\
  Reglermöte'22, Luleå, Sweden, June 2022. [[Slides](/files/Slides/Slides-ltu.pdf)]
- _Robust analysis of uncertain ODE-PDE systems using PIEs._\
  CDC'20, Jeju Island, South Korea, December 2020. [[Slides](/files/Slides/Slides-jeju.pdf)]
- _H∞ optimal estimation of linear coupled PDE systems._\
  CDC'19, Nice, France, December 2019. [[Slides](/files/Slides/Slides-nice.pdf)]
- _Sensorless field-oriented estimation of hybrid stepper motors in high-performance paper handling._\
  CCTA'19, City of Hong Kong, Hong Kong, August 2019. [[Slides](/files/Slides/Slides-ccta.pdf)]
- _Frequency domain estimation of spatially varying parameters in heat and mass transport._\
  ACC'19, Philadelphia, USA, July 2019. [[Slides](/files/Slides/Slides-acc.pdf)]
- _Model approximation of thermo-fluidic diffusion processes in spatially interconnected structures._\
  ECC'18, Limassol, Cyprus, June 2018. [[Slides](/files/Slides/Slides-ecc.pdf)]
- _Optimal trajectory tracking control for automated guided Vehicles._\
  IFAC World Congress'17, Toulouse, France, July 2017. [[Slides](/files/Slides/Slides-ifac17.pdf)][[Poster](/files/Slides/Poster-ifac17.pdf)]

## Talk Locations Map

       <div id="talk-map" style="height: 400px; width: 100%; margin: 20px 0;"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
// Talk locations data
const talkLocations = [
    {
        name: "PhD Defense Talk",
        location: "TU Eindhoven, Eindhoven, the Netherlands",
        coords: [51.4416, 5.4697],
        date: "November 2020",
        type: "PhD Defense"
    },
    {
        name: "Ode to +/- signs in feedback control",
        location: "TU Eindhoven, Eindhoven, the Netherlands",
        coords: [51.4416, 5.4697],
        date: "July 2022",
        type: "Invited Seminar"
    },
    {
        name: "Keeping feedback in neural networks",
        location: "University of Pennsylvania, Philadelphia, USA",
        coords: [39.9526, -75.1652],
        date: "April 2021",
        type: "Invited Seminar"
    },
    {
        name: "Digital twin for industrial processes",
        location: "University of Cambridge, Cambridge, UK",
        coords: [52.2053, 0.1218],
        date: "November 2020",
        type: "Invited Seminar"
    },
    {
        name: "Analysis and control of networked infinite-dimensional systems",
        location: "Max Planck Institute, Magdeburg, Germany",
        coords: [52.1205, 11.6276],
        date: "March 2020",
        type: "Invited Seminar"
    },
    {
        name: "Controlling thermal effects in DoD inkjet printhead",
        location: "ASML N.V., Veldhoven, The Netherlands",
        coords: [51.4208, 5.4097],
        date: "November 2019",
        type: "Invited Seminar"
    },
    {
        name: "Thermo-fluidic processes in spatially interconnected structures",
        location: "Canon Production Printing B.V., Venlo, The Netherlands",
        coords: [51.3703, 6.1724],
        date: "October 2018",
        type: "Invited Seminar"
    },
    {
        name: "Learning Flows of Control Systems",
        location: "c3.ai DTI Workshop, Urbana, USA",
        coords: [40.1106, -88.2073],
        date: "October 2022",
        type: "Conference"
    },
    {
        name: "Splitting algorithm for i/o analysis of negative resistance circuits",
        location: "Reglermöte'22, Luleå, Sweden",
        coords: [65.5848, 22.1567],
        date: "June 2022",
        type: "Conference"
    },
    {
        name: "Robust analysis of uncertain ODE-PDE systems using PIEs",
        location: "CDC'20, Jeju Island, South Korea",
        coords: [33.4996, 126.5312],
        date: "December 2020",
        type: "Conference"
    },
    {
        name: "H∞ optimal estimation of linear coupled PDE systems",
        location: "CDC'19, Nice, France",
        coords: [43.7102, 7.2620],
        date: "December 2019",
        type: "Conference"
    },
    {
        name: "Sensorless field-oriented estimation of hybrid stepper motors",
        location: "CCTA'19, Hong Kong",
        coords: [22.3193, 114.1694],
        date: "August 2019",
        type: "Conference"
    },
    {
        name: "Frequency domain estimation of spatially varying parameters",
        location: "ACC'19, Philadelphia, USA",
        coords: [39.9526, -75.1652],
        date: "July 2019",
        type: "Conference"
    },
    {
        name: "Model approximation of thermo-fluidic diffusion processes",
        location: "ECC'18, Limassol, Cyprus",
        coords: [34.7071, 33.0226],
        date: "June 2018",
        type: "Conference"
    },
    {
        name: "Optimal trajectory tracking control for automated guided Vehicles",
        location: "IFAC World Congress'17, Toulouse, France",
        coords: [43.6047, 1.4442],
        date: "July 2017",
        type: "Conference"
    }
];

// Initialize map
const map = L.map('talk-map').setView([30, 0], 2);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Color coding for different talk types
const colors = {
    'PhD Defense': '#e74c3c',
    'Invited Seminar': '#3498db',
    'Conference': '#2ecc71'
};

// Add markers for each talk location
talkLocations.forEach(talk => {
    const marker = L.marker(talk.coords).addTo(map);
    
    const popupContent = `
        <div style="min-width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #333;">${talk.name}</h4>
            <p style="margin: 4px 0; color: #666;"><strong>Location:</strong> ${talk.location}</p>
            <p style="margin: 4px 0; color: #666;"><strong>Date:</strong> ${talk.date}</p>
            <p style="margin: 4px 0; color: #666;"><strong>Type:</strong> ${talk.type}</p>
        </div>
    `;
    
    marker.bindPopup(popupContent);
    
    // Color code the markers
               const icon = L.divIcon({
               className: 'custom-div-icon',
               html: `<div style="background-color: ${colors[talk.type]}; width: 18px; height: 18px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 4px rgba(0,0,0,0.3);"></div>`,
               iconSize: [18, 18],
               iconAnchor: [9, 9]
           });
    
    marker.setIcon(icon);
});

// Add legend
const legend = L.control({position: 'bottomright'});
legend.onAdd = function(map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.style.backgroundColor = 'white';
    div.style.padding = '10px';
    div.style.borderRadius = '5px';
    div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
    div.innerHTML = `
        <h4 style="margin: 0 0 8px 0;">Talk Types</h4>
                       <div style="display: flex; align-items: center; margin: 4px 0;">
                   <div style="background-color: ${colors['PhD Defense']}; width: 18px; height: 18px; border-radius: 50%; margin-right: 8px;"></div>
                   <span>PhD Defense</span>
               </div>
               <div style="display: flex; align-items: center; margin: 4px 0;">
                   <div style="background-color: ${colors['Invited Seminar']}; width: 18px; height: 18px; border-radius: 50%; margin-right: 8px;"></div>
                   <span>Invited Seminar</span>
               </div>
               <div style="display: flex; align-items: center; margin: 4px 0;">
                   <div style="background-color: ${colors['Conference']}; width: 18px; height: 18px; border-radius: 50%; margin-right: 8px;"></div>
                   <span>Conference</span>
               </div>
    `;
    return div;
};
legend.addTo(map);
</script>
