# 📚 RecSys Research Digest — 2026-11-02 ~ 2026-11-09

> 자동 생성: 2026-11-09 02:16 | 팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

This week's research landscape reveals a strong convergence around making topological and geometric deep learning more practical, interpretable, and efficient. The standout paper for the team is **TopoSHAP**, which directly addresses a critical gap in topological deep learning (TDL): the lack of principled explainability methods for higher-order architectures. By extending Shapley values to attribute importance across cells and neighborhood types, it provides both interpretability and a pathway to efficient architecture search—a dual utility that aligns perfectly with the team's work on simplicial/cell complex neural networks and combinatorial complex networks. Equally relevant is the **filtration methods paper**, which proposes three alternatives to the standard lower-star filtration, directly enriching the team's persistent homology and persistence diagram toolkit with methods that yield more expressive topological summaries.

Beyond the core TDL papers, several works offer transferable methodological insights. **LIR (Latent Importance Reweighting)** introduces Jacobian-based dimension weighting for latent graph generation, a technique that resonates with the team's interests in graph representation learning and diffusion-based generative models on geometric structures. The idea of prioritizing reconstruction-critical dimensions could inform how we weight topological features in latent spaces. **GA-SRMC** extends score-based Monte Carlo with Fisher-information preconditioning—a geometry-aware sampling strategy that connects to the team's work on Riemannian manifold diffusion and could improve sampling in topological generative pipelines. **GMAdam's** slow-manifold analysis of multi-task gradient balancing is relevant given TDL's inherently multi-scale loss landscapes (e.g., balancing objectives across different cell dimensions).

The remaining papers (**HFX3D**, **MetricPose**, **SZO-κ**) are more peripheral but not without value. HFX3D's massive 3D point cloud benchmark with hierarchical annotations could serve as a testbed for the team's point cloud and geometric deep learning methods, while SZO-κ's use of forward-pass activation geometry for gradient estimation introduces spectral ideas that may complement the team's spectral graph convolution research.

---

## 📄 Top Papers This Week


### 1. TopoSHAP: Shapley for Explainable and Efficient Topological Deep Learning

| 항목 | 내용 |
|------|------|
| **저자** | Mathilde Papillon, Nina Miolane |
| **발행일** | 2026-11-05 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.608 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08789v1) \| [PDF](https://arxiv.org/pdf/2611.08789v1) |

**요약:** TopoSHAP extends Shapley-value explanations to topological deep learning, attributing importance to higher-order cells and neighborhood types for both model interpretability and efficient architecture search.

**핵심 기여:**

- Introduces TopoSHAP-cell, which assigns Shapley values to topological cells (nodes, edges, rings, etc.) to explain TDL predictions, achieving up to 112× speedup over graph-based explainability baselines while matching or exceeding explanation quality on GraphXAI benchmarks.

- Proposes TopoSHAP-neighbor, which attributes Shapley values to neighborhood types (e.g., boundary, co-boundary, adjacency) to quantify each architectural component's contribution to model performance.

- Leverages TopoSHAP-neighbor explanations to drive a backward-elimination architecture search that identifies smaller, competitive TDL architectures early in training, reducing computational cost by up to 11.3× compared to traditional hyperparameter sweeps.

- Demonstrates that TopoSHAP explanations reveal beneficial topological feature design choices, yielding measurable improvements in both explanation recovery and downstream predictive accuracy.


**팀 관련성:** Directly relevant to the team's work on topological deep learning, cell/simplicial complex neural networks, and higher-order interactions. TopoSHAP provides a principled explainability and architecture selection tool for TDL models built on simplicial, cell, and combinatorial complexes—offering practical guidance on which higher-order structures and neighborhood definitions actually matter, a key open question in TDL research.

---

### 2. Beyond the Lower-Star Filtration: Alternative Filtration Methods for Persistent Homology

| 항목 | 내용 |
|------|------|
| **저자** | Innocent Abaa, Umar Islambekov |
| **발행일** | 2026-11-06 |
| **카테고리** | stat.ML, cs.LG, math.AT |
| **관련성 점수** | 0.517 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08833v1) \| [PDF](https://arxiv.org/pdf/2611.08833v1) |

**요약:** Three alternative filtration methods (ε-lower-star, Lp, and softmax) are proposed to overcome the lower-star filtration's limitation of simultaneously introducing simplices and their boundary faces, yielding richer persistence diagrams.

**핵심 기여:**

- Identifies a key limitation of the standard lower-star filtration (LSF): higher-dimensional simplices can enter simultaneously with their boundary faces, causing topological features (loops, voids) to be immediately filled and thus absent from persistence diagrams.

- Proposes three alternative filtration constructions—ε-lower-star (ELSF) adding dimension-dependent delays, Lp filtration (LpF) using Lp-norm aggregation over all vertex values, and softmax filtration (SMF) using differentiable softmax aggregation—each ensuring more progressive simplex entry.

- Demonstrates that the new filtrations produce persistence diagrams with additional persistence features not captured by LSF, potentially encoding finer structural information useful for distinguishing data populations.

- Experimental validation on simulated and real-world datasets shows the proposed methods are computationally efficient and offer greater sensitivity to structural differences compared to LSF.


**팀 관련성:** Directly relevant to the team's work on persistent homology, persistence diagrams, simplicial complexes in ML, and topological deep learning. These alternative filtrations could improve TDA-based feature extraction pipelines used in topological representation learning, and the differentiable softmax filtration is particularly interesting for integration into end-to-end learnable topological pipelines.

---

### 3. From Geometry to Function: A Multi-Task LiDAR Benchmark Dataset for Semantic and Functional Parsing of Urban Facades

| 항목 | 내용 |
|------|------|
| **저자** | Abdiaziz Muse et al. |
| **발행일** | 2026-11-05 |
| **카테고리** | cs.CV, cs.AI, cs.GR |
| **관련성 점수** | 0.471 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08645v1) \| [PDF](https://arxiv.org/pdf/2611.08645v1) |

**요약:** HFX3D introduces a ~492M-point LiDAR facade benchmark with three-tier annotations (semantic, instance, functional attributes), enabling function-aware 3D urban parsing beyond pure geometric segmentation.

**핵심 기여:**

- Introduces the first large-scale facade LiDAR dataset pairing geometry and semantics with per-instance functional attribute labels across 26 buildings, four seasons, and varied lighting/weather conditions.

- Proposes a semi-automatic annotation pipeline combining geometry-guided heuristics with expert validation to produce three-tier labels (semantic segmentation, instance segmentation, functional attributes).

- Benchmarks point-based (PointNet++, RandLA-Net), graph-based (DGCNN), convolutional (KPConv), and transformer (Point Transformer) architectures, revealing that severe class imbalance, repetitive instance separation, and functional reasoning from geometry remain substantially open challenges.

- Establishes a new evaluation protocol and baseline suite for function-aware 3D urban understanding, with public code and data to support reproducibility.


**팀 관련성:** Directly relevant to the team's work on point cloud learning with geometric deep learning and graph-based architectures. The dataset's challenges—reasoning about function from pure geometry, handling repetitive structures, and severe class imbalance in 3D point clouds—present natural testbeds for equivariant networks (SE(3)/E(3)), graph neural networks (DGCNN, message passing), and topological methods (e.g., persistent homology for capturing facade repetition patterns). The multi-tier annotation structure also opens opportunities to explore higher-order relational reasoning between architectural elements.

---

### 4. Not All Latents Are Equal: Importance-Weighted Latent Graph Generation

| 항목 | 내용 |
|------|------|
| **저자** | Biraaj Rout et al. |
| **발행일** | 2026-11-05 |
| **카테고리** | cs.LG, cs.AI |
| **관련성 점수** | 0.458 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08788v1) \| [PDF](https://arxiv.org/pdf/2611.08788v1) |

**요약:** Proposes Latent Importance Reweighting (LIR), a Jacobian-based dimension weighting scheme that closes the performance gap between latent and discrete graph diffusion/flow models by prioritizing reconstruction-critical latent dimensions.

**핵심 기여:**

- Identifies that latent graph generation underperforms discrete methods because latent dimensions have highly unequal impact on graph reconstruction, yet existing losses treat them uniformly — causing models to waste capacity on task-irrelevant dimensions.

- Introduces LIR, which computes per-dimension importance weights via the Jacobian of the decoder with respect to the latent, measuring each dimension's relative influence on final graph reconstruction.

- The method is model-agnostic, parameter-free, and hyperparameter-free — it can be applied on top of any latent graph generative model (demonstrated on two different autoencoders across multiple benchmarks) with no architectural changes.

- Experiments show LIR consistently boosts generation quality and accelerates training convergence, narrowing the gap between scalable latent approaches and quadratic-cost discrete graph diffusion/flow matching methods.


**팀 관련성:** Directly relevant to the team's interests in geometric and topological methods for graph representation learning and diffusion processes for generative models. The Jacobian-based importance analysis of latent spaces offers a principled lens that could extend to latent generative models over simplicial/cell complexes and higher-order structures, where similar dimension-imbalance issues likely arise.

---

### 5. Task-Contribution Dynamics of Adam in Physics-Informed Neural Networks: Slow-Manifold Analysis and Gradient Modulation

| 항목 | 내용 |
|------|------|
| **저자** | Enzhan Zheng, Xiaoliang Song |
| **발행일** | 2026-11-06 |
| **카테고리** | math.NA, cs.LG |
| **관련성 점수** | 0.453 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08910v1) \| [PDF](https://arxiv.org/pdf/2611.08910v1) |

**요약:** Analyzes how Adam's optimizer distributes updates across competing PINN loss terms via slow-manifold singular perturbation theory, and proposes GMAdam which uses task-specific second-moment estimates to improve multi-task gradient balancing.

**핵심 기여:**

- Introduces task-wise contribution indicators for Adam updates and identifies three distinct training regimes (smooth, intermittent spikes, persistent oscillations) governing multi-task optimization dynamics in PINNs.

- Derives a continuous-time singular perturbation framework under the (1-β₂)/(1-β₁)≪1 regime, revealing that task-contribution redistribution is governed by curvature-alignment disparities and coordinatewise distribution differences of preconditioned task gradients—both mediated by Adam's shared second-moment estimate.

- Proposes Gradient-Modulated Adam (GMAdam), which replaces Adam's shared second-moment estimate with task-specific second-moment estimates to modulate incoming task gradients, inspired by but improving upon AdaTask.

- Demonstrates consistent accuracy gains over AdaTask on challenging PDE benchmarks including high-frequency Poisson/wave equations, Allen-Cahn, and 2D lid-driven cavity flow at Re=100 and 400.


**팀 관련성:** This paper is primarily about optimizer dynamics for physics-informed neural networks and multi-task loss balancing—topics peripheral to our team's focus on geometric/topological deep learning. However, the singular perturbation analysis of adaptive optimizers could offer transferable insights for training equivariant or topological networks with competing loss terms (e.g., reconstruction + topological regularization), and the multi-task gradient modulation idea may be relevant when combining geometric priors with multiple learning objectives.

---

### 6. An Educated Guess: Deriving Statistically Aligned Gradient Estimates for Zeroth-Order Optimisation

| 항목 | 내용 |
|------|------|
| **저자** | Justus Huebotter et al. |
| **발행일** | 2026-11-05 |
| **카테고리** | cs.LG, cs.AI |
| **관련성 점수** | 0.440 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08712v1) \| [PDF](https://arxiv.org/pdf/2611.08712v1) |

**요약:** Proposes Spectral Zeroth-Order (SZO-κ) methods that leverage forward-pass activation geometry to derive gradient estimates with improved alignment, addressing the curse of dimensionality in zeroth-order optimisation.

**핵심 기여:**

- Derives a family of zeroth-order optimisation methods (SZO-κ) that construct perturbation directions from the spectral structure of activations during the forward pass, replacing blind random noise with geometrically informed search directions.

- Formulates gradient-guessing objectives under explicit stochastic assumptions, showing that optimal perturbation directions align with feature-supported subspaces identified via local activation geometry.

- Provides theoretical analysis of gradient alignment, bias-variance tradeoffs, and training stability of SZO-κ relative to standard perturbation baselines (SPSA, weight perturbation) and backpropagation.

- Demonstrates the approach on multilayer and convolutional networks, showing that spectral perturbation directions yield more informative loss responses and mitigate the dimensionality curse of classical zeroth-order methods.


**팀 관련성:** While not directly about geometric/topological deep learning, this paper's use of spectral structure from activation geometry connects to the team's expertise in spectral graph convolutions and Hodge Laplacians. The backpropagation-free optimisation framework could be relevant for training on non-standard architectures where equivariant or topological network layers may not be easily differentiable, and the spectral perspective on gradient estimation may inspire new approaches to optimisation on manifolds and complexes.

---

### 7. MetricPose: Flexible 3D Human Pose Estimation with Depth and Geometric Cues

| 항목 | 내용 |
|------|------|
| **저자** | Shifan Zhu et al. |
| **발행일** | 2026-11-06 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.420 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08954v1) \| [PDF](https://arxiv.org/pdf/2611.08954v1) |

**요약:** MetricPose extends a pretrained 3D human pose estimator with optional depth and geometric-constraint modules to predict metrically accurate joint positions in camera coordinates, reducing camera-local error by up to 55%.

**핵심 기여:**

- Introduces a unified architecture supporting RGB, RGB-Ground, and RGB-D inputs via shared parameters, with optional metric depth and geometry-processing modules that gracefully degrade to RGB-only operation.

- Decouples the scale–distance ambiguity inherent in monocular 3D pose estimation by fusing three complementary signals: learned RGB priors, direct depth measurements, and environmental geometric constraints (e.g., ground-plane contact).

- Proposes a depth-guided body refinement mechanism and a camera-distance estimation module that leverage metric depth maps and geometric cues without retraining the base RGB backbone.

- Achieves 12.16%, 31.00%, and 54.61% reductions in camera-local joint-position error over the SAM 3D Body foundation model in RGB, RGB-Ground, and RGB-D modes respectively.


**팀 관련성:** This paper has limited direct relevance to the team's core topics in geometric/topological deep learning. However, its use of geometric constraints (ground-plane contact, SE(3)-relevant camera-frame reasoning) and multi-modal fusion for 3D geometric inference may offer peripheral inspiration for how geometric priors and inductive biases can be injected into 3D perception systems—a theme loosely connected to the team's interest in geometric priors in deep learning and E(3)-aware architectures.

---

### 8. Geometry-Aware Score-Repellent Monte Carlo

| 항목 | 내용 |
|------|------|
| **저자** | Jie Hu, Lingyun Chen, Do Young Eun |
| **발행일** | 2026-11-06 |
| **카테고리** | stat.ML, cs.LG |
| **관련성 점수** | 0.419 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08909v1) \| [PDF](https://arxiv.org/pdf/2611.08909v1) |

**요약:** GA-SRMC generalizes Score-Repellent Monte Carlo by replacing scalar repulsion with a Fisher-information-preconditioned matrix alignment, provably optimal for anisotropic targets, yielding up to 6.8× ESS gains.

**핵심 기여:**

- Generalizes the SRMC repulsion mechanism from scalar α to a symmetric positive-definite matrix M, enabling direction-dependent repulsion strength that adapts to anisotropic energy landscapes.

- Proves via a stochastic-approximation CLT that the trace-normalized inverse Fisher information matrix M_opt ∝ S⁻¹ uniquely minimizes the worst-direction asymptotic covariance bound, elevating Fisher information from a proposal-side preconditioner to the optimal repulsion-side matrix.

- Shows that a single online estimate of the Fisher information matrix can serve dual roles (proposal preconditioning à la FisherMALA + repulsion geometry), adding no extra computational cost over standard adaptive MCMC.

- Demonstrates consistent ESS improvements across 8 targets (κ ∈ [1.3, 100], d ∈ [2, 785]): 4.3× on anisotropic Gaussians, 6.8× on MNIST, 16–32% on well-conditioned posteriors, and lower posterior-mean MSE in all 16 tested configurations.


**팀 관련성:** Tangential relevance: while the paper applies Riemannian/Fisher geometry to sampling — conceptually adjacent to the team's interest in diffusion on Riemannian manifolds for generative models — it addresses MCMC mixing rather than geometric deep learning or TDA. It may be of niche interest for team members exploring geometry-aware sampling in manifold-based generative pipelines or Bayesian inference for geometric models.

---

### 9. SSF-Net: A Spatial-Spectral Fusion Network for Accurate PDE Operator Learning

| 항목 | 내용 |
|------|------|
| **저자** | Siqi Zhao, Flora D. Salim |
| **발행일** | 2026-11-06 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.415 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08912v1) \| [PDF](https://arxiv.org/pdf/2611.08912v1) |

**요약:** SSF-Net combines a multi-directional Mamba spatial branch with a Fourier-domain block-diagonal MLP spectral branch in a multiresolution encoder-decoder for efficient and accurate PDE operator learning.

**핵심 기여:**

- Proposes a dual-branch Spatial-Spectral Fusion (SSF) block that pairs a multi-directional Mamba scanner (for local, causal-bias-mitigated interactions at linear complexity) with a Fourier-transform-based block-diagonal MLP (for global spectral coupling with reduced parameters).

- Embeds the SSF block within a multiresolution convolutional encoder-decoder to extract and fuse multi-scale spatial features, enabling the model to capture both fine-grained local dynamics and coarse global structure.

- Demonstrates that multi-directional scanning in the Mamba branch alleviates the inherent single-direction causal bias of state-space models, making them more suitable for spatially symmetric PDE domains.

- Achieves lower prediction error with fewer parameters and near-linear complexity in spatial tokens compared to attention-based (e.g., transformer/FNO variants) and convolution-based baselines across a comprehensive PDE benchmark, including long-horizon rollout stability.


**팀 관련성:** This paper is relevant to the team's interests in spectral and spatial methods for learning on structured domains. The dual spatial-spectral design parallels ideas in spectral vs. spatial graph convolutions, and the multiresolution/multi-scale architecture connects to signal processing on complexes and manifolds. The Fourier-domain branch and block-diagonal parameterization offer insights transferable to spectral methods on graphs and higher-order structures, while the treatment of directional bias in sequential scanning may inform design choices for processing signals on oriented simplicial or cell complexes.

---

### 10. GeoJeV: Unified Spatial Probability for Training-Free Efficient Evidence Acquisition in Ultra-High-Resolution Remote Sensing

| 항목 | 내용 |
|------|------|
| **저자** | Xinyi Niu et al. |
| **발행일** | 2026-11-06 |
| **카테고리** | cs.CV, eess.SP |
| **관련성 점수** | 0.409 |
| **arXiv** | [링크](https://arxiv.org/abs/2611.08879v1) \| [PDF](https://arxiv.org/pdf/2611.08879v1) |

**요약:** GeoJeV introduces a training-free spatial probability framework that replaces RLHF-aligned generative search with distribution-driven decision making for efficient evidence acquisition in ultra-high-resolution remote sensing imagery.

**핵심 기여:**

- Formulates evidence acquisition in UHR remote sensing as spatial probability-driven decision making using a frozen JeV model, eliminating the need for RLHF-aligned intermediate generation and autoregressive decoding overhead.

- Proposes three coordinated mechanisms—Region Rank (search priority), Sparse Branch (adaptive branching width via sparse probability support), and Depth Gate (refinement depth control via sparsity and concentration)—all derived from a single shared probability distribution over candidate regions.

- Achieves a 7.8× inference speedup over prior methods while improving average accuracy of Qwen3-VL-8B by +5.32 percentage points across three remote sensing benchmarks (LRS-GRO, MME-RealWorld-RS, LRS-VQA) with only ~1.12s additional overhead per query.

- Demonstrates that principled probabilistic search control can outperform learned/generative search strategies, suggesting that explicit spatial probability modeling is more effective than relying on LLM generation for region-level relevance judgments.


**팀 관련성:** While this paper targets remote sensing rather than RecSys, the core idea of replacing learned generative search with principled probability-driven spatial exploration has conceptual parallels to efficient candidate retrieval and search-space pruning in recommendation. However, direct relevance to the team's geometric/topological deep learning focus is low — the spatial probability framework here is task-specific and does not leverage geometric priors, equivariance, or topological structures central to the team's research agenda.

---


## 🏭 Industry Blog Highlights



## 📈 이번 주 트렌드 분석

### Emerging Trends

- Explainability for higher-order and topological architectures: TopoSHAP signals a maturing of the TDL field beyond predictive performance toward interpretability, with Shapley-based attribution now extended to simplicial and cell complexes—expect more XAI-for-TDL work to follow.

- Richer topological featurization through novel filtration strategies: The alternative filtration paper reflects a growing recognition that the standard lower-star filtration is a bottleneck, and that persistence diagrams can be made substantially more expressive by decoupling simplex and boundary-face introduction.

- Geometry-aware preconditioning and importance weighting in latent/generative models: Both LIR (Jacobian-based latent dimension weighting) and GA-SRMC (Fisher-information-preconditioned repulsion) demonstrate a trend toward using local geometric structure—curvature, Jacobians, Fisher information—to guide learning and sampling in latent and generative settings.

- Multi-task gradient balancing via dynamical systems analysis: GMAdam's slow-manifold singular perturbation framework for understanding optimizer behavior in multi-objective settings represents a sophisticated new lens for analyzing training dynamics in architectures with competing loss terms across scales or cell dimensions.

- Bridging spectral methods and optimization: SZO-κ's use of activation-space spectral structure for zeroth-order gradient estimation hints at deeper connections between spectral graph/manifold methods and optimization, potentially relevant for non-differentiable topological loss functions.


### 팀 액션 아이템


---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + 0개 기술 블로그 → 시맨틱 필터링(threshold=0.35) → LLM 요약*