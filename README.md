# ☁️ Hi there, I'm Hank Zhang

<p align="left">
  <img src="https://komarev.com/ghpvc/?username=shangversatile&label=Profile%20Views&color=FF69B4&style=flat" />
</p>

<!-- DAILY-QUOTE-START -->
> **“A child without education is like a bird without wings.”**
> — Tibetan Proverb
> _source: zenquotes_
<!-- DAILY-QUOTE-END -->

I am interested in **Mechanism-guided Trustworthy AI Systems** — building AI systems that can be not only powerful, but also **understood, calibrated, monitored, corrected, and controlled** when they operate in changing real-world environments.

My current work starts from a practical question:

> **How can an AI system know when it is becoming unreliable — and what should happen next?**

I study this question through the connection between **model internals**, **uncertainty**, **causal mechanisms**, **dynamic environments**, and **system-level intervention**.

My near-term focus is to build reliability pipelines for AI models under distribution shift, noisy observations, incomplete data, and fragile deployment workflows. My long-term goal is broader: to understand how AI systems can move from black-box prediction toward **mechanism-grounded, corrigible, and controllable intelligence**.

**From black-box models to reliable, interpretable, and controllable intelligence.**

---
<p align="center">
  <img src="./spiral-research-roadmap.png"
       alt="Spiral Research Roadmap for Mechanism-guided Trustworthy AI Systems"
       width="850" />
</p>

<p align="center">
  <em>Not a linear ladder, but a spiral: each turn deepens understanding and strengthens control.</em>
</p>
---

> **“Nature operates through the principle of least action — intelligence, perhaps, should too.”**

<p align="center">
  <img src="https://latex.codecogs.com/svg.image?S=\int_{t_1}^{t_2}(p\dot{q}-H(q,p,t))dt" />
</p>

---

## 🎓 About Me

- 🎓 Incoming / M.S. in Data Science @ **UC San Diego, Halıcıoğlu Data Science Institute (HDSI)**
- 🔄 Background: **Management Information Systems → Machine Learning / AI Systems / Trustworthy AI**
- 🧭 Research-oriented transition:
  - Model User → Model Builder → System Thinker → Reliability-oriented Researcher
- 🛠 Currently building foundations in:
  - Machine Learning, Deep Learning, and NLP
  - Spatiotemporal Graph Learning and Complex Dynamic Systems
  - Causal Discovery, Uncertainty Quantification, and Trustworthy Evaluation
  - AI Reliability, Model Monitoring, and ML Systems
  - Signal Processing, Dynamical Systems, and Mechanism Discovery

---

## 🧭 Long-term Research Map

I currently think about trustworthy AI through four connected research paths.

| Path | Core Idea | My View |
|---|---|---|
| **Agentic AI** | Give language models a body through tools, memory, planning, and interaction. | This is an important application frontier, but not my only research identity. I am more interested in how agentic systems fail, how tool use should be monitored, and when human review or intervention should be triggered. |
| **Model Mechanisms** | Open and repair the model body: representations, circuits, concepts, world models, and causal structure. | This is the depth layer of my long-term interest. I want to understand whether internal representations can support correction, steering, and reliable behavior rather than remaining opaque high-dimensional artifacts. |
| **External Control Harness** | Keep AI systems inside evaluation, monitoring, guardrail, audit, fallback, and human-in-the-loop control loops. | This is my near-term anchor. Before fully understanding every internal mechanism, we can still build systems that detect risk, expose failure signals, abstain, defer, or roll back. |
| **Human and Scientific Understanding** | Study how human concepts, machine representations, and world mechanisms can align. | This is the philosophical and scientific motivation behind my interest in interpretability. I care about when an explanation is not just plausible, but connected to stable, human-understandable, and scientifically meaningful structure. |

My current strategy is:

```text
near-term anchor: external reliability harness and monitoring
research depth: model mechanisms, concepts, and causal structure
application frontier: agentic AI and scientific AI systems
long-term foundation: human concepts, machine representations, and world mechanisms
```

In this view, interpretability is not only about explaining a model after it makes a prediction. It can also become part of a broader control interface:

```text
model behavior
→ uncertainty and calibration
→ mechanism / concept signals
→ failure detection
→ human review, fallback, correction, or intervention
```

This is the direction I am gradually building toward: **AI systems whose reliability is grounded in both internal mechanisms and external control loops**.

## 🔬 Research Focus

I focus on **mechanism-guided trustworthy AI systems**: models and evaluation pipelines that remain understandable, calibratable, monitorable, and actionable under real-world uncertainty and distribution shift.

My long-term research question is:

> **How can mechanistic understanding make AI systems more reliable, corrigible, and controllable in complex dynamic environments?**

I am especially interested in AI systems where prediction alone is not enough. In domains such as traffic, environment, energy, scientific modeling, healthcare, and AI agents, models must expose uncertainty, reveal failure signals, support intervention, and remain reliable when the environment changes.

---

### 🧭 Mechanism-guided Reliable Prediction

- Spatiotemporal graph learning for complex dynamic systems
- Reliable forecasting under missingness, noise, regime changes, and long-horizon uncertainty
- Moving beyond accuracy-only evaluation toward calibration, robustness, and decision usefulness
- Understanding whether models learn stable dynamic mechanisms or dataset-specific correlations

---

### 🔗 Causal Reliability and Mechanism Discovery

- Causal discovery and invariant prediction under distribution shift
- Separating stable mechanisms from spurious correlations
- Applying causal and mechanistic thinking to environmental, traffic, energy, and scientific prediction
- Studying whether learned graphs, latent states, and representations correspond to meaningful system structure

---

### 📏 Uncertainty, Calibration, and Conformal Reliability

- Uncertainty quantification, calibration, and predictive intervals
- Conformal prediction under temporal shift, change points, and nonstationarity
- Turning model confidence into decision-relevant reliability signals
- Asking when a model should predict, abstain, defer to human review, or trigger fallback

---

### 🧠 Interpretable and Concept-based Representation

- Representation analysis, CKA, probing, and concept stability
- From post-hoc explanations to mechanism-level understanding
- Evaluating whether explanations and representations survive sanity checks
- Exploring concept bottlenecks, sparse features, and mechanistic signals as possible interfaces for model correction and control

---

### 🛡 AI Evaluation, Monitoring, and Control

- Model monitoring under data drift, prediction drift, calibration drift, and representation drift
- RAG / LLM evaluation pipelines where reliability and failure diagnosis matter
- Human-in-the-loop review, audit trails, fallback mechanisms, and intervention triggers
- Toward AI systems that can be audited, corrected, and controlled after deployment

---

## 🧩 My Current Research Framing

I currently organize trustworthy AI around three connected layers:

| Layer | Core Question | Methods / Signals |
|---|---|---|
| **Mechanism Layer** | What internal concepts, representations, causal structures, or dynamic mechanisms does the model rely on? | Mechanistic interpretability, concept probing, causal discovery, representation analysis |
| **Reliability Layer** | When is the model uncertain, miscalibrated, out-of-distribution, or about to fail? | Calibration, conformal prediction, uncertainty quantification, drift detection |
| **Control Layer** | How should the system respond when risk is detected? | Abstention, human review, fallback, rollback, monitoring, audit trails |

A practical research loop I want to build is:

```text
Model prediction
→ uncertainty and calibration check
→ concept / mechanism reliability check
→ drift and failure monitoring
→ risk-aware intervention
→ human review, fallback, or correction
```

This is why I am particularly interested in **dynamic distribution shift**: it forces a model to reveal whether it has learned stable mechanisms or only fragile correlations.

---

## 🧠 Deeper Motivation

I am interested in interpretability not only as a tool for explaining model outputs, but as a way to study the relationship between:

```text
world mechanisms
→ human concepts
→ machine representations
→ model behavior
→ system-level decisions
```

Human concepts and machine representations are both compressed descriptions of the world. A central challenge is to understand when high-dimensional learned representations can be aligned with stable, human-understandable, and scientifically meaningful mechanisms.

This motivates my interest in:

- mechanism discovery
- causal representation learning
- concept-based interpretability
- scientific machine learning
- trustworthy evaluation
- AI systems that can be corrected and controlled after deployment

I try to keep this broader question grounded in measurable reliability, concrete systems, and reproducible experiments.

---

## 🚧 What I'm Currently Building

### 🧪 Reliable-AI-Research-Lab

Flagship research lab for:

- reliable spatiotemporal forecasting under dynamic distribution shift
- graph construction validation
- uncertainty quantification and conformal calibration
- risk-aware decision evaluation
- mechanism-guided reliability experiments
- monitoring triggers for abstention, human review, and fallback

---

### 📚 Paper-Reading-Notes

Research-level reading system for:

- spatiotemporal graph learning
- uncertainty and calibration
- conformal prediction
- mechanism discovery and causal time-series analysis
- interpretable representation and trustworthy evaluation
- AI systems, monitoring, and technical debt in ML systems

---

### 🧠 Representation-Analysis-Lab

Exploratory lab for:

- concept representations
- CKA and representation similarity
- probing and hidden-state diagnostics
- sanity checks for explanations and representations
- representation drift under noise, missingness, and distribution shift

---

### 🤖 ML-DL-NLP-Lab

Foundation implementations from scratch:

- classical ML, MLPs, optimization, and backpropagation
- deep learning and attention mechanisms
- tiny transformer and NLP foundations
- mathematical intuition and implementation discipline
- baseline models for reliability and shift experiments

Earlier RAG / LLM evaluation work remains part of my broader AI reliability interest, especially when evaluation, monitoring, and failure diagnosis are central.

---

## 🛠 Tech Stack

### Core

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-CC2927?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

### Machine Learning

<p>
  <img src="https://img.shields.io/badge/Scikit--Learn-FF6F00?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
</p>

### Focus Areas

<p>
  <img src="https://img.shields.io/badge/Trustworthy_AI-191970?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Spatiotemporal_GNN-4B0082?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Causal_Discovery-8A2BE2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Uncertainty_Calibration-006400?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Model_Monitoring-2F4F4F?style=for-the-badge" />
</p>

---

## 📊 GitHub Stats

<p align="center">
  <img height="180em"
       src="https://github-readme-stats-sigma-five.vercel.app/api?username=shangversatile&show_icons=true&theme=tokyonight" />

  <img height="180em"
       src="https://github-readme-stats-sigma-five.vercel.app/api/top-langs/?username=shangversatile&layout=compact&theme=tokyonight" />
</p>

---

## 🧠 Intellectual Interests

| Domain | Focus |
|---|---|
| 🧠 AI | Mechanism-guided trustworthy AI, reliability, interpretability, causality |
| 🔬 Science | Complex dynamic systems, uncertainty-aware prediction, physics-inspired modeling |
| 🛠 Systems | Evaluation pipelines, monitoring, human-in-the-loop control, ML systems for reliable deployment |
| 📡 Signals | Noise, sampling, filtering, graph signals, state estimation, dynamic observations |
| 📖 Humanities | Epistemology, pragmatism, causality, interpretability, philosophy of science |

---

## 📌 Active Research Projects

| Project | Direction | Core Question |
|---|---|---|
| **Reliable Spatiotemporal Forecasting under Dynamic Shift** | STGNN / UQ / Conformal Prediction | How can forecasts remain calibrated and decision-useful when graph structure, sensors, and environments shift? |
| **Mechanism Discovery for Complex Dynamic Systems** | Causal Discovery / Dynamic Systems | Can models recover stable mechanisms rather than exploiting unstable correlations? |
| **Graph Construction and Reliability Validation** | Spatiotemporal Graph Learning | When is a learned or designed graph a valid representation of physical, statistical, or causal influence? |
| **Concept and Representation Stability** | Interpretability / Representation Analysis | Do model representations encode meaningful concepts, and do they remain stable under shift? |
| **AI Evaluation and Monitoring Pipelines** | AI Reliability / Model Monitoring | How can deployed AI systems be audited, calibrated, monitored, corrected, and controlled over time? |
| **Mechanism-guided Reliability Harness** | Trustworthy AI Systems | Can uncertainty signals, mechanism checks, and monitoring triggers form a practical control loop for AI failure detection and intervention? |

---

## 💬 Let's Connect

- 💡 Topics:
  - Mechanism-guided Trustworthy AI
  - Spatiotemporal Graph Learning
  - Uncertainty and Calibration
  - Causal Discovery
  - AI Evaluation and Monitoring
  - Interpretability and Representation Analysis
  - Human-in-the-loop AI Reliability

- 📫 Open to:
  - Research collaborations
  - ML / AI internships
  - Applied AI reliability and evaluation projects
  - Mechanism-guided AI systems research

---

<p align="center">
  <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake.svg" />
</p>
