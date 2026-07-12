# 📚 RecSys Research Digest — 2026-07-05 ~ 2026-07-12

> 자동 생성: 2026-07-12 23:46 | 팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

This week's research landscape reveals a strong undercurrent of symmetry, geometry, and manifold-aware reasoning permeating diverse areas of deep learning—themes that directly intersect with the team's core interests. The standout paper for the team is the work on near-zero Hessian eigenvalues explained through approximate symmetries (pseudo-Goldstone modes), which provides a rigorous physics-inspired lens on how continuous parametrization symmetries—and their weak breaking by nonlinearities like ReLU—shape the loss landscape geometry of neural networks. This connects deeply to the team's work on equivariant networks and symmetry group representations, offering new theoretical tools for understanding how architectural symmetries manifest in optimization dynamics.

On the topological side, two papers merit close attention. CIRCOL (Selecting Interpretable Circular Coordinates) advances persistent cohomology by framing basis selection as a minimum-weight matroid problem, directly enriching the team's toolkit in persistent homology, Vietoris-Rips complexes, and topological descriptors. Meanwhile, the UMAP kNN graph paper demonstrates that classical graph-theoretic algorithms (PageRank, k-core decomposition, clustering coefficient) applied to neighborhood graphs—normally discarded after dimensionality reduction—can unlock richer high-dimensional data exploration. This bridges the team's interests in spectral/spatial graph convolutions, message passing, and topological descriptors with practical data analysis pipelines.

Several other papers provide valuable peripheral insights. The gradient descent dynamics paper extends edge-of-stability theory to manifolds of flat minima with vector-valued outputs, relevant to understanding optimization on the geometric structures the team studies. AutoAnchor's use of cross-attention as a manifold surrogate for diffusion model unlearning connects to diffusion processes on Riemannian manifolds. The Monte Carlo training paper (gradient-free deep network training) could inspire novel approaches to training on discrete or combinatorial structures like simplicial/cell complexes where gradients are difficult. The texture perception paper (ViTs vs. CNNs) offers insights into how architectural inductive biases—a core team concern—affect learned representations.

---

## 📄 Top Papers This Week


### 1. Explaining Near-Zero Hessian Eigenvalues Through Approximate Symmetries in Neural Networks

| 항목 | 내용 |
|------|------|
| **저자** | Marcel Kühn, Bernd Rosenow |
| **발행일** | 2026-07-08 |
| **카테고리** | cs.LG, cond-mat.dis-nn |
| **관련성 점수** | 0.545 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.07845v1) \| [PDF](https://arxiv.org/pdf/2607.07845v1) |

**요약:** Near-zero Hessian eigenvalues in neural networks are explained as pseudo-Goldstone modes arising from continuous parametrization symmetries that are weakly broken by nonlinearities like ReLU.

**핵심 기여:**

- Identifies the bulk of near-zero Hessian eigenvalues as weakly lifted pseudo-Goldstone modes of continuous symmetries in the network parametrization, providing a symmetry-breaking explanation for loss landscape geometry.

- Constructs explicit zero-mode eigenvectors for deep linear networks by leveraging exact continuous symmetries (e.g., GL transformations between layers) that generate flat directions in the loss.

- Demonstrates that ReLU nonlinearities act as a weak explicit symmetry breaking: the Hessian bulk remains almost entirely within the symmetry subspace with small eigenvalues, while high-curvature directions are orthogonal to it.

- Validates the mechanism across architectures—two-layer ReLU student-teacher models, CIFAR-10 trained networks, and convolutional networks—showing the diagnostic generalizes beyond fully connected layers.


**팀 관련성:** This work provides a rigorous group-theoretic and symmetry-breaking framework for understanding loss landscape geometry, directly connecting to our team's interests in geometric priors, symmetry group representations, and equivariant network design. Understanding how continuous symmetries of the parametrization shape optimization could inform the design of equivariant architectures and clarify how built-in symmetries interact with trainability and curvature structure.

---

### 2. Wat3R: Underwater 3D Geometry Learning without Annotations

| 항목 | 내용 |
|------|------|
| **저자** | Jiangwei Ren et al. |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.521 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08772v1) \| [PDF](https://arxiv.org/pdf/2607.08772v1) |

**요약:** Wat3R introduces a cross-domain semi-supervised teacher-student framework to adapt 3D reconstruction models from air to underwater scenes without requiring any annotated underwater depth data.

**핵심 기여:**

- Proposes a teacher-student semi-supervised architecture that transfers learned 3D geometry priors from in-air feed-forward reconstruction models to underwater domains using only unlabeled underwater video footage.

- Designs a cross-view consistency loss exploiting multi-view geometric cues to compensate for information degradation caused by underwater light attenuation and scattering.

- Constructs Water3D, a diverse evaluation benchmark covering various water bodies and underwater scenarios for depth estimation and point cloud reconstruction tasks.

- Achieves state-of-the-art performance on underwater multi-view depth estimation and 3D point cloud reconstruction without any ground-truth underwater annotations.


**팀 관련성:** This paper has limited direct relevance to the team's core focus on geometric/topological deep learning (equivariant networks, TDA, simplicial/cell complexes). However, the point cloud reconstruction output and the cross-view geometric consistency formulation may offer a downstream application context for point cloud learning methods and geometric priors — researchers interested in how learned geometric representations transfer across domains may find the semi-supervised cross-domain adaptation strategy of peripheral interest.

---

### 3. Dimensionality Reduction Meets Network Science: Sensemaking on UMAP's kNN Graph

| 항목 | 내용 |
|------|------|
| **저자** | Duen Horng Chau et al. |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.LG, cs.AI, cs.DS |
| **관련성 점수** | 0.514 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08746v1) \| [PDF](https://arxiv.org/pdf/2607.08746v1) |

**요약:** This paper repurposes UMAP's internally constructed kNN graph—typically discarded after embedding—by applying classical graph algorithms (PageRank, k-core decomposition, clustering coefficient) to enhance high-dimensional data exploration.

**핵심 기여:**

- Identifies UMAP's internal kNN graph as an underutilized manifold representation that preserves high-dimensional structure without the distortion introduced by 2D projection, reframing UMAP as a graph construction tool rather than solely a visualization method.

- Demonstrates that PageRank on the kNN graph selects representative exemplars competitive with k-medoids, k-core decomposition reveals density stratification complementary to HDBSCAN clustering, and clustering coefficient detects tight-knit local neighborhoods—all without purpose-built algorithms.

- Provides quantitative and qualitative evaluation on MNIST and Fashion MNIST showing these lightweight graph-theoretic analyses match or complement dedicated methods for exemplar selection and density-based clustering.

- Bridges dimensionality reduction and network science, proposing a practical workflow where users can extract richer structural insights from a graph they already compute but typically discard.


**팀 관련성:** Directly relevant to the team's work on graph-based learning and topological data analysis. The kNN graph constructed by UMAP is essentially a discretized manifold approximation—the same object underlying Vietoris-Rips complexes, Mapper, and graph neural network pipelines. This paper's insight that classical graph-theoretic descriptors (degree centrality, core number, clustering coefficient) yield meaningful manifold-level information could inform how we extract features or initialize structures in GDL/TDA workflows, and connects naturally to higher-order analyses (e.g., clustering coefficient relates to triangle counts in simplicial complexes, k-core decomposition to filtrations relevant for persistent homology).

---

### 4. Texture Representations in Deep Vision Models: Comparing CNNs, Vision Transformers, and Human Perception

| 항목 | 내용 |
|------|------|
| **저자** | Ludovica de Paolis et al. |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.CV |
| **관련성 점수** | 0.468 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08321v1) \| [PDF](https://arxiv.org/pdf/2607.08321v1) |

**요약:** Vision Transformers (ViTs) better predict human texture perception than CNNs, suggesting architecture-driven differences in internal texture representations.

**핵심 기여:**

- Introduces a rank-based statistical framework to quantify texture information encoded in intermediate representations of CNNs and ViTs across textures of varying algorithmic complexity.

- Demonstrates that ViT internal representations are mutually aligned across different ViT architectures but diverge substantially from CNN representations, pointing to architecture as a key driver of texture encoding.

- Shows that ViTs form similar representations for textures of different complexity levels, unlike CNNs, and that ViT representations better predict human psychophysical texture recognition performance.

- Provides evidence that the inductive biases of network architecture (local convolutions vs. global self-attention) fundamentally shape how texture patterns are represented, beyond training data or task effects.


**팀 관련성:** While not directly in the team's core areas, this paper is tangentially relevant through its analysis of how architectural inductive biases (a central theme in geometric deep learning) shape internal representations. The finding that global self-attention vs. local convolution drives fundamentally different texture encodings connects to the team's interest in geometric priors and inductive biases in deep learning, and could inform how topological or equivariant architectural choices might similarly shape learned representations of structured visual data.

---

### 5. Dynamics of Gradient Descent with Large Step Size Near a Manifold of Flat Minima

| 항목 | 내용 |
|------|------|
| **저자** | Lachlan Ewen MacDonald, René Vidal |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.LG, math.DS, math.OC |
| **관련성 점수** | 0.459 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08380v1) \| [PDF](https://arxiv.org/pdf/2607.08380v1) |

**요약:** Extends the theory of gradient descent with large step sizes beyond the edge of stability to vector-valued outputs and manifolds of flat minima, with applications to deep matrix factorisation.

**핵심 기여:**

- Generalises the normal form and convergence theorems for large-step GD from isolated flat minima with scalar outputs to manifolds of flat minima with vector-valued outputs, covering practical settings like multi-output regression.

- Solves a singular PDE arising in the normal-form reduction via a novel method that exploits the geometric structure of the minima manifold, potentially of independent mathematical interest.

- Proves that for deep matrix factorisation, the set of flat minima forms a fibre bundle over a product of spheres and that the sharpness function is Morse-Bott along this manifold — providing precise geometric and topological characterisation of the loss landscape.

- Overcomes technical challenges of extending edge-of-stability analysis to non-isolated minima, showing that the manifold structure (rather than isolated points) is essential for realistic overparametrised models like matrix factorisation.


**팀 관련성:** This paper provides rigorous geometric and topological characterisations of the loss landscape (fibre bundles, Morse-Bott functions) that directly connect to our interests in geometric deep learning and topological methods. The fibre bundle structure of flat minima and the role of manifold geometry in optimisation dynamics offer theoretical grounding for understanding symmetry, overparametrisation, and implicit bias in architectures studied by the team — particularly relevant for equivariant networks where parameter symmetries create exactly these kinds of minima manifolds.

---

### 6. AutoAnchor: Stable Diffusion Unlearning Using Cross-Attention as a Manifold Surrogate

| 항목 | 내용 |
|------|------|
| **저자** | Siyuan Wen, Jiahao Zeng, Ningning Ding |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.LG, stat.ML |
| **관련성 점수** | 0.458 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08337v1) \| [PDF](https://arxiv.org/pdf/2607.08337v1) |

**요약:** AutoAnchor stabilizes diffusion model unlearning by automatically generating manifold-proximal anchors via a cross-attention consistency loss that serves as a computationally efficient surrogate for manifold proximity.

**핵심 기여:**

- Formalizes unstable diffusion unlearning under the manifold hypothesis, proving that lacking a manifold-proximal anchor causes normal-space drift that degrades unlearning — providing a geometric explanation for failure modes of anchor-free methods.

- Proposes a two-stage framework (AutoAnchor) that automatically synthesizes anchors close to the data manifold, eliminating the need for manually chosen semantic alternatives that introduce bias.

- Introduces a cross-attention consistency loss as a computationally tractable surrogate for direct manifold proximity optimization, leveraging the observation that cross-attention maps encode structural layout information that correlates with on-manifold membership.

- Demonstrates strong empirical gains: up to 31% improvement in targeted concept removal (CLIP score) and 4.18% in non-target utility retention, with plug-in compatibility into existing unlearning methods (averaging ~6.5% improvement).


**팀 관련성:** Tangentially relevant to the team's interests in diffusion processes on manifolds and geometric priors in deep learning. The paper's theoretical contribution — decomposing latent updates into tangent-space and normal-space components to explain unlearning instability — echoes manifold geometry concepts familiar to our group, though the application domain (content safety/unlearning in text-to-image models) and the methods themselves (cross-attention engineering) fall outside our core RecSys and geometric/topological deep learning focus. Most useful as an example of manifold-theoretic reasoning applied to a practical generative model problem.

---

### 7. Beyond Backpropagation: Monte Carlo Method Can Train Deep Neural Networks

| 항목 | 내용 |
|------|------|
| **저자** | Hong Zhao |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.LG, stat.ML |
| **관련성 점수** | 0.439 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08406v1) \| [PDF](https://arxiv.org/pdf/2607.08406v1) |

**요약:** A simple Monte Carlo random mutation method (no gradients) can train deep networks (20+ layers, Transformers), enabling pruning, discrete weights, and unconventional activations without backpropagation.

**핵심 기여:**

- Demonstrates that a single-GPU Monte Carlo algorithm — randomly perturb one parameter, accept if loss decreases, reject otherwise — can practically train networks with 20+ layers, wide single-hidden-layer nets (16K neurons), and simple Transformers on MNIST and character-level language modeling.

- Shows the gradient-free method trains deep networks *without* batch normalization or residual connections, bypassing vanishing/exploding gradient issues entirely.

- Enables nontrivial training scenarios difficult for BP: pure pruning-based training (only removing weights), discrete/quantized weight training, and use of non-standard activation functions like Gaussians.

- Reveals substantial parameter redundancy in deep networks, as the method's per-parameter random search still converges, suggesting most parameters occupy a broadly favorable loss landscape region.


**팀 관련성:** While not directly addressing geometric or topological deep learning, this work is relevant to our team because gradient-free training could unlock architectures with non-differentiable components — such as discrete combinatorial structures (simplicial/cell complexes), topological descriptors (persistence diagrams, Betti numbers), or hard geometric constraints (exact symmetry projections) — that are difficult to integrate into standard backpropagation pipelines. It also provides a complementary lens on the loss landscape geometry of over-parameterized networks.

---

### 8. Selecting Interpretable Circular Coordinates from Data

| 항목 | 내용 |
|------|------|
| **저자** | Vincent P. Grande, Marina Meila |
| **발행일** | 2026-07-09 |
| **카테고리** | math.AT, stat.ML |
| **관련성 점수** | 0.433 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08230v1) \| [PDF](https://arxiv.org/pdf/2607.08230v1) |

**요약:** Proposes CIRCOL, a method to select interpretable circle-valued coordinates from a dictionary of meaningful candidates by framing persistent cohomology basis selection as a minimum-weight matroid problem with provably consistent discrete estimation.

**핵심 기여:**

- Formulates the selection of interpretable circular coordinates from persistent cohomology as a minimum-weight basis problem in a vector matroid over candidate cohomology classes, bridging abstract topological features with scientifically meaningful variables.

- Introduces CIRCOL for discrete point clouds, defining a cochain inner product and proving it is a consistent estimator of the continuous L² inner product of smooth 1-forms under non-uniform sampling conditions.

- Provides a projection matrix framework that simultaneously selects low-energy dictionary coordinates spanning detected H¹ classes, diagnoses topologically trivial candidates, and identifies unexplained persistent cohomology classes.

- Validates the approach on synthetic data, molecular dynamics simulations (torsion angles), and neural recordings of head-direction cells, demonstrating practical interpretability gains.


**팀 관련성:** Directly relevant to our TDA and topological deep learning efforts: this work makes persistent cohomology outputs interpretable by grounding abstract circular coordinates in domain-specific variables. The consistent cochain inner product estimator and Hodge-theoretic formulation connect to our work on Hodge Laplacians, signal processing on simplicial complexes, and could inform how topological features are integrated as priors or inductive biases in geometric deep learning pipelines.

---

### 9. Contravariance Theory: Strong Alignment for Minimal Solutions to Hard Tasks

| 항목 | 내용 |
|------|------|
| **저자** | Dan Yamins, Aran Nayebi |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.LG, q-bio.NC |
| **관련성 점수** | 0.425 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08561v1) \| [PDF](https://arxiv.org/pdf/2607.08561v1) |

**요약:** Proves that minimal DNN solutions to sufficiently hard tasks are guaranteed to have strongly aligned privileged axes (not just weak affine alignment), with alignment propagating hierarchically through layers.

**핵심 기여:**

- Establishes that weak alignment (affine mappings between representations) implies strong alignment (privileged axis correspondence) for any two minimal-complexity solutions to sufficiently hard tasks, reducing sensitivity to the choice of inter-network comparison metric.

- Shows that representational alignment 'zippers' up the network hierarchy: end-to-end task optimization causes privileged axes to emerge layer-by-layer from output back to input, formalizing a mechanistic account of convergent representations.

- Formalizes the contravariance principle from Cao & Yamins (2024), providing a theoretical foundation for why convergent evolution between artificial and biological neural networks may be inevitable under sufficient task complexity.

- Derives conditions on task hardness and solution minimality that determine when representation comparison methods (e.g., CKA, Procrustes, linear probes) will yield consistent conclusions about network similarity.


**팀 관련성:** While not directly about geometric or topological deep learning, this paper is highly relevant to our team's interests in understanding how geometric priors and inductive biases shape learned representations. The result that minimal solutions to hard tasks converge to aligned privileged axes connects to our work on equivariant networks and symmetry group representations — it suggests that sufficiently constrained tasks may force the emergence of structured, quasi-canonical representations regardless of architectural choices, informing when geometric inductive biases are necessary versus when they emerge naturally from task pressure.

---

### 10. Classical versus Deep Mirror-Symmetry Scoring: A Benchmark of Thirteen Methods

| 항목 | 내용 |
|------|------|
| **저자** | Maximilian Woehrer |
| **발행일** | 2026-07-09 |
| **카테고리** | cs.CV, eess.IV |
| **관련성 점수** | 0.425 |
| **arXiv** | [링크](https://arxiv.org/abs/2607.08379v1) \| [PDF](https://arxiv.org/pdf/2607.08379v1) |

**요약:** A systematic benchmark of 13 mirror-symmetry scoring methods reveals that a tuned classical HOG descriptor nearly matches frozen deep features at ~300× lower cost, with discrimination concentrating in mid-scale oriented features.

**핵심 기여:**

- Introduces the first statistically grounded benchmark comparing 13 symmetry scoring methods (9 existing + 4 new) across 9 datasets under a reflection-exact protocol with chance-anchored, significance-tested discrimination metrics.

- Demonstrates that frozen deep backbone features offer only a small (though significant) margin over a classical HOG descriptor for symmetry scoring, while HOG runs ~300× faster on CPU.

- Identifies that symmetry discrimination concentrates in mid-scale oriented features: deep networks peak at low/mid layers and HOG peaks at mid cell sizes, suggesting symmetry is largely a mid-level visual property.

- Releases imgsym, an open-source toolkit for image symmetry detection and measurement, providing reproducible scorers and evaluation harness.


**팀 관련성:** This paper directly probes how well geometric symmetry priors (specifically reflection/mirror symmetry) are captured by learned versus hand-crafted representations — a question central to our team's work on equivariant networks and geometric inductive biases. The finding that symmetry discrimination is a mid-level feature phenomenon, where deep representations provide diminishing returns, offers useful intuition for designing architectures with built-in symmetry group structure and for understanding what geometric properties are (or aren't) effectively learned by standard backbones.

---


## 🏭 Industry Blog Highlights



## 📈 이번 주 트렌드 분석

### Emerging Trends

- Symmetry-aware loss landscape analysis: The pseudo-Goldstone modes paper exemplifies a growing trend of using Lie group and continuous symmetry theory to explain neural network optimization phenomena, moving beyond empirical observations of the loss landscape toward principled geometric explanations rooted in symmetry breaking.

- Repurposing internal geometric structures for downstream analysis: Both the UMAP kNN graph paper and AutoAnchor demonstrate a pattern of extracting and reusing latent geometric/topological objects (neighborhood graphs, cross-attention manifold surrogates) that models construct internally but traditionally discard—turning computational byproducts into first-class analytical tools.

- Matroid-theoretic and combinatorial optimization for topological feature selection: CIRCOL's framing of persistent cohomology basis selection as a minimum-weight matroid problem signals increasing sophistication in how TDA practitioners select and interpret topological features, moving toward provably optimal and interpretable topological coordinate systems.

- Gradient-free and unconventional training paradigms for structured architectures: The Monte Carlo training paper opens a door to training networks on discrete, combinatorial, or non-differentiable structures (simplicial complexes, cell complexes, discrete-weight networks) where backpropagation is infeasible or unnatural.

- Manifold-aware optimization theory for deep learning: Multiple papers this week (Hessian eigenvalues, gradient descent dynamics on flat minima manifolds, AutoAnchor's manifold proximity) converge on the theme that understanding the manifold structure of parameter spaces and loss landscapes is becoming central to both theoretical and applied deep learning.


### 팀 액션 아이템


---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + 0개 기술 블로그 → 시맨틱 필터링(threshold=0.35) → LLM 요약*