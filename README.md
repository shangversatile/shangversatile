# ☁️ Hi there, I'm Hank Zhang

<p align="left">
  <img src="https://komarev.com/ghpvc/?username=shangversatile&label=Profile%20Views&color=FF69B4&style=flat" />
</p>

<!-- DAILY-QUOTE-START -->
> **“The soul is neither born, and nor does it die.”**
> — Bhagavad Gita  
> _source: zenquotes_
<!-- DAILY-QUOTE-END -->

I am interested in how intelligent systems form, preserve, and revise their internal representations of the world.

My research began with a practical problem:

> **What happens when an AI model encounters a world different from the one on which it was trained?**

In spatiotemporal forecasting and other dynamic prediction tasks, noise, missing observations, structural changes, and distribution shifts can quickly expose the limits of a learned model. Studying these failures led me from reliability questions toward a deeper problem:

> **When new experience arrives, what should a model preserve, what should it revise, and what new structure should it create?**

My current direction is **Continual Structured Representation Learning** — studying how learning systems can retain shared structure across environments, absorb genuinely new knowledge, and reorganize inadequate representations without simply overwriting the past.

In the long term, I hope to understand how machines can move from task-specific pattern fitting toward adaptive internal models of states, mechanisms, environments, and change.

**From reliable prediction to continually evolving representations of the world.**

---

<p align="center">
  <img src="./spiral-research-roadmap.png"
       alt="Spiral roadmap from reliable prediction to adaptive world representation"
       width="850" />
</p>

<p align="center">
  <em>
    Research is not a linear ladder: each encounter with failure reveals a deeper question about learning, representation, and understanding.
  </em>
</p>

---

> **“Nature operates through the principle of least action — intelligence, perhaps, should too.”**

<p align="center">
  <img src="https://latex.codecogs.com/svg.image?S=\int_{t_1}^{t_2}(p\dot{q}-H(q,p,t))dt" />
</p>

---

## 🎓 About Me

- 🎓 Incoming M.S. in Data Science at **UC San Diego, Halıcıoğlu Data Science Institute**
- 🔄 Background: **Management Information Systems → Machine Learning → Scientific and Reliable AI**
- 🧭 Current transition:
  - Model User → Model Builder → Representation Researcher → Scientific Thinker
- 🛠 Building foundations in:
  - Machine Learning, Deep Learning, and Representation Learning
  - Probability, Optimization, Linear Algebra, and Geometry
  - Dynamical Systems, State-space Models, and Signal Processing
  - Continual Learning, Causal Representation, and World Models
  - Scientific Machine Learning and Mechanism Discovery
  - Epistemology, Philosophy of Science, and Models of Understanding

---

## 🧭 Research Evolution

My earlier work focused on **reliable AI under dynamic distribution shift**.

In forecasting systems, I was interested in questions such as:

- What happens when observations become noisy or incomplete?
- Why do models remain confident after their assumptions have failed?
- Do learned graphs and latent representations reflect stable structure?
- How can uncertainty and failure signals reveal model limitations?

These questions remain important, but I now view them as the first layer of a broader research program.

```text
distribution shift
→ exposes representation fragility

catastrophic forgetting
→ exposes interference between old and new knowledge

task-specific learning
→ exposes the partial nature of learned abstractions

continual experience
→ requires representations to be preserved, extended, or reorganized

generalization
→ tests whether a model has learned structure or only correlations
```

The deeper problem is therefore not only how to detect failure after deployment.

It is:

> **How should a learning system revise its internal model of the world when new experience conflicts with what it previously learned?**

---

## 🔬 Current Research Direction

# Continual Structured Representation Learning

I study how models learn and update internal representations from **non-stationary, multi-environment, and sequential experience**.

The central challenge is the relationship between:

```text
stability
  preserving useful prior knowledge

plasticity
  acquiring genuinely new knowledge

structure
  separating shared mechanisms from contextual variation

revision
  reorganizing representations when old abstractions become inadequate
```

A useful conceptual decomposition is:

\[
z_t =
\left(
z_t^{\mathrm{shared}},
z_t^{\mathrm{context}},
z_t^{\mathrm{novel}}
\right),
\]

where:

- \(z_t^{\mathrm{shared}}\) represents structure that persists across environments;
- \(z_t^{\mathrm{context}}\) represents task-, domain-, or observation-specific factors;
- \(z_t^{\mathrm{novel}}\) represents genuinely new information that cannot be explained by the current model.

The objective is not to keep every representation unchanged. A good learning system should be able to decide:

```text
preserve
when the world is unchanged but observations differ

adapt
when context or task requirements change

expand
when new objects, variables, or mechanisms appear

reorganize
when the old representation was fundamentally incomplete
```

---

## ❓ Central Research Question

> **How can a learning system preserve shared latent structure across changing environments while remaining plastic enough to discover and integrate genuinely new structure?**

This question connects several areas that are often studied separately:

| Area | Role in the Research Problem |
|---|---|
| **Continual Learning** | How can models learn sequentially without catastrophic forgetting or plasticity loss? |
| **Representation Learning** | What information is encoded, discarded, entangled, or shared? |
| **Distribution Shift** | Which environmental changes expose fragile or task-specific representations? |
| **Dynamical Systems** | What internal state is sufficient to summarize the past and predict future evolution? |
| **Causal Representation** | Which latent variables correspond to stable mechanisms rather than accidental correlations? |
| **World Models** | How can internal representations support prediction, intervention, planning, and revision? |
| **Scientific ML** | Can models recover effective variables, symmetries, interactions, and evolution laws from data? |

These are not separate topics in my current framing. They are different views of the same problem:

> **How does a model's internal representation grow with experience?**

---

## 🌀 From Task-specific Features to World-structured Representations

A representation learned for a single objective is not necessarily a representation of the world.

For a task \(T_1\), a model may learn:

\[
z^{(1)} = E_{T_1}(x),
\]

while a different objective \(T_2\) may produce:

\[
z^{(2)} = E_{T_2}(x).
\]

Each representation may preserve only the information necessary for its own objective.

My long-term interest is whether diverse tasks, environments, temporal observations, and interventions can constrain a model toward a more shared internal structure:

\[
x
\longrightarrow
z_{\mathrm{shared}}
\longrightarrow
\begin{cases}
\text{prediction}\\
\text{classification}\\
\text{parameter estimation}\\
\text{intervention response}\\
\text{control}\\
\text{new-task transfer}
\end{cases}
\]

However, a larger representation is not automatically a more unified representation.

It may merely store unrelated task features side by side. A meaningful shared representation should instead reveal common generative factors, states, interactions, or mechanisms.

This motivates a sharper question:

> **When does multi-task or multi-environment learning recover common structure, and when does it merely accumulate task-specific features?**

---

## ⚖️ Stability, Plasticity, and Memory

Memory in a learning system is not only the storage of past samples.

I distinguish several computational forms of memory:

| Memory Form | Possible Computational Realization |
|---|---|
| **Parametric memory** | Knowledge encoded in model weights |
| **Episodic memory** | Replay buffers, retrieval systems, stored experiences |
| **State memory** | Hidden states that summarize relevant past observations |
| **Structural memory** | Persistent representations of objects, relations, dynamics, and mechanisms |

My main interest is **structural memory**.

A system should not merely remember past outputs. It should preserve what prior experience revealed about the structure of the world, while remaining capable of changing that structure when new evidence demands it.

This creates the stability–plasticity problem:

\[
\text{preserve previous structure}
\quad\leftrightarrow\quad
\text{remain capable of revision}.
\]

Too much stability leads to rigidity.

Too much plasticity leads to forgetting.

A scientifically meaningful learner must determine which parts of its internal model deserve each treatment.

---

## 🌍 Distribution Shift as a Scientific Probe

Distribution shift is not my final research identity. It is an experimental condition that reveals what a model has learned.

Different shifts imply different forms of change:

| Change | What May Have Changed | Desired Representation Response |
|---|---|---|
| Sensor, scanner, style, or viewpoint | Observation process | Preserve underlying state |
| Task or label definition | Readout objective | Preserve shared structure, modify task head |
| New object or variable | State space | Expand the representation |
| Changed interaction or dynamics | Mechanism | Revise the structural model |
| New combination of known factors | Composition | Generalize without relearning |
| Contradictory evidence | Existing abstraction | Reorganize the representation |

The research question is therefore not merely:

> Can the model remain accurate under shift?

It is:

> **Can the model distinguish superficial change, contextual change, genuinely new structure, and failure of its previous world model?**

---

## ⚙️ Dynamical and Physical Perspective

Dynamical systems provide a mathematically controlled setting for studying representation growth.

Suppose an underlying state evolves as:

\[
s_{t+1}=F(s_t,u_t),
\]

while the model observes only:

\[
x_t=G_e(s_t)+\eta_t,
\]

where \(e\) denotes the environment or observation condition.

The model must infer:

\[
z_t=E(x_{\leq t}),
\]

and determine whether \(z_t\) captures:

- the physical state;
- environmental context;
- system parameters;
- interaction structure;
- genuinely new dynamics.

This connects machine learning to a classical scientific question:

> **How can effective state variables and evolution laws be discovered from incomplete observations?**

Physics provides important conceptual guidance:

```text
microscopic observations
→ effective variables
→ invariants and symmetries
→ evolution laws
→ prediction and intervention
```

My interest is not simply to attach physical constraints to a neural network. It is to study whether learning systems can discover useful abstractions in a way analogous to scientific modeling.

---

## 🧪 Near-term Research Program

My first concrete research problem is:

# Continual Learning of Shared Latent Dynamics across Changing Environments

The goal is to study whether a model can retain a shared latent state while sequentially encountering changes in:

- observation viewpoint;
- noise and missingness;
- physical parameters;
- external forces;
- object composition;
- governing dynamics.

A controlled physical system may be used first, such as:

- pendulum systems;
- coupled oscillators;
- Lorenz dynamics;
- spring–mass systems;
- interacting particles.

The experimental structure is:

```text
known physical system
→ multiple observation environments
→ sequential learning
→ shared / context / novel representation analysis
→ retention, adaptation, and intervention tests
```

The first hypothesis is:

> **A representation that explicitly separates shared state, environmental context, and system parameters will support better continual adaptation and mechanism generalization than a single entangled latent space.**

The project will examine:

- old-environment retention;
- adaptation to new environments;
- latent alignment with ground-truth states;
- representation reorganization;
- intervention prediction;
- compositional generalization;
- catastrophic forgetting;
- long-term plasticity.

---

## 🧠 Long-term Research Framework

My long-term direction has three connected but methodologically distinct layers.

### 1. Technical Science

**How do machines learn shared, structured, and revisable representations?**

Methods:

- mathematical modeling;
- controlled experiments;
- representation analysis;
- continual learning;
- causal and dynamical inference;
- identifiability analysis.

### 2. Human and Machine Cognition

**How do humans and machines form concepts, memories, abstractions, and internal models?**

Questions:

- Is memory storage or reconstruction?
- Are representations inherently task-relative?
- How are concepts reorganized after contradictory experience?
- What distinguishes prediction from understanding?

This is currently an intellectual and interdisciplinary research interest rather than a claim that machine learning alone can answer cognitive science.

### 3. Epistemology, Agency, and Responsibility

**What allows a system to count as understanding, acting, or being responsible?**

Questions concerning AI responsibility, accountability, agency, and human oversight require their own methods from:

- philosophy of action;
- epistemology;
- ethics;
- law;
- human–computer interaction;
- science and technology studies.

These questions motivate my broader thinking, but I do not treat them as consequences that can be derived directly from representation-learning experiments.

---

## 🧭 Long-term Vision

My broader goal is to study **Adaptive World Representation**:

> How can an intelligent system form an internal model from experience, preserve what remains valid, revise what fails, and expand its conceptual structure when it encounters genuinely new phenomena?

I view learning as an iterative scientific process:

```text
observe
→ compress
→ form structure
→ predict
→ encounter contradiction
→ revise representation
→ test under new conditions
→ build a richer internal model
```

This connects four long-term interests:

| Discipline | Inspiration |
|---|---|
| **Mathematics** | Identifiability, geometry, probability, optimization, invariance |
| **Physics** | State, dynamics, symmetry, conservation, scale, effective theories |
| **Computer Science** | Learning algorithms, memory systems, representation, continual adaptation |
| **Philosophy** | Explanation, evidence, abstraction, understanding, and model revision |

---

## 🚧 What I'm Currently Building

### 🧪 Reliable-AI-Research-Lab

This repository began with reliable spatiotemporal forecasting under uncertainty and distribution shift.

It now serves as the experimental origin of a broader program:

```text
reliable forecasting
→ representation fragility
→ shared latent structure
→ continual adaptation
→ structured world representation
```

Current and planned themes:

- failure of learned representations under changing environments;
- shared versus environment-specific latent structure;
- state and parameter separation;
- continual adaptation and forgetting;
- mechanism generalization;
- controlled physical and dynamical testbeds.

---

### 📚 Paper-Reading-Notes

Research-level reading and synthesis across:

- continual learning and plasticity;
- representation learning;
- causal representation learning;
- dynamical systems and system identification;
- world models;
- scientific machine learning;
- computational neuroscience;
- philosophy of science and representation.

The goal is not to collect papers, but to develop research questions, mathematical derivations, critical comparisons, and falsifiable hypotheses.

---

### 🧠 Representation-Analysis-Lab

Experimental tools for studying:

- representation similarity and alignment;
- CKA, CCA, Procrustes analysis, and probing;
- latent state recovery;
- disentanglement and factorization;
- representation drift and reorganization;
- stability–plasticity behavior;
- shared, contextual, and novel features.

---

### 🤖 ML-DL-NLP-Lab

Foundation implementations from scratch:

- classical machine learning;
- optimization and backpropagation;
- neural networks and attention;
- recurrent and state-space models;
- representation learning;
- mathematical derivation and implementation discipline.

This repository supports the technical foundations needed for deeper research rather than serving as an isolated collection of models.

---

### 📐 Mathematical-Foundations-for-AI-CS-Lab

A developing foundation in:

- mathematical logic and proof;
- probability and statistics;
- linear algebra and matrix analysis;
- optimization;
- discrete mathematics;
- geometry and symmetry;
- dynamical systems;
- causal and statistical reasoning.

---

## 🛠 Technical Foundations

### Core Languages and Tools

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-CC2927?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/Scikit--Learn-FF6F00?style=for-the-badge&logo=scikit-learn&logoColor=white" />
</p>

### Research Areas

<p>
  <img src="https://img.shields.io/badge/Continual_Learning-191970?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Representation_Learning-4B0082?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Dynamical_Systems-006400?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Causal_Representation-8A2BE2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Scientific_ML-2F4F4F?style=for-the-badge" />
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

| Domain | Current Interest |
|---|---|
| 🧠 **Machine Learning** | Continual learning, representation learning, world models, causal representation |
| 📐 **Mathematics** | Probability, geometry, identifiability, optimization, dynamical systems |
| 🔬 **Physics** | State variables, evolution laws, symmetry, invariants, emergence, effective theories |
| 🧬 **Cognition** | Memory, abstraction, concept formation, human and machine representation |
| 📖 **Philosophy** | Scientific explanation, structural realism, epistemology, agency, responsibility |
| 🛠 **Systems** | How computational architectures preserve, retrieve, revise, and compose knowledge |

---

## 📌 Research Projects

| Project | Role in the Research Program | Core Question |
|---|---|---|
| **Reliable Spatiotemporal Forecasting under Dynamic Shift** | Original empirical starting point | How do changes in observations and environments reveal fragile learned representations? |
| **Shared Latent Dynamics across Environments** | Current technical focus | Can a model preserve common system state while observation conditions change? |
| **Continual Structured Representation Learning** | Emerging main project | How should representations be preserved, expanded, and reorganized as new experience arrives? |
| **Representation Stability and Reorganization** | Analytical foundation | When is representation drift harmful, and when does it reflect necessary conceptual revision? |
| **Mechanism and State Discovery** | Scientific extension | Can learned latent variables recover states, interactions, and evolution laws? |
| **Human and Machine Representation Notes** | Interdisciplinary inquiry | How do task, memory, abstraction, and experience shape representations in humans and machines? |

---

## 💬 Let's Connect

### Research Topics

- Continual Structured Representation Learning
- Shared Latent State and Dynamics
- Stability–Plasticity in Learning Systems
- Causal and Identifiable Representation Learning
- Dynamical Systems and Scientific Machine Learning
- World Models and Adaptive Internal Representations
- Human and Machine Cognition
- Philosophy of Scientific Models and AI

### Open To

- Research collaborations
- ML / AI research internships
- Scientific machine learning projects
- Continual and representation learning research
- Interdisciplinary work connecting AI, mathematics, physics, and cognition

---

<p align="center">
  <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake.svg" />
</p>
