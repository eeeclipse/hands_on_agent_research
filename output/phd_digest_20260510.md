# 📚 RecSys Research Digest — 2026-05-03 ~ 2026-05-10

> 자동 생성: 2026-05-10 23:44 | 팀 연구 주제 기반 시맨틱 필터링 적용

---

## 🧠 Executive Summary

This week's RecSys-adjacent research landscape reveals a maturing field grappling with fundamental questions about what geometric and topological deep learning models actually learn versus what we assume they learn. A striking meta-theme emerges: **diagnostic skepticism**. Multiple papers—from the MANTRA triangulation benchmark extension showing no model achieves true topological generalization, to the invariant-based diagnostics revealing GNN benchmarks are solvable without learning from connectivity, to the GRL-Safety benchmark exposing safety blind spots across twelve methods—collectively challenge the community to rigorously validate that our models exploit the structural and topological inductive biases we design into them. This is a healthy corrective that directly impacts how our team should evaluate progress on equivariant networks, sheaf neural networks, and simplicial/cell complex architectures.

On the constructive side, several papers push the theoretical frontier of our core research areas in exciting ways. The HilbNets paper on Hilbert bundles and cellular sheaves is a landmark contribution that directly extends our sheaf neural network and gauge equivariant CNN research, providing the first rigorous convergence guarantees from discrete sheaf approximations to continuous manifold settings—essentially bridging our GDL and TDA pillars with provable foundations. The Diversity Curves paper offers a novel, principled approach to graph-level representation via isometry-invariant structural descriptors at multiple coarsening scales, connecting to our work on topological descriptors and spectral graph methods. FedGMC's dual manifold calibration introduces geometric thinking (equidistant anchors, structural templates on manifolds) into federated graph learning, a previously under-explored intersection.

The overall signal is clear: the field is transitioning from "can we build models on topological/geometric domains?" to "do these models genuinely leverage topological/geometric structure, and can we prove it?" This demands that our team invest more heavily in (1) rigorous benchmarking and diagnostic baselines for our own architectures, (2) convergence theory connecting discrete computational models to continuous geometric/topological ground truth, and (3) safety and robustness evaluation as a first-class concern rather than an afterthought.

---

## 📄 Top Papers This Week


### 1. No Triangulation Without Representation: Generalization in Topological Deep Learning

| 항목 | 내용 |
|------|------|
| **저자** | Johannes S. Schmidt et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG, math.AT |
| **관련성 점수** | 0.645 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06467v1) \| [PDF](https://arxiv.org/pdf/2605.06467v1) |

**요약:** Extends the MANTRA triangulation benchmark and reveals that both GNNs and higher-order models can saturate it given proper representations, but no existing model generalizes beyond combinatorial structure to true topological understanding.

**핵심 기여:**

- Extends the MANTRA benchmark to a larger, more diverse set of manifold triangulations with richer homeomorphism types, providing a more rigorous evaluation landscape for topological deep learning models.

- Demonstrates that both standard GNNs and higher-order message passing (HOMP) models can saturate the original benchmark when given appropriate data representations and feature assignments—contradicting prior claims of HOMP superiority on this task.

- Introduces a novel evaluation protocol based on representational diversity and triangulation refinement (e.g., stellar subdivisions) to test whether models truly capture topological invariants rather than memorizing combinatorial structure.

- Reveals a critical research gap: no existing model generalizes across different triangulations of the same manifold, indicating that current architectures lack topology-aware inductive biases that are invariant to scale and combinatorial realization.


**팀 관련성:** Directly relevant to our work on topological deep learning, simplicial/cell complex neural networks, and higher-order message passing. The paper challenges prevailing assumptions about HOMP advantages over GNNs and provides concrete evaluation protocols, highlighting the urgent need for models with true topological inductive biases—connecting to our interests in persistent homology, Hodge Laplacians, and geometric priors for representation learning.

---

### 2. Diversity Curves for Graph Representation Learning

| 항목 | 내용 |
|------|------|
| **저자** | Katharina Limbeck et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.621 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06466v1) \| [PDF](https://arxiv.org/pdf/2605.06466v1) |

**요약:** Diversity curves track structural diversity across graph coarsening levels via a novel isometry invariant ("spread"), yielding interpretable, size-invariant graph-level embeddings with provably improved expressivity.

**핵심 기여:**

- Introduces 'spread,' a novel isometry-invariant descriptor capturing metric diversity and geometry of graphs, serving as the foundation for graph-level representations.

- Proposes diversity curves—graph embeddings constructed by tracking spread across an edge-contraction coarsening hierarchy—enabling direct comparison of graphs with different sizes.

- Proves theoretically that coarsening-based diversity curves are strictly more expressive than single-scale structural descriptors alone, improving discriminative power for graph-level tasks.

- Demonstrates practical utility across four domains: clustering/visualising simulated graphs of varying sizes, distinguishing single-cell graph geometry, comparing molecular graph datasets, and characterising geometric shapes.


**팀 관련성:** Directly relevant to the team's work on geometric and topological methods for graph representation learning. The multiscale coarsening approach parallels ideas from persistent homology and filtration-based TDA, while the isometry-invariant spread descriptor connects to equivariant/invariant representation design. The unsupervised, interpretable nature of diversity curves offers a complementary tool to GNN-based and topological graph-level descriptors the team already studies.

---

### 3. On the Safety of Graph Representation Learning

| 항목 | 내용 |
|------|------|
| **저자** | Xiaoguang Guo et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.555 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06576v1) \| [PDF](https://arxiv.org/pdf/2605.06576v1) |

**요약:** GRL-Safety is a multi-axis benchmark evaluating twelve graph representation learning methods (from classical embeddings to graph foundation models) across five safety dimensions: robustness, OOD generalization, class imbalance, fairness, and interpretability.

**핵심 기여:**

- Introduces GRL-Safety, a standardized benchmark spanning 12 GRL methods (topology-only embeddings, supervised GNNs, self-supervised models, and graph foundation models) across 25 datasets, evaluating five safety axes: corruption robustness, OOD generalization, class imbalance, fairness, and interpretation.

- Provides per-axis and sub-condition reporting rather than a single aggregate score, enabling fine-grained diagnosis of how specific representation design choices interact with specific deployment stresses (e.g., feature corruption vs. structural perturbation).

- Reveals that foundation-era models (GFMs, self-supervised methods) exhibit axis-specific strengths rather than broad safety dominance—no single method family uniformly outperforms across all safety dimensions.

- Identifies persistent capability gaps across all method families: several deployment regimes (e.g., severe structural OOD shifts, extreme class imbalance) remain challenging even for the best methods, pointing toward the need for new robustness and adaptation objectives beyond model selection.


**팀 관련성:** Directly relevant to our work on geometric and topological methods for graph representation learning. The benchmark's axis-decomposed safety analysis reveals how structural and spectral properties of graph representations (central to our GDL/TDA research) interact with deployment stresses—informing whether topological priors, higher-order structures, or equivariant designs might address the identified capability gaps in robustness, fairness, and OOD generalization.

---

### 4. Consistent Geometric Deep Learning via Hilbert Bundles and Cellular Sheaves

| 항목 | 내용 |
|------|------|
| **저자** | Kartik Tandon et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG, cs.AI, eess.SP |
| **관련성 점수** | 0.548 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06395v1) \| [PDF](https://arxiv.org/pdf/2605.06395v1) |

**요약:** Introduces HilbNets, a convolutional framework for infinite-dimensional signals on manifolds via Hilbert bundle connection Laplacians, with provable convergence guarantees from discrete sheaf approximations to the continuous setting.

**핵심 기여:**

- Proposes a convolutional learning framework (HilbNets) built on the connection Laplacian of Hilbert bundles, enabling spectral filtering of possibly infinite-dimensional signals (e.g., time series, distributions, operators) defined over manifolds.

- Proves that sampling a manifold with a Hilbert bundle naturally induces a Hilbert Cellular Sheaf, and that its sheaf Laplacian converges in probability to the continuous connection Laplacian — generalizing the classical Belkin & Niyogi graph-Laplacian-to-manifold-Laplacian convergence to infinite-dimensional fiber spaces.

- Establishes a two-stage discretization theory: (1) spatial sampling of the manifold into a sheaf, and (2) signal discretization within fibers, proving that the fully discrete HilbNets converge to their continuous counterparts and are transferable across different samplings of the same bundle.

- Validates the framework on synthetic and real-world tasks, demonstrating that the theoretical consistency guarantees translate into practical learning performance on irregular, infinite-dimensional signal domains.


**팀 관련성:** This paper is highly relevant to several of our core research threads. It provides the first rigorous bridge between sheaf neural networks on graphs and continuous geometric deep learning on manifolds with infinite-dimensional features, directly extending sheaf Laplacian and spectral graph convolution theory. The convergence and transferability results offer principled foundations for point cloud learning, gauge equivariant networks, and signal processing on cell/simplicial complexes, while the Hilbert bundle perspective opens new directions for handling rich signals (distributions, operators) in topological deep learning.

---

### 5. Beyond Rigid Alignment: Graph Federated Learning via Dual Manifold Calibration

| 항목 | 내용 |
|------|------|
| **저자** | Wentao Yu et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.491 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06260v1) \| [PDF](https://arxiv.org/pdf/2605.06260v1) |

**요약:** FedGMC addresses semantic and structural heterogeneity in graph federated learning by replacing rigid parameter/prototype alignment with dual manifold calibration using equidistant semantic anchors and global structural templates.

**핵심 기여:**

- Introduces a unified manifold perspective for graph federated learning that replaces the restrictive global linearity assumption (rigid alignment of parameters/prototypes) with a dual manifold calibration mechanism preserving both global commonalities and local personalization.

- Constructs geometrically optimal semantic manifolds on the server via equidistant semantic anchors, providing a principled geometric guide for calibrating heterogeneous local semantic spaces without collapsing them into a single global representation.

- Addresses structural heterogeneity by building global structural templates that form a global structural manifold, enabling calibration of local structural manifolds across clients with diverse graph topologies (both homophilic and heterophilic).

- Demonstrates consistent state-of-the-art performance across eleven benchmarks spanning homophilic and heterophilic graph settings, validating the framework's ability to balance global knowledge sharing with local distributional diversity.


**팀 관련성:** Directly relevant to our interests in geometric methods for graph representation learning and manifold-based reasoning. The paper's use of manifold geometry (equidistant anchors, structural templates) as an inductive bias for federated graph learning connects to our work on geometric priors, diffusion on manifolds, and topological/geometric approaches to graph neural networks—offering a novel angle on how manifold structure can regularize distributed learning over heterogeneous graph data.

---

### 6. Criticality and Saturation in Orthogonal Neural Networks

| 항목 | 내용 |
|------|------|
| **저자** | Max Guillen, Jan E. Gerken |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.471 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06563v1) \| [PDF](https://arxiv.org/pdf/2605.06563v1) |

**요약:** Derives exact finite-width recursion relations for orthogonally-initialized neural networks, theoretically explaining the observed depth-stability of finite-width correction tensors via Feynman diagram techniques.

**핵심 기여:**

- Derives explicit layer-wise recursion relations for all tensors in the 1/width expansion of network statistics under orthogonal initialization, valid to all orders.

- Extends Feynman diagram techniques (previously developed for i.i.d. initialization) to handle the richer combinatorial structure of orthogonal weight matrices.

- Proves analytically that finite-width correction tensors stabilize at large depth for activation functions with vanishing fixed point, explaining prior empirical observations by Day et al.

- Validates theoretical recursions against Monte-Carlo estimates from network ensembles, showing excellent agreement for both numerical solutions and analytical large-depth expansions.


**팀 관련성:** Limited direct relevance to the team's core topics. However, the analysis of orthogonal weight structure connects tangentially to the team's work on symmetry groups and equivariant architectures: understanding how orthogonal constraints on weight matrices affect signal propagation at finite width could inform the design of equivariant layers (e.g., SO(n)/O(n)-equivariant networks) where weight matrices are structurally constrained by group representations. The Feynman diagram methodology may also interest those studying signal propagation in deep geometric networks on manifolds or graphs.

---

### 7. Concept-Based Abductive and Contrastive Explanations for Behaviors of Vision Models

| 항목 | 내용 |
|------|------|
| **저자** | Ronaldo Canizales et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG, cs.AI |
| **관련성 점수** | 0.455 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06640v1) \| [PDF](https://arxiv.org/pdf/2605.06640v1) |

**요약:** Introduces concept-based abductive and contrastive explanations that identify minimal sets of high-level concepts causally responsible for vision model predictions, bridging concept-based and formal explanation methods.

**핵심 기여:**

- Defines concept-based abductive explanations (minimal concept sets sufficient for a prediction) and contrastive explanations (minimal concept sets whose removal changes a prediction), grounded in causal reasoning via concept erasure.

- Proposes a family of enumeration algorithms that compute all minimal abductive and contrastive explanations for a given model prediction, leveraging SAT-solver-inspired hitting set dualities.

- Extends individual-image explanations to collective behavior explanations by aggregating minimal explanations across image collections exhibiting a user-specified common model behavior.

- Empirically validates on multiple vision models and datasets, showing the explanations are compact, human-interpretable, and effective at revealing model reasoning patterns.


**팀 관련성:** This paper has limited direct relevance to the team's core focus on geometric/topological deep learning. However, it could be tangentially useful if the team seeks to interpret or explain predictions of geometric models (e.g., equivariant networks on point clouds) using high-level concept-based reasoning, or if concept erasure ideas inspire work on understanding learned representations in GDL architectures.

---

### 8. Invariant-Based Diagnostics for Graph Benchmarks

| 항목 | 내용 |
|------|------|
| **저자** | Richard von Moos, Mathieu Alain, Bastian Rieck |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG, math.CO |
| **관련성 점수** | 0.452 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06462v1) \| [PDF](https://arxiv.org/pdf/2605.06462v1) |

**요약:** Graph invariants—non-trainable, permutation-invariant structural descriptors—serve as diagnostic baselines revealing that many graph benchmarks are solvable without learning from connectivity, questioning whether GNNs truly exploit structure.

**핵심 기여:**

- Introduce a diagnostic framework based on classical graph invariants (e.g., degree sequences, clustering coefficients, spectral properties) that are provably more expressive than standard 1-WL GNNs, yet require no training.

- Demonstrate that invariants can characterize structural heterogeneity within and across 26 benchmark datasets, exposing which tasks genuinely require learning graph structure versus relying on node features.

- Show that simple invariant-based models (non-learned) are competitive with—and sometimes outperform—trained message-passing and transformer baselines, suggesting expressivity alone is not the primary driver of performance.

- Propose that invariant baselines become a standard evaluation tool for graph benchmarks, helping the community disentangle feature-driven from structure-driven performance and guiding development of graph foundation models.


**팀 관련성:** Directly relevant to the team's work on geometric and topological methods for graph representation learning. The invariants studied overlap with topological descriptors (spectral properties, Betti-number-adjacent features) and challenge the assumed necessity of learned message-passing and higher-order architectures—providing a rigorous null-hypothesis baseline that should inform how we evaluate GNNs, simplicial/cell complex networks, and sheaf neural networks on standard benchmarks.

---

### 9. SoftSAE: Dynamic Top-K Selection for Adaptive Sparse Autoencoders

| 항목 | 내용 |
|------|------|
| **저자** | Jakub Stępień et al. |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG, cs.CV |
| **관련성 점수** | 0.443 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06610v1) \| [PDF](https://arxiv.org/pdf/2605.06610v1) |

**요약:** SoftSAE replaces fixed top-K sparsity in sparse autoencoders with a differentiable, input-dependent dynamic top-K mechanism that adapts the number of active features to each input's complexity.

**핵심 기여:**

- Introduces a differentiable Soft Top-K operator that enables learning an input-dependent sparsity level k, replacing the fixed-K constraint in standard TopK sparse autoencoders.

- Connects adaptive sparsity to the notion of varying local intrinsic dimensionality of data manifolds, arguing that inputs of different complexity require different numbers of monosemantic features.

- Demonstrates that SoftSAE not only recovers meaningful monosemantic features in LLMs and Vision Transformers but also automatically calibrates explanation length (number of active features) to match per-sample information content.

- Provides a fully differentiable end-to-end training pipeline—avoiding the non-differentiability issues of hard top-K selection—enabling gradient-based optimization of the sparsity level itself.


**팀 관련성:** While not directly about geometric or topological deep learning, this paper's core motivation—that data lies on manifolds with varying local intrinsic dimensionality—resonates with the team's expertise in manifold-aware methods and geometric priors. The adaptive sparsity mechanism could inform how we design representation bottlenecks in geometric models (e.g., on point clouds or graphs) where local complexity varies, and the interpretability angle is relevant for understanding learned features in equivariant and topological neural networks.

---

### 10. Inductive Venn-Abers and related regressors

| 항목 | 내용 |
|------|------|
| **저자** | Ivan Petej, Vladimir Vovk |
| **발행일** | 2026-05-07 |
| **카테고리** | cs.LG |
| **관련성 점수** | 0.439 |
| **arXiv** | [링크](https://arxiv.org/abs/2605.06646v1) \| [PDF](https://arxiv.org/pdf/2605.06646v1) |

**요약:** Generalizes Venn-Abers probabilistic predictors from binary classification to unbounded regression by incorporating conformal prediction elements, with modest efficiency gains on larger training sets.

**핵심 기여:**

- Extends Venn-Abers predictors beyond binary classification and bounded regression to the unbounded regression setting, broadening their applicability.

- Integrates conformal prediction techniques to handle unbounded targets while preserving the validity guarantees characteristic of Venn-Abers predictors.

- Derives point regressors from the probabilistic Venn-Abers regression framework and empirically demonstrates modest improvements in predictive efficiency over standard regressors as training set size grows.

- Provides both simulation and empirical studies validating the approach and characterizing when the efficiency gains are most pronounced.


**팀 관련성:** This paper has **low relevance** to our team's focus areas. It addresses calibrated probabilistic regression via conformal/Venn-Abers methods, with no connection to geometric deep learning, topological data analysis, equivariant architectures, or graph/manifold-based learning. It may be of peripheral interest only if team members explore uncertainty quantification as a post-hoc layer on geometric models, but the paper itself does not engage with any geometric or topological structure.

---


## 🏭 Industry Blog Highlights



## 📈 이번 주 트렌드 분석

### Emerging Trends

- Diagnostic skepticism and benchmark auditing: Multiple papers (MANTRA extension, invariant-based diagnostics, GRL-Safety) converge on the theme that existing benchmarks may not test what we think they test—GNNs may not truly exploit connectivity, higher-order models may not achieve topological understanding, and graph representation methods have uneven safety profiles. This trend toward rigorous diagnostic baselines is reshaping how the community validates geometric and topological inductive biases.

- Discrete-to-continuous convergence theory for topological deep learning: The HilbNets paper establishes provable convergence from discrete cellular sheaf models to continuous Hilbert bundle settings on manifolds. Combined with the MANTRA paper's call for true topological generalization, this signals a growing demand for theoretical guarantees that discrete computational architectures faithfully approximate the continuous geometric/topological objects they claim to model.

- Multi-scale and coarsening-aware graph representations: Diversity Curves introduce spread-based isometry invariants tracked across coarsening hierarchies, producing size-invariant graph embeddings. This connects to persistent homology's multi-scale philosophy and suggests a broader trend of leveraging hierarchical structural summaries—bridging spectral graph theory, topological persistence, and practical graph classification.

- Manifold-aware calibration in distributed and heterogeneous settings: FedGMC's dual manifold calibration for graph federated learning introduces geometric reasoning (equidistant semantic anchors, global structural templates) to handle heterogeneity. This represents an emerging application of geometric deep learning principles beyond traditional prediction tasks into systems-level challenges like federated learning, robustness, and alignment.

- Concept-level and structural interpretability as a first-class objective: From concept-based abductive/contrastive explanations to invariant diagnostics to the interpretability axis in GRL-Safety, there is a clear trend toward making model decisions interpretable at semantically meaningful levels—whether those are high-level visual concepts or graph-structural invariants—rather than treating interpretability as post-hoc.


### 팀 액션 아이템


---

*이 뉴스레터는 RecSys Research Agent가 자동 생성했습니다.*
*arXiv + 0개 기술 블로그 → 시맨틱 필터링(threshold=0.35) → LLM 요약*