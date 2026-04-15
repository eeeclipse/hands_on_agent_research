# 📚 RecSys Research Digest — 2026-03-08 ~ 2026-03-23

> 자동 생성: 2026-03-23 10:41 | 팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

This week's research landscape is notably dominated by 3D geometric reasoning and manifold-aware methods, with several papers directly intersecting our team's core competencies in geometric deep learning, Riemannian manifolds, and higher-order network structures. While none of the papers are squarely in the recommender systems domain, the methodological innovations—particularly in manifold-aware representations, hypergraph controllability theory, and graph neural networks on irregular structures—carry significant transferable ideas for our geometric and topological deep learning agenda.

The strongest signals for our team come from three papers. First, **ReManNet** formulates monocular 3D lane detection as inference on a Riemannian manifold using SPD-manifold Gaussian descriptors, directly connecting to our work on diffusion processes on Riemannian manifolds and gauge equivariant networks. Second, the **Structural Controllability of Large-Scale Hypergraphs** paper extends classical graph controllability to hypergraphs via polynomial dynamical systems, offering fresh theoretical machinery relevant to our higher-order interactions and hypergraph signal processing research. Third, the **GNN for subgrid-scale modeling** paper demonstrates message passing on non-uniform/complex meshes with strong generalization, reinforcing the value of graph-based geometric priors on irregular domains—a theme central to our spectral/spatial GCN and MPNN work. Additionally, **Cov2Pose**'s use of SPD matrix pooling and manifold-aware Cholesky encodings provides concrete architectural patterns for incorporating Riemannian geometry into end-to-end pipelines, and the **Discrete MMD distillation** paper extends diffusion model distillation to discrete spaces, potentially informing our generative modeling on discrete topological structures.

Papers on LiDAR snow removal, novel view synthesis, and quantum architecture search are more peripheral but still touch on point cloud learning and 3D geometric inductive biases. Overall, the week highlights a clear trend: the community is increasingly embedding explicit geometric and manifold structure into neural architectures rather than relying on data augmentation or implicit learning alone.

---

## 📄 Top Papers This Week


### 1. LIORNet: Self-Supervised LiDAR Snow Removal Framework for Autonomous Driving under Adverse Weather Conditions

| 항목 | 내용 |
|------|------|
| **저자** | Ji-il Park, Inwook Shim |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.CV, cs.RO |
| **관련성 점수** | 0.498 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19936v1) \| [PDF](https://arxiv.org/pdf/2603.19936v1) |

**요약:** LIORNet uses a self-supervised U-Net++ with physics-informed pseudo-labels to remove snow noise from LiDAR point clouds without manual annotation, achieving state-of-the-art filtering on autonomous driving benchmarks.

**핵심 기여:**

- Proposes a self-supervised learning framework that generates pseudo-labels from multiple physical/statistical cues (range-dependent intensity thresholds, snow reflectivity, point sparsity, sensing range) to eliminate the need for costly manual snow-point annotation.

- Integrates distance-based, intensity-based, and learning-based filtering paradigms into a unified U-Net++ architecture, combining the complementary strengths of each approach.

- Demonstrates state-of-the-art snow removal performance on WADS and CADC datasets with improved accuracy and runtime efficiency over existing methods, preserving critical environmental structure.

- Achieves practical real-time capability for autonomous driving deployment by avoiding heavy computational overhead typical of prior learning-based approaches.


**팀 관련성:** While this paper operates on point clouds — a core data modality for geometric deep learning — its technical approach (U-Net++ with handcrafted pseudo-labels) does not engage with the team's primary interests in equivariant architectures, topological representations, or geometric priors. Its relevance is limited to providing a practical preprocessing/denoising benchmark for downstream point cloud learning tasks the team may work on, but it offers minimal methodological overlap with GDL or TDA research.

---

### 2. Beyond Single Tokens: Distilling Discrete Diffusion Models via Discrete MMD

| 항목 | 내용 |
|------|------|
| **저자** | Emiel Hoogeboom et al. |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.LG, cs.CV, stat.ML |
| **관련성 점수** | 0.493 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.20155v1) \| [PDF](https://arxiv.org/pdf/2603.20155v1) |

**요약:** Introduces Discrete Moment Matching Distillation (D-MMD), a method that successfully distills discrete diffusion models into fewer sampling steps by adapting continuous-domain moment matching ideas to discrete state spaces.

**핵심 기여:**

- Proposes D-MMD, which uses a discrete Maximum Mean Discrepancy objective to match joint distributions over multiple tokens simultaneously, overcoming the single-token independence assumptions that cause prior discrete distillation methods to collapse.

- Demonstrates that moving beyond per-token KL divergence to a kernel-based distributional loss preserves both quality and diversity in the distilled model, unlike previous approaches that suffer from mode collapse.

- Shows that distilled discrete diffusion generators can outperform their teacher models on both text and image generation benchmarks, achieving strong results with significantly fewer sampling steps.

- Bridges the gap between continuous and discrete diffusion distillation by adapting moment matching — a highly successful continuous-domain technique — to categorical/discrete state spaces.


**팀 관련성:** Tangentially relevant: the team studies diffusion processes on Riemannian manifolds for generative models, and this work extends distillation to discrete diffusion — a complementary modality. The kernel-based distributional matching objective (MMD) could inspire analogous distillation strategies for geometric diffusion models on manifolds or graphs, where discrete structures (e.g., node/edge types in molecular generation) are common.

---

### 3. Structural Controllability of Large-Scale Hypergraphs

| 항목 | 내용 |
|------|------|
| **저자** | Joshua Pickard, Xin Mao, Can Chen |
| **발행일** | 2026-03-20 |
| **카테고리** | math.OC, cs.LG, cs.SI |
| **관련성 점수** | 0.471 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19955v1) \| [PDF](https://arxiv.org/pdf/2603.19955v1) |

**요약:** Extends structural controllability theory from graphs to hypergraphs by modeling higher-order dynamics as polynomial systems and deriving scalable driver node selection algorithms based on topological criteria.

**핵심 기여:**

- Formulates hypergraph dynamics as polynomial dynamical systems and extends classical structural controllability notions (accessibility, dilation) from linear graph-based systems to this nonlinear higher-order setting.

- Establishes a hypergraph topology-based criterion guaranteeing that Lie-algebraic and Kalman-type rank conditions for controllability are satisfied for almost all parameter choices, bridging algebraic control theory with hypergraph structure.

- Derives a topology-based lower bound on the minimum number of driver nodes and designs a scalable algorithm combining dilation-aware initialization (via maximum matching) with greedy accessibility expansion for driver node selection.

- Demonstrates scalability and effectiveness on hypergraphs ranging from tens to thousands of nodes, addressing a key gap where prior exact controllability methods were computationally impractical at scale.


**팀 관련성:** Directly relevant to the team's work on higher-order interactions and hypergraph signal processing. This paper provides a principled control-theoretic framework for hypergraph dynamics that complements our topological deep learning efforts—understanding structural controllability of hypergraphs could inform architecture design for hypergraph neural networks (e.g., identifying critical driver nodes as inductive biases) and deepen our theoretical understanding of information flow in higher-order networks.

---

### 4. LagerNVS: Latent Geometry for Fully Neural Real-time Novel View Synthesis

| 항목 | 내용 |
|------|------|
| **저자** | Stanislaw Szymanowicz et al. |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.469 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.20176v1) \| [PDF](https://arxiv.org/pdf/2603.20176v1) |

**요약:** LagerNVS achieves state-of-the-art real-time novel view synthesis by leveraging 3D-aware latent features from a pre-trained 3D reconstruction encoder, combining strong geometric inductive biases with end-to-end photometric training.

**핵심 기여:**

- Introduces a '3D-aware' latent representation by initializing the encoder from a 3D reconstruction network pre-trained with explicit 3D supervision, embedding geometric structure into the latent space without requiring explicit 3D reconstruction at inference.

- Achieves state-of-the-art deterministic feed-forward NVS (31.4 PSNR on Re10k) while rendering in real time, demonstrating that strong 3D geometric priors in network design outperform purely data-driven approaches.

- Operates both with and without known camera parameters and generalizes to in-the-wild data, showing robustness of the learned geometric latent features across diverse settings.

- Can be paired with a diffusion decoder for generative extrapolation beyond observed views, bridging deterministic geometric reasoning with probabilistic generation.


**팀 관련성:** This paper directly validates a core thesis of our research agenda: that geometric inductive biases (here, 3D-aware latent structure) substantially improve neural network performance on spatial tasks compared to geometry-agnostic architectures. The approach of distilling explicit geometric supervision into latent representations parallels our work on embedding geometric and topological priors into learned representations, and the interplay between 3D equivariant structure and end-to-end learning offers insights applicable to our SE(3)-equivariant network and geometric deep learning research.

---

### 5. Cov2Pose: Leveraging Spatial Covariance for Direct Manifold-aware 6-DoF Object Pose Estimation

| 항목 | 내용 |
|------|------|
| **저자** | Nassim Ali Ousalah et al. |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.452 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19961v1) \| [PDF](https://arxiv.org/pdf/2603.19961v1) |

**요약:** Cov2Pose introduces covariance-based SPD matrix pooling and a manifold-aware Cholesky pose encoding for direct, end-to-end 6-DoF object pose regression from RGB images.

**핵심 기여:**

- Proposes covariance pooling of convolutional features into a symmetric positive definite (SPD) matrix, capturing spatial second-order statistics typically discarded by global average pooling in direct pose regression methods.

- Introduces a novel continuous pose representation encoded as an SPD matrix via Cholesky decomposition, avoiding the discontinuities of standard rotation parameterizations (e.g., Euler angles, quaternions).

- Designs a manifold-aware regression head that respects the Riemannian geometry of the SPD manifold, operating with appropriate metrics (e.g., Log-Euclidean or affine-invariant) rather than treating SPD matrices as flat Euclidean objects.

- Demonstrates consistent improvements over direct baselines on 6-DoF pose benchmarks, including robustness under partial occlusion, validating both the second-order pooling and the continuous manifold-aware representation.


**팀 관련성:** This paper is directly relevant to the team's work on Riemannian manifold-aware learning, SE(3) geometric representations, and geometric inductive biases in deep learning. The use of SPD manifold geometry for regression heads and the Cholesky-based continuous pose encoding exemplify how respecting the underlying differential-geometric structure (here, the SPD and rotation manifolds) yields practical gains — a principle central to our research on equivariant networks, diffusion on Riemannian manifolds, and geometric priors.

---

### 6. ReManNet: A Riemannian Manifold Network for Monocular 3D Lane Detection

| 항목 | 내용 |
|------|------|
| **저자** | Chengzhi Hong, Bijun Li |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.444 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19776v1) \| [PDF](https://arxiv.org/pdf/2603.19776v1) |

**요약:** ReManNet formulates monocular 3D lane detection as inference on a Riemannian manifold by modeling roads as smooth 2D manifolds in R³ and lanes as embedded 1D submanifolds, using SPD-manifold Gaussian descriptors for geometric reasoning.

**핵심 기여:**

- Introduces the Road-Manifold Assumption: roads are smooth 2D manifolds in R³ with lanes as embedded 1D submanifolds, coupling metric and topological structure across surfaces, curves, and point sets to regularize the ill-posed 2D-to-3D lifting problem.

- Encodes local road geometry as Riemannian Gaussian descriptors on the symmetric positive-definite (SPD) manifold, capturing curvature and covariance structure of lane neighborhoods, then fuses these with visual features via a lightweight gating mechanism for coherent 3D reasoning.

- Proposes 3D Tunnel Lane IoU (3D-TLIoU) loss, a joint point-curve objective that computes slice-wise overlap of tubular neighborhoods along lanes, improving shape-level alignment beyond standard point-wise losses.

- Achieves state-of-the-art on OpenLane with +8.2% F1 over the baseline and +1.8% over the previous best, with scenario-level gains up to +6.6%, demonstrating the practical value of Riemannian geometric priors.


**팀 관련성:** This paper is a concrete application of Riemannian geometry and manifold-based learning to a real-world 3D perception task, directly relevant to our interests in geometric priors/inductive biases in deep learning, diffusion and computation on Riemannian manifolds, and SPD manifold representations. The tubular neighborhood IoU loss also connects to topological shape analysis ideas (e.g., thickened submanifolds, Hausdorff-style metrics) that resonate with our TDA work.

---

### 7. Layered Quantum Architecture Search for 3D Point Cloud Classification

| 항목 | 내용 |
|------|------|
| **저자** | Natacha Kuete Meli et al. |
| **발행일** | 2026-03-20 |
| **카테고리** | quant-ph, cs.CV, cs.LG |
| **관련성 점수** | 0.444 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.20024v1) \| [PDF](https://arxiv.org/pdf/2603.20024v1) |

**요약:** A layered quantum architecture search method, inspired by classical network morphism, progressively grows parametrised quantum circuits for 3D point cloud classification, achieving state-of-the-art PQC-based results on ModelNet.

**핵심 기여:**

- Introduces layered-QAS, a progressive circuit-growing strategy inspired by classical network morphism that searches for PQC architectures by iteratively adding and adapting layers, avoiding the need for predefined quantum architectural templates.

- Uses the PQC as the primary classification model rather than merely a feature extractor for a classical classifier, departing from prior quantum approaches to 3D point cloud tasks.

- Demonstrates that the layered growth strategy mitigates barren plateaus—a key trainability bottleneck in variational quantum circuits—by controlling circuit depth incrementally.

- Outperforms quantum-adapted local and evolutionary QAS baselines and achieves state-of-the-art results among PQC-based methods on the ModelNet 3D point cloud benchmark.


**팀 관련성:** This paper tackles 3D point cloud classification—a core geometric deep learning task our team works on—but from a quantum computing angle. While the quantum circuit paradigm is distant from our primary toolkit (equivariant networks, topological methods), the paper's central challenge of encoding geometric inductive biases without standard architectural primitives (convolution, attention) mirrors fundamental questions in our research on designing architectures with appropriate geometric priors. It offers a complementary perspective on how structured search can substitute for hand-crafted inductive biases in 3D geometric learning.

---

### 8. Modeling subgrid scale production rates on complex meshes using graph neural networks

| 항목 | 내용 |
|------|------|
| **저자** | Priyabrat Dash, Mathis Bode, Konduri Aditya |
| **발행일** | 2026-03-20 |
| **카테고리** | physics.flu-dyn, cs.LG |
| **관련성 점수** | 0.444 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19841v1) \| [PDF](https://arxiv.org/pdf/2603.19841v1) |

**요약:** A graph neural network is proposed to model subgrid-scale filtered production rates for large-eddy simulation on non-uniform meshes, generalizing across unseen fuel compositions and filter widths.

**핵심 기여:**

- Formulates LES closure modeling as learning on subdomain graphs constructed from mesh-point connectivity, enabling direct operation on non-uniform and complex geometries without remeshing to structured grids.

- Demonstrates cross-composition generalization by training on 10% and 80% hydrogen blends and testing on an unseen 50% blend, showing the GNN captures interpolative fuel-chemistry regimes.

- Shows robust generalization across varying filter widths (i.e., coarser spatial resolutions) without retraining, maintaining bounded prediction errors — a key practical requirement for multi-resolution LES.

- Outperforms both an unclosed baseline (evaluating rates at filtered state) and a CNN baseline (requiring structured remeshing), with validation on a backward-facing step geometry confirming applicability to practical configurations.


**팀 관련성:** This work is a direct application of message-passing neural networks on irregular graph-structured meshes, aligning closely with the team's interests in spatial graph convolutions and geometric inductive biases. The use of mesh connectivity as graph topology to bypass structured-grid assumptions is a compelling case study of how GNN architectures can encode geometric priors for physics on non-Euclidean domains.

---

### 9. Graph-Informed Adversarial Modeling: Infimal Subadditivity of Interpolative Divergences

| 항목 | 내용 |
|------|------|
| **저자** | Panagiota Birmpa, Eric Joseph Hall |
| **발행일** | 2026-03-20 |
| **카테고리** | stat.ML, cs.LG, math.ST |
| **관련성 점수** | 0.417 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.20025v1) \| [PDF](https://arxiv.org/pdf/2603.20025v1) |

**요약:** Proves an infimal subadditivity principle for interpolative divergences on Bayesian networks, theoretically justifying graph-structured localized discriminators in GANs over monolithic alternatives.

**핵심 기여:**

- Establishes a new infimal subadditivity inequality showing that global variational divergences (including (f,Γ)-divergences, IPMs, and proximal OT divergences) are upper-bounded by an average of family-level (local) discrepancies aligned with the Bayesian network structure, with exactness in an additive regime.

- Provides a rigorous variational justification for replacing a single monolithic GAN discriminator with localized family-level discriminators informed by a known graphical model, without requiring the optimal solution itself to factorize over the graph.

- Extends the theoretical framework beyond (f,Γ)-divergences to integral probability metrics and proximal optimal transport divergences, and identifies concrete discriminator function classes satisfying the required conditions.

- Demonstrates experimentally that graph-informed GANs with localized discriminators achieve improved training stability and better structural recovery of the target distribution compared to graph-agnostic baselines.


**팀 관련성:** This paper connects graphical model structure to adversarial generative modeling via a principled decomposition of divergence objectives — directly relevant to our interests in geometric and graph-based inductive biases in deep learning. The idea of exploiting known relational/graph structure to decompose global learning objectives into local ones resonates with message-passing and graph-structured learning paradigms central to our research.

---

### 10. GDEGAN: Gaussian Dynamic Equivariant Graph Attention Network for Ligand Binding Site Prediction

| 항목 | 내용 |
|------|------|
| **저자** | Animesh, Plaban Kumar Bhowmick, Pralay Mitra |
| **발행일** | 2026-03-20 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.416 |
| **arXiv** | [링크](https://arxiv.org/abs/2603.19817v1) \| [PDF](https://arxiv.org/pdf/2603.19817v1) |

**요약:** GDEGAN replaces dot-product attention in equivariant GNNs with Gaussian kernel-based dynamic attention that adapts bandwidth via local feature variance, significantly improving protein-ligand binding site prediction.

**핵심 기여:**

- Introduces a Gaussian dynamic attention mechanism for equivariant GNNs that replaces dot-product attention with adaptive kernels parameterized by local neighborhood feature statistics (mean, variance), allowing context-specific importance weighting per protein region.

- Uses local variance as an adaptive bandwidth parameter with learnable per-head temperatures, enabling each layer to dynamically recompute neighborhood statistics and adjust receptive field sensitivity to chemical and geometric heterogeneity of residues.

- Achieves substantial improvements over state-of-the-art equivariant GNN baselines, with 37–66% relative gains in DCC and 7–19% in DCA success rates across three standard benchmarks (COACH420, HOLO4k, PDBBind2020).

- Demonstrates that capturing distributional variation in local neighborhoods—rather than relying solely on pairwise dot-product similarity—is critical for distinguishing binding sites from non-binding regions in 3D protein structures.


**팀 관련성:** Directly relevant to our work on equivariant neural networks and geometric priors for 3D data. The Gaussian dynamic attention mechanism offers a principled alternative to dot-product attention in E(3)-equivariant message passing, with the adaptive bandwidth idea (local variance as kernel width) potentially transferable to other geometric deep learning tasks on point clouds, manifolds, or molecular graphs where local feature heterogeneity matters.

---


## 🏭 Industry Blog Highlights



## 📈 이번 주 트렌드 분석

### Emerging Trends

- Riemannian manifold-aware neural architectures are gaining traction beyond niche applications: both ReManNet (SPD-manifold Gaussian descriptors for lane detection) and Cov2Pose (Cholesky manifold pose encoding) demonstrate that explicit manifold structure in network layers yields strong performance on practical 3D tasks, suggesting broader adoption of SPD and Riemannian layers in geometric pipelines.

- Hypergraph and higher-order structural theory is maturing: the extension of structural controllability from graphs to hypergraphs via polynomial dynamical systems signals growing theoretical sophistication in higher-order network analysis, directly relevant to our hypergraph signal processing and simplicial/cell complex research.

- Graph neural networks on irregular and non-uniform domains: the subgrid-scale GNN paper shows MPNNs generalizing across unseen mesh topologies and physical conditions, reinforcing that geometric graph priors enable strong out-of-distribution generalization on complex, real-world meshes beyond standard benchmarks.

- Discrete diffusion model distillation: D-MMD's adaptation of continuous moment matching to discrete state spaces opens new directions for efficient generative modeling on discrete structures (graphs, simplicial complexes, combinatorial objects), connecting to our interest in diffusion processes for generative models.

- 3D geometric inductive biases as first-class architectural components: across LagerNVS, ReManNet, Cov2Pose, and the point cloud quantum architecture search, the recurring theme is that strong geometric priors (3D-aware latent features, manifold encodings, SE(3) structure) are being baked directly into architecture design rather than handled through augmentation or post-processing.


### 팀 액션 아이템


---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + 0개 기술 블로그 → 시맨틱 필터링(threshold=0.35) → LLM 요약*