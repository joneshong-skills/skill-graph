# Edge Taxonomy — Skill Relationship Types

## Overview

The skill graph uses 5 relationship types to model how skills connect and collaborate.
Edges are directional except `shares-domain` (bidirectional).

## Edge Types

### 1. Pipeline (A → B)

**Definition**: A's output becomes B's input. Sequential dependency.

| Property | Value |
|----------|-------|
| Direction | A → B (strict) |
| Strength | 0.7–0.9 |
| Visual | Solid arrow `-->` |
| Color | `#6c8ebf` (process blue) |

**Signal**: "First use A, then feed result into B."

**Examples**:
- `spec-kit` → `maestro`: Spec defines tasks, Maestro dispatches
- `image-prompt` → `image-gen`: Prompt crafts, Gen produces
- `competitive-intel` → `content-writer`: Intel informs, Writer publishes

### 2. Enhancement (A → B)

**Definition**: A makes B better without being required. Optional amplifier.

| Property | Value |
|----------|-------|
| Direction | A → B (enhancer → enhanced) |
| Strength | 0.5–0.8 |
| Visual | Dashed arrow `-.->` |
| Color | `#2f9e44` (growth green) |

**Signal**: "B works fine alone, but A elevates the result."

**Examples**:
- `theme-factory` → `pptx`: Theme styles the slides
- `brand-guidelines` → `marketing-copy`: Brand ensures voice consistency
- `diagram-gen` → `readme-gen`: Diagrams make README more visual

### 3. Composition (A + B + ... = Emergent)

**Definition**: Multiple skills combine to create a capability none has alone.

| Property | Value |
|----------|-------|
| Direction | N/A (group) |
| Strength | 0.8–1.0 |
| Visual | Subgraph cluster |
| Color | `#5f3dc4` (reasoning purple) |

**Signal**: "Together they become something new."

**Examples**:
- `competitive-intel` + `content-writer` + `smart-search` = **Thought Leadership Engine**
- `spec-kit` + `maestro` + `team-tasks` = **Full Dev Pipeline**
- `create-skill` + `skill-optimizer` + `skill-curator` + `skill-publisher` = **Skill Lifecycle**

### 4. Shares-Domain (A ↔ B)

**Definition**: Skills operate in the same domain but serve different purposes.

| Property | Value |
|----------|-------|
| Direction | Bidirectional |
| Strength | 0.3–0.6 |
| Visual | Dotted line `~~~` or thin `---` |
| Color | `#868e96` (neutral gray) |

**Signal**: "Related but not interchangeable."

**Examples**:
- `notebookllm-mentor` ↔ `notebook-bridge`: Knowledge vs automation
- `marketing-copy` ↔ `content-writer`: Conversion vs editorial

### 5. Enables (A → B)

**Definition**: A unlocks or is a prerequisite for B to function.

| Property | Value |
|----------|-------|
| Direction | A → B (enabler → dependent) |
| Strength | 0.9–1.0 |
| Visual | Thick arrow `==>` |
| Color | `#e67700` (critical orange) |

**Signal**: "B cannot work without A being set up first."

**Examples**:
- `sync-config` → `maestro`: CLI configs must be synced before multi-CLI dispatch
- `model-mentor` → `maestro`: Need to know which CLI to route to

## Edge Discovery Heuristics

When analyzing skills for new edges, check:

1. **Output/Input match**: Does A produce something B consumes?
2. **Tool overlap**: Do they share tools (Bash, Read, etc.)?
3. **Domain overlap**: Jaccard similarity ≥ 0.5 of domain keywords?
4. **Description co-occurrence**: Do trigger phrases mention similar concepts?
5. **Workflow sequence**: Does the user naturally use them in order?

## Strength Scoring

| Score | Meaning | Evidence |
|-------|---------|----------|
| 0.9–1.0 | Critical link | One doesn't work without the other |
| 0.7–0.8 | Strong link | Frequently used together |
| 0.5–0.6 | Moderate link | Sometimes useful together |
| 0.3–0.4 | Weak link | Shared domain, rare co-use |
| < 0.3 | Not an edge | Coincidental overlap |
