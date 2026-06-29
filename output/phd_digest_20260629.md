# 📚 RecSys Research Digest — 2026-06-22 ~ 2026-06-29

> 자동 생성: 2026-06-29 00:04 | 팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

This week's RecSys research landscape reveals a strong convergence around equivariance, graph neural network expressiveness, and geometric structure-awareness — all core pillars of our team's research agenda. Two papers directly advance equivariant network theory: the Bayesian neural network equivariance paper provides rigorous variational inference conditions and practical symmetrization strategies, while the quantum GNN paper demonstrates that permutation equivariance and Weisfeiler-Leman expressivity can be achieved in quantum message-passing architectures at non-trivial scale. The comprehensive GNN survey offers a timely unified lens connecting spectral/spatial formulations to the WL hierarchy across twelve domains, serving as both a reference and a map of open problems relevant to our spectral, spatial, and higher-order network research threads.

A second notable theme is the creative application of transformer and autoregressive architectures to geometric and topological structures. SubdivAR's autoregressive mesh subdivision with topology-aware local aggregation and the FRST triangulation paper's use of transformers for exploring Calabi-Yau classifications both demonstrate that generative modeling over discrete geometric/topological objects is maturing rapidly. These approaches are highly relevant to our interests in simplicial/cell complexes, manifold-aware learning, and topological deep learning, as they suggest new generative paradigms for structured geometric data beyond point clouds and graphs.

Finally, the temporal GNN explainability paper and the self-supervised CT reconstruction paper highlight growing attention to interpretability and label-efficiency in structured learning. The temporal GNN attribution method's focus on information flow through event-associated variables resonates with our work on signal processing over higher-order networks and Hodge decomposition, as it effectively traces signal propagation pathways through dynamic graph structures. The NeRF geometry sculpting paper, while application-specific, reinforces the trend of integrating human feedback and geometric priors (3D density fields) directly into learning pipelines — a design philosophy aligned with our emphasis on geometric inductive biases.

---

## 📄 Top Papers This Week


### 1. Equivariance and Augmentation for Bayesian Neural Networks

| 항목 | 내용 |
|------|------|
| **저자** | Miaowen Dong, Axel Flinth, Jan E. Gerken |
| **발행일** | 2026-06-24 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.562 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.26273v1) \| [PDF](https://arxiv.org/pdf/2606.26273v1) |

**요약:** This paper derives theoretical conditions under which Bayesian neural networks trained with variational inference and data augmentation achieve exact equivariance, and proposes three symmetrization techniques (including orbit expansion) that improve equivariance and performance.

**핵심 기여:**

- Establishes formal conditions for exact equivariance in BNNs with exponential family variational distributions trained on augmented data, bridging the gap between the equivariant architecture vs. augmentation debate.

- Derives quantitative bounds on the equivariance error for BNNs under data augmentation, providing theoretical guarantees beyond the infinite-ensemble limit studied in prior work.

- Introduces three novel symmetrization techniques—orbit expansion, prediction symmetrization, and distribution symmetrization—to boost equivariance in variational BNNs, with orbit expansion consistently outperforming baselines in both equivariance and task performance.

- Provides extensive experiments validating the theoretical findings and demonstrating that principled augmentation strategies for BNNs can approach the equivariance of architecturally constrained models without hard-coding symmetries.


**팀 관련성:** Directly relevant to the team's work on equivariant neural networks and geometric priors/inductive biases. This paper offers a rigorous Bayesian perspective on the fundamental question of whether symmetries should be built into architectures (e.g., E(3)-equivariant or gauge-equivariant networks) or learned via augmentation, with practical techniques applicable to settings where designing exact equivariant architectures is difficult.

---

### 2. Scalable Message-Passing Quantum Graph Neural Networks in the Weisfeiler-Leman Hierarchy

| 항목 | 내용 |
|------|------|
| **저자** | Snehal Raj et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | quant-ph, cs.LG |
| **관련성 점수** | 0.558 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.26873v1) \| [PDF](https://arxiv.org/pdf/2606.26873v1) |

**요약:** A quantum GNN framework is designed to perform message passing with permutation equivariance and provable expressivity at any chosen level of the Weisfeiler-Leman hierarchy, validated at scale up to 56 qubits.

**핵심 기여:**

- Constructs quantum circuit architectures that natively implement message-passing on graphs while provably maintaining permutation equivariance, directly mirroring classical MPNN design principles but in the quantum domain.

- Provides formal expressivity guarantees by showing the quantum GNN can be placed at a chosen level of the Weisfeiler-Leman (WL) hierarchy (k-WL), the standard benchmark for graph distinguishing power — extending the classical GNN–WL connection to quantum models.

- Demonstrates a pre-training strategy on small graph instances that transfers to larger graphs, mitigating the barren plateau trainability bottleneck of variational quantum circuits, with readout costs that remain low as graph size grows.

- Validates the framework empirically at up to 56 qubits on three tasks — separating WL-indistinguishable graphs, molecular property prediction, and the travelling salesperson problem — showing competitive or superior performance to classical baselines.


**팀 관련성:** Directly relevant to the team's work on message-passing neural networks, graph representation learning, and geometric/symmetry-aware inductive biases. The paper rigorously transplants the classical MPNN and WL expressivity theory into the quantum setting with equivariance guarantees, offering a new angle on how symmetry group representations and graph-theoretic priors can be embedded in alternative computational substrates — potentially informing future hybrid geometric deep learning architectures.

---

### 3. Graph Neural Networks Applications Across Domains: All Insights You Need

| 항목 | 내용 |
|------|------|
| **저자** | Abderaouf Bahi |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.510 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27202v1) \| [PDF](https://arxiv.org/pdf/2606.27202v1) |

**요약:** A comprehensive GNN survey unifying spectral/spatial formulations, connecting expressiveness to the Weisfeiler-Leman hierarchy, and critically evaluating architectural choices across twelve application domains.

**핵심 기여:**

- Derives spectral and spatial GNN formulations from shared first principles and formally connects architectural expressiveness to the Weisfeiler-Leman hierarchy, explicitly delineating what current message-passing architectures can and cannot distinguish.

- Systematically evaluates twelve application domains (including recommendation, drug discovery, traffic, materials science, etc.), specifying graph-construction choices, dominant architecture families, and separating genuine gains from artefacts of weak baselines or favourable data splits.

- Identifies recurring cross-domain failure modes—heterophily, scale limitations, temporal graph difficulty, and the gap between leaderboard-topping and deployment-ready architectures—providing a practical diagnostic for practitioners.

- Treats over-smoothing, over-squashing, robustness, distribution shift, fairness, and explainability as first-class adoption constraints rather than afterthoughts, framing them as the bottlenecks that determine real-world viability.


**팀 관련성:** Directly relevant to the team's work on message-passing neural networks, spectral/spatial graph convolutions, and geometric priors. The survey's critical analysis of WL-expressiveness limits strengthens the motivation for our research into higher-order topological architectures (simplicial/cell complex networks, sheaf neural networks) as pathways beyond standard MPNN expressiveness. The cross-domain failure-mode analysis (over-smoothing, over-squashing, heterophily) also connects to our work on Hodge Laplacians, topological filters, and higher-order signal processing as principled remedies.

---

### 4. SubdivAR: Autoregressive Next-Scale Prediction for Neural Mesh Subdivision

| 항목 | 내용 |
|------|------|
| **저자** | Huipeng Guo et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.460 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27088v1) \| [PDF](https://arxiv.org/pdf/2606.27088v1) |

**요약:** SubdivAR reformulates mesh subdivision as autoregressive next-scale prediction using a novel mesh representation and a hybrid transformer combining global attention with topology-aware local aggregation.

**핵심 기여:**

- Introduces Mesh Autoregressive Representation (MAR), which arranges multi-level subdivision meshes into an ordered scale sequence, enabling autoregressive next-scale coordinate prediction of vertex offsets that respects subdivision topology.

- Proposes a Hybrid Topology-Aware Transformer that fuses global semantic self-attention with topology-constrained local feature aggregation (message passing guided by mesh connectivity), bridging global context and local geometric structure.

- Constructs FII-40K, a large-scale dataset of ~40,000 high-quality meshes with multi-level subdivision ground truth, addressing the lack of standardized training data for neural subdivision.

- Achieves state-of-the-art results with 18.8% and 14.2% reductions in Hausdorff and Chamfer distances respectively, with demonstrated robustness on complex open-surface geometries where prior methods struggle.


**팀 관련성:** Directly relevant to our work on geometric deep learning on meshes and manifolds: the hybrid transformer architecture explicitly combines graph-based message passing (topology-constrained aggregation over mesh connectivity) with global attention, offering a concrete design pattern for balancing local geometric inductive biases with long-range context. The multi-scale autoregressive formulation over simplicial structures also connects to our interests in hierarchical representations on cell/simplicial complexes and signal processing at multiple topological resolutions.

---

### 5. Sculpting NeRF Geometry: Human-Preference Fine-Tuning of a 3D-Aware Face GAN

| 항목 | 내용 |
|------|------|
| **저자** | Archer Moore, Mingming Gong, Liam Hodgkinson |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.436 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27305v1) \| [PDF](https://arxiv.org/pdf/2606.27305v1) |

**요약:** Fine-tunes a 3D-aware face GAN (EG3D) using RLHF applied directly to NeRF density fields, improving 3D geometry without mesh extraction, text conditioning, or multi-view rendering.

**핵심 기여:**

- Introduces a reward model that operates directly on continuous 3D density (σ) fields of a NeRF, bypassing the typical mesh-extraction or multi-view rendering steps used in prior 3D RLHF pipelines.

- Proposes a density-consistency constraint that preserves 2D appearance fidelity while reshaping the underlying 3D geometry, bounding distributional drift (FID-50k: 4.09 → 6.66).

- Demonstrates that a lightweight reward model trained on a small set of pairwise preference samples from a single annotator can yield geometries preferred 74.4% of the time in user studies.

- Operates entirely in the implicit radiance-field representation space, requiring no external mesh supervision, shape priors, or surface-supervised pretraining — keeping the pipeline simple and representation-native.


**팀 관련성:** While not directly in the team's core areas, the paper's approach of learning geometric structure directly from continuous volumetric density fields (rather than explicit surface representations) connects to the team's interests in geometric priors, implicit 3D representations, and signal processing on continuous domains. The density-consistency constraint can be viewed as a geometric inductive bias preserving the learned manifold structure, and the work raises interesting questions about how topological or geometric invariants of density fields (e.g., persistent homology of level sets) could serve as more principled reward signals for 3D shape quality.

---

### 6. Generating Special Triangulations with Transformers

| 항목 | 내용 |
|------|------|
| **저자** | Charles Arnal et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | hep-th, cs.LG, math.AG |
| **관련성 점수** | 0.431 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.26660v1) \| [PDF](https://arxiv.org/pdf/2606.26660v1) |

**요약:** Transformers with tailored encoding schemes are trained to generatively produce fine, regular, star triangulations (FRSTs) of 4D reflexive polytopes, enabling self-improving exploration of Calabi-Yau threefold classifications.

**핵심 기여:**

- Proposes an encoding scheme that maps the high-dimensional, combinatorially complex structure of triangulations into token sequences suitable for autoregressive transformer generation, addressing a non-trivial representation challenge for geometric-combinatorial objects.

- Demonstrates that transformers can representatively generate valid FRSTs across polytopes of varying size, producing novel triangulations not seen during training — a task where classical enumeration methods struggle due to combinatorial explosion.

- Introduces a self-improvement loop where the model is retrained on its own verified outputs, progressively expanding coverage of the triangulation space without additional ground-truth data.

- Provides a concrete pipeline relevant to string theory (Calabi-Yau classification) by connecting generative ML to the systematic exploration of triangulations of reflexive polytopes.


**팀 관련성:** This work sits at the intersection of generative modeling and combinatorial/geometric structures (simplicial complexes, triangulations of polytopes) that are core to the team's interests in topological deep learning, simplicial complexes in ML, and geometric priors. The encoding of triangulations for sequence models and the self-improving generation loop offer methodological insights transferable to generative approaches over simplicial/cell complexes and higher-order topological objects studied by the group.

---

### 7. Enabling self-supervised learned primal dual with Noise2Inverse

| 항목 | 내용 |
|------|------|
| **저자** | Antti Sällinen et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | eess.IV, cs.LG, math.OC |
| **관련성 점수** | 0.424 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.26991v1) \| [PDF](https://arxiv.org/pdf/2606.26991v1) |

**요약:** Extends the Noise2Inverse self-supervised framework to the Learned Primal-Dual algorithm for ground-truth-free CT reconstruction in low-dose and sparse-angle settings.

**핵심 기여:**

- Proposes N2I-LPD, combining the Learned Primal-Dual iterative reconstruction architecture with the Noise2Inverse self-supervised training strategy, eliminating the need for ground-truth CT images during training.

- Exploits statistical independence of noise across angular projections to construct data-splitting schemes that enable self-supervised loss computation within a learned primal-dual unrolled optimization framework.

- Demonstrates that N2I-LPD outperforms both classical reconstruction methods (e.g., FBP) and self-supervised U-Net baselines (N2I + U-Net) in low-dose and sparse-angle CT scenarios.

- Highlights the practical viability of learned iterative reconstruction operators in real-world CT imaging where paired ground-truth data is unavailable.


**팀 관련성:** This paper has limited direct relevance to the team's core focus on geometric/topological deep learning. However, the learned primal-dual framework is an unrolled optimization scheme operating on structured (sinogram/image) domains, and the noise-splitting strategy could conceptually inspire self-supervised approaches for inverse problems on manifolds or graphs — settings where ground-truth signals are similarly scarce. Teams exploring diffusion processes on Riemannian manifolds for generative models may find the self-supervised inverse problem formulation tangentially interesting.

---

### 8. Explaining Temporal Graph Neural Networks via Feature-induced Information Flow

| 항목 | 내용 |
|------|------|
| **저자** | Ping Xiong et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.416 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27201v1) \| [PDF](https://arxiv.org/pdf/2606.27201v1) |

**요약:** A novel attribution method explains Event-based Temporal GNNs by tracing the complete information flow through all event-associated variables, including often-overlooked event-induced pathways that capture long-range temporal dependencies.

**핵심 기여:**

- Identifies a critical gap in existing ETGNN explanation methods: they only trace contributions from event-related embeddings to output, missing information pathways through event-induced variables (e.g., memory states) that mediate inter-node interactions and long-range temporal dependencies.

- Extends the Normalized Relevance Measure (NRM) framework to quantify information flow from both event embeddings and event-induced variables, ensuring cross-layer comparability of latent variables and supporting higher-order interaction analysis between events.

- Introduces a modular decomposition procedure that systematically constructs relevance structures for architecturally complex ETGNNs, making the NRM framework practically applicable to real-world temporal graph architectures.

- Demonstrates consistent improvements over existing explanation methods on synthetic (epidemic tracing, social dynamics) and real-world (political event networks) benchmarks, with more human-interpretable explanations.


**팀 관련성:** Directly relevant to the team's work on graph representation learning and message passing neural networks. The paper advances explainability for temporal graph models used in recommender systems and social networks, and its modular decomposition approach for analyzing information flow through complex graph architectures could inform interpretability strategies for other structured neural networks the team studies (e.g., simplicial or cell complex networks with similarly complex message-passing schemes).

---

### 9. Kolmogorov Arnold networks (KAN) for aerodynamic prediction: a comparison with MLPs and GNNs

| 항목 | 내용 |
|------|------|
| **저자** | Miguel Jaraiz et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.LG, physics.data-an, physics.flu-dyn |
| **관련성 점수** | 0.415 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27126v1) \| [PDF](https://arxiv.org/pdf/2606.27126v1) |

**요약:** KANs are benchmarked against MLPs and GNNs for aerodynamic surface pressure prediction, showing comparable but slightly inferior accuracy to MLPs, with GNNs achieving best performance albeit at higher training cost.

**핵심 기여:**

- Provides the first systematic comparison of Kolmogorov-Arnold Networks (KANs) against MLPs and GNNs on a fluid dynamics surrogate modeling task (airfoil pressure coefficient prediction across Mach numbers and angles of attack).

- Demonstrates that KAN models achieve good interpolation capability across flight conditions with significantly lower model complexity than MLPs and GNNs, resulting in faster training times.

- Identifies critical practical limitations of KANs: training instabilities and high sensitivity to hyperparameter selection, which currently hinder their reliability compared to established architectures.

- Shows that GNNs—leveraging mesh-based graph structure—achieve the best overall predictive performance, reinforcing the value of geometric inductive biases for spatially-structured physical problems.


**팀 관련성:** This paper is directly relevant to our team's work on graph neural networks and geometric inductive biases. The finding that GNNs outperform both KANs and MLPs on spatially-structured aerodynamic data reinforces the importance of encoding geometric priors (e.g., mesh topology via message passing) into network architectures—a central theme across our research on spectral/spatial graph convolutions and geometric deep learning. The KAN comparison also provides useful context as this emerging architecture gains attention across scientific ML.

---

### 10. RayPE: Ray-Space Positional Encoding for 3D-Aware Video Generation

| 항목 | 내용 |
|------|------|
| **저자** | Minghao Yin et al. |
| **발행일** | 2026-06-25 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.407 |
| **arXiv** | [링크](https://arxiv.org/abs/2606.27345v1) \| [PDF](https://arxiv.org/pdf/2606.27345v1) |

**요약:** RayPE injects 6D Plücker ray coordinates into video diffusion transformer attention via an additive positional encoding whose bilinear structure naturally recovers the geometric reciprocal product between camera rays.

**핵심 기여:**

- Identifies a precise algebraic analogy between the Plücker reciprocal product (a bilinear form measuring geometric relations between 3D rays) and the dot-product attention mechanism in Transformers, motivating a principled geometric positional encoding.

- Proposes an additive query/key injection of per-token 6D Plücker coordinates with a query/key flip arrangement, decomposing attention into content, geometry, and cross-terms — all shown to be individually necessary via ablation.

- Introduces a scale-robust normalization pipeline (decoupling ray direction from moment magnitude, log-magnitude gating, and RMSNorm alignment with QKNorm) to handle heterogeneous camera-translation scales from diverse data sources (SfM, deep SLAM, metric).

- Achieves improved camera controllability and cross-frame 3D consistency on a four-dataset mixture while adding <0.1% parameters to a pretrained video DiT, using zero-initialization for seamless fine-tuning from pretrained weights.


**팀 관련성:** This work is highly relevant to the team's interests in geometric priors and inductive biases in deep learning, and in leveraging the structure of geometric groups (here, the ray space of SE(3) camera poses via Plücker coordinates) to design architecturally principled modules. The explicit use of the bilinear structure of Plücker geometry as an attention mechanism exemplifies how projective/Euclidean geometric invariants can be embedded directly into neural network computations — connecting to the team's work on equivariant networks, geometric deep learning, and diffusion processes on manifolds for generative models.

---


## 🏭 Industry Blog Highlights



## 📈 이번 주 트렌드 분석

### Emerging Trends

- Rigorous equivariance guarantees in probabilistic and approximate inference settings: The Bayesian NN equivariance paper moves beyond deterministic equivariant architectures to establish when and how equivariance is preserved (or can be restored) under variational inference and data augmentation — opening a new theoretical frontier for our equivariant network research.

- Weisfeiler-Leman expressivity as a unifying benchmark across classical, quantum, and survey-level GNN research: Both the quantum GNN paper and the comprehensive GNN survey center on the WL hierarchy as the gold standard for expressivity analysis, signaling its consolidation as the primary lens for comparing message-passing architectures including potential higher-order extensions.

- Autoregressive and transformer-based generative models operating directly on discrete geometric and topological structures (meshes, triangulations, polytopes): SubdivAR and the FRST triangulation paper show that sequence-based generative modeling can be effectively adapted to complex combinatorial geometric objects, suggesting near-term opportunities for generative models over simplicial and cell complexes.

- Information flow tracing and attribution methods for temporal and dynamic graph neural networks: The temporal GNN explainability paper introduces event-induced information pathways that capture long-range dependencies, paralleling concepts from signal processing on higher-order networks and Hodge-theoretic flow decomposition.

- Integration of human feedback and geometric priors directly into 3D-aware generative pipelines: The NeRF/RLHF paper exemplifies a broader trend of embedding geometric structure (density fields, 3D-awareness) into reward-driven fine-tuning, relevant to our focus on geometric inductive biases in deep learning.


### 팀 액션 아이템


---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + 0개 기술 블로그 → 시맨틱 필터링(threshold=0.35) → LLM 요약*