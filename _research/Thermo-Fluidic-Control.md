---
title: "Control of PDEs"
layout: single
image: "/images/research/sub-theme-pde.png"
description: "discretization-independent control of multi-physics processes"
author_profile: true
classes: wide
---

<img src="/images/research/sub-theme-pde.png" alt="sub-theme-pde" width="450" style="display: block; margin: 0 auto"/>

## Collaborators

- [prof. Siep Weiland](https://scholar.google.nl/citations?user=y2DLux4AAAAJ&hl=nl), TU Eindhoven
- [dr. Matthew Peet](https://scholar.google.com/citations?user=l7umOqMAAAAJ&hl=en), Arizona State University
- [dr. Matthijs van Berkel](https://scholar.google.com/citations?user=xhmEKnIAAAAJ&hl=en), Dutch Institute for Fundamental Energy Research

## Summary

Digital twin is a computer-aided platform that virtually represents
an industrial asset for emulating its conception, mechanism, usage and life
cycle. I develop
a digital twin that represents assets exhibiting thermo-fluidic processes and synthesizes controllers
for them to achieve desirable performance. The thermo-fluidic processes are
defined by the interaction of solids and fluids under the influence of external
thermal energy. These processes involve physical quantities that dynamically
vary over time, as well as over space. My research focus is twoards building industrial-scale digital twins for engineering assets governed by thermo-fluidic processes. My research has established a new theory,
computational techniques, and software tools that prescribes strategies to be implemented on the asset for achieving a predefined performance without
adding addtional sensors or actuators.
{: style="text-align: justify;"}

I designate the digital twin with four key attributes:

1. _Flexibility:_ At any stage, in a digital twin of the
   physical asset should be flexible so that a user can make
   adjustments on it at any stage of the development cycle.
   {: style="text-align: justify;"}
2. _Versatility:_ As the functionalities of a digital twin are quite diverse, it has to
   be versatile accommodating all the functionalities under software tool that
   the digital twin represents.
   {: style="text-align: justify;"}
3. _Modularity:_ The digital twin has to be modular so that, in future, when a new
   component or service is added to the physical asset or process, the digital
   twin is modular to adapt its architecture accordingly.
   {: style="text-align: justify;"}
4. _Integrebility:_ A digital twin that is dedicated to
   a specific asset or process has to be meaningfully integrable to the
   industry’s entire operational pipeline.
   {: style="text-align: justify;"}

This is particularly difficult since thermo-fluidic processes are multi-physical and hard to control. You can find more about such a digital twin in my PhD thesis.
{: style="text-align: justify;"}

### PhD Thesis

[Thesis](https://research.tue.nl/en/publications/a-digital-twin-for-controlling-thermo-fluidic-processes){: .btn--research} [Software](http://control.asu.edu/pietools/){: .btn--research} [Public Presentation](https://www.youtube.com/watch?v=h9y8sntrbBI){: .btn--research}

> Executive Summary: A digital twin brings an industrial asset out of the laboratory’s four walls and
> put it on a computer as a piece of software. As a result, throughout its entire life
> cycle, procedures of design, analysis, prediction, diagnosis and monitoring can be
> performed virtually without the asset’s physical form. How do we develop such a
> digital twin for assets that are governed by thermo-fluidic processes and guarantee
> that the asset achieves the desired performance?
> {: style="text-align: justify;"}

## Theory

Since thermo-fluidic processes are hard to control, my research focuses on three theoretical directions as shown in the figure below.
{: style="text-align: justify;"}

<img src="/images/research/threeways-pde.png" alt="threeways-pde" width="420" style="display: block; margin: 0 auto"/>

These directions differ from each other based on whether approximation is required to build a computational framework on thermo-fluidic processes. Furthermore, even if approximation is unavoidable, at what stage we need that. A representive paper of my research can be found below:
{: style="text-align: justify;"}

[Paper](https://ieeexplore.ieee.org/abstract/document/9303892){: .btn--research}

> Abstract: This paper presents a computational framework for analyzing stability and performance of uncertain Partial Differential Equations (PDEs) when they are coupled with uncertain Ordinary Differential Equations (ODEs). To analyze the behavior of the interconnected ODE-PDE systems under uncertainty, we introduce a class of multipliers of Partial Integral (PI) operator type and consider various classes of uncertainties by enforcing constraints on these multipliers. Since the ODE-PDE models are equivalent to Partial Integral Equations (PIEs), we show that the robust stability and performance can be formulated as Linear PI Inequalities (LPIs) and LPIs can be solved by LMIs using PIETOOLS. The methods are demonstrated on examples of ODE-PDE systems that are subjected to wide classes of uncertainty.
> {: style="text-align: justify;"}

## Application to High-Tech Systems

My research, so far, has focused on applications related to high-tech industries such as inkjet printing, lithography, 3D-printing, soft-robotics. The paper below showcases how the developed methods improves thermal performance of inkjet printers by 12%.
{: style="text-align: justify;"}

[Paper](https://ieeexplore.ieee.org/document/9465747){: .btn--research}

> Abstract: This article introduces a closed-loop control strategy for maintaining consistency of liquid temperature in commercial drop-on-demand (DoD) inkjet printing. No additional sensors or additional actuators are installed in the printhead while achieving consistency in liquid temperature. To this end, this article presents a novel in situ sensing-actuation policy at every individual liquid nozzle, where the jetting mechanism has three distinct roles. It is used for jetting liquid droplet onto the print media based on the print job. It is used as a soft sensor to estimate the real-time liquid temperature of the jetting nozzle. While not jetting liquid, it is used as a heating actuator to minimize the gradient of liquid temperature among nozzles. The soft sensing-based in situ controller is implemented in an experimentally validated digital twin that models the thermofluidic processes of the printhead. The digital twin is scalable and flexible to incorporate an arbitrary number of liquid nozzles, making the control strategy applicable for future designs of the printhead.
> {: style="text-align: justify;"}

## Application to Enegry Sectors

Nuclear fusion is a long-standing fascination for me. I strongly believe this is the most suitab;e solution to the dire energy crisis the world is soon going to face. A large part of my future research will be dedicated to control of nuclear fusion reactors. My early work on this is given below
{: style="text-align: justify;"}

[Paper](https://ieeexplore.ieee.org/document/9284622){: .btn--research}

> Abstract: This letter presents a closed-form solution to estimate space-dependent transport parameters of a linear one dimensional diffusion-transport-reaction equation. The infinite dimensional problem is approximated by a finite dimensional model by 1) taking a frequency domain approach, 2) linear parameterization of the unknown parameters, and 3) using a semi-discretization. Assuming full state knowledge, the commonly used output error criterion is rewritten as the equation error criterion such that the problem results in linear least squares. The optimum is then given by a closed-form solution, avoiding computational expensive optimization methods. Functioning of the proposed method is illustrated by means of simulation.
> {: style="text-align: justify;"}
