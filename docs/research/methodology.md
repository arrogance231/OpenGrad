# Methodology

OpenGrad uses baseline → intervention → evaluation → diagnosis → next experiment. No post-training method is presumed superior. Accepted checkpoints require reproducible comparisons, variance/confidence, regression analysis, contamination review, and lineage explaining why checkpoint X was preferred over Y.

Tool quality and inference efficiency are measured separately before any joint claim.

OpenGrad's initial research questions were motivated by deployment findings from the independently maintained [OpenWeights](https://github.com/alpharomercoma/openweights) project. OpenWeights observations are problem-discovery evidence, not OpenGrad results. Preserve that distinction with explicit labels such as `Observed in OpenWeights`, `Motivated by OpenWeights`, `OpenGrad hypothesis`, `OpenGrad planned experiment`, `OpenGrad reproduced`, and `OpenGrad result`; see [motivation and provenance](motivation.md).
