# ☁️ Hi there, I'm Hank Zhang

<p align="left">
  <img src="https://komarev.com/ghpvc/?username=shangversatile&label=Profile%20Views&color=FF69B4&style=flat" />
</p>

<!-- DAILY-QUOTE-START -->
> **“Whether you think you can or think you can't – you are right.”**
> — Henry Ford
> _source: zenquotes_
<!-- DAILY-QUOTE-END -->

I am interested in **Mechanism-guided Trustworthy AI Systems** — AI systems that can be understood, calibrated, monitored, intervened upon, and controlled in complex dynamic environments.

My current research direction connects **mechanism interpretability, concept representations, causal discovery, spatiotemporal graph learning, uncertainty calibration, and system-level monitoring**.

I study how AI models fail under distribution shift, noisy observations, incomplete data, changing environments, and fragile deployment workflows — and how to build models and evaluation pipelines that are more **reliable, auditable, controllable, and scientifically grounded**.

My current view of trustworthy AI is not limited to making model outputs more explainable. I see it as a broader **control problem**:

> Can an AI system detect when it is becoming unreliable, diagnose why it is failing, expose the mechanisms behind its behavior, and trigger correction, abstention, human review, fallback, or intervention before harm occurs?

In this sense, interpretability is not only a visualization tool. It can become part of a **control interface**: a way to connect internal concepts, representations, uncertainty, and causal mechanisms to external system-level decisions.

**From black-box models to reliable, interpretable, and controllable intelligence.**

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
  - Machine Learning, Deep Learning, NLP
  - Spatiotemporal Graph Learning and Complex Dynamic Systems
  - Causal Discovery, Uncertainty Quantification, and Trustworthy Evaluation
  - AI Reliability, Model Monitoring, and ML Systems
  - Signal Processing, Dynamical Systems, and Mechanism Discovery

---

## 🔬 Research Focus

I focus on **mechanism-guided trustworthy AI systems**: building AI models and evaluation pipelines that remain understandable, calibratable, monitorable, and actionable under real-world uncertainty and distribution shift.

My long-term research question is:

> **How can mechanistic understanding make AI systems more reliable, corrigible, and controllable in complex dynamic environments?**

I am especially interested in systems where prediction is not enough. In domains such as traffic, environment, energy, scientific modeling, healthcare, and AI agents, models must not only produce outputs, but also expose uncertainty, reveal failure signals, support human or algorithmic intervention, and remain reliable when the environment changes.

### 🧭 Mechanism-guided Reliable Prediction
- Spatiotemporal graph learning for complex dynamic systems
- Reliable forecasting under missingness, noise, regime changes, and long-horizon uncertainty
- Moving beyond accuracy-only evaluation toward calibration, robustness, and decision usefulness
- Understanding when models learn stable dynamic mechanisms rather than dataset-specific correlations

### 🔗 Causal Reliability and Mechanism Discovery
- Causal discovery and invariant prediction under distribution shift
- Separating stable mechanisms from spurious correlations
- Applying causal and mechanistic thinking to environmental, traffic, energy, and scientific prediction
- Studying whether learned graphs, latent states, and representations correspond to meaningful system structure

### 📏 Uncertainty, Calibration and Conformal Reliability
- Uncertainty quantification, calibration, and predictive intervals
- Conformal prediction under temporal shift, change points, and nonstationarity
- Turning model confidence into decision-relevant reliability signals
- Asking when a model should predict, abstain, defer to human review, or trigger fallback

### 🧠 Interpretable and Concept-based Representation
- Representation analysis, CKA, probing, and concept stability
- From post-hoc explanations to mechanism-level understanding
- Evaluating whether explanations and representations survive sanity checks
- Exploring concept bottlenecks, sparse features, and mechanistic signals as possible interfaces for model correction and control

### 🛡 AI Evaluation, Monitoring and Control
- Model monitoring under data drift, prediction drift, calibration drift, and representation drift
- RAG / LLM evaluation pipelines where reliability and failure diagnosis matter
- Human-in-the-loop review, audit trails, fallback mechanisms, and intervention triggers
- Toward AI systems that can be audited, corrected, and controlled after deployment

---

## 🧩 My Current Research Framing

I currently think about trustworthy AI through three connected layers:

| Layer | Core Question | Methods / Signals |
|---|---|---|
| **Mechanism Layer** | What internal concepts, representations, causal structures, or dynamic mechanisms does the model rely on? | Mechanistic interpretability, concept probing, causal discovery, representation analysis |
| **Reliability Layer** | When is the model uncertain, miscalibrated, out-of-distribution, or about to fail? | Calibration, conformal prediction, uncertainty quantification, drift detection |
| **Control Layer** | How should the system respond when risk is detected? | Abstention, human review, fallback, rollback, monitoring, audit trails |

My goal is to connect these layers into a practical research loop:

```text
Model prediction
→ uncertainty and calibration check
→ concept / mechanism reliability check
→ drift and failure monitoring
→ risk-aware intervention
→ human review, fallback, or correction
