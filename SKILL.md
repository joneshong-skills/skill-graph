---
name: skill-graph
description: >-
  This skill should be used when the user asks to "show skill synergies",
  "skill graph", "which skills work together", "skill combinations",
  "技能圖譜", "skill 協作", "哪些 skill 可以搭配", "skill 知識圖譜",
  "recommend a skill combo", "what can my skills do together",
  mentions skill collaboration discovery, or discusses mapping skill
  relationships, finding creative skill combinations, or visualizing
  the skill network.
version: 0.2.0
tools: Read, Bash, Task, Glob, Grep, sandbox_execute
---

# Skill Graph

Map the installed skill inventory as a knowledge graph. Discover pipelines,
synergies, and emergent compositions. Output actionable recommendations and
a visual network diagram. Uses parallel sub-agents for creative analysis.

## Agent Delegation

Delegate dependency data extraction to `explorer` agent, visualization to `designer` agent.

```
explorer (Haiku, maxTurns=10, tools: Read, Grep, Glob)
```

## Core Principles

- **Bold hypothesis, careful verification** — Sub-agents propose wild combos;
  validation checks feasibility against actual SKILL.md content.
- **Maintain principles, preserve flexibility** — The graph structure is
  deterministic (scan script); the analysis is creative (sub-agents).
- **Stay current** — Re-scan every invocation. No cached assumptions.
- **Network over tree** — Skills form a mesh, not a hierarchy. Any skill
  can connect to any other. Compositions emerge from the network topology.

## Workflow

### Step 1: Scan — Build the Graph

Run the scanner to generate a fresh JSON graph.

**Preferred (Sandbox)**:
```python
# sandbox_execute
import sys
sys.path.insert(0, "/Users/joneshong/.claude/skills/skill-graph/scripts")
import scan_skills
graph_json = scan_skills.main(json_output=True)
output(graph_json)
```

**Fallback (Bash)**:
```bash
GRAPH_JSON=$(python3 ~/.claude/skills/skill-graph/scripts/scan_skills.py --json)
```

The script outputs:
- **nodes**: Each skill with id, domains, tools, resource counts
- **edges**: Pipeline, enhancement, shares-domain relationships
- **compositions**: Known multi-skill combos with completeness scores
- **stats**: Hub skills, isolated skills, domain distribution

Parse the JSON to understand the current topology before launching sub-agents.

### Step 2: Parallel Sub-Agent Analysis

Launch **3 sub-agents simultaneously** using the Task tool with
`subagent_type: "general-purpose"`. Each analyzes the graph from a
different angle. Pass the full graph JSON to each agent.

#### Agent A: Pipeline Architect

Focus: Discover sequential workflows — chains where A's output feeds B's input.

```
Prompt template:
You are analyzing a skill knowledge graph to discover PIPELINE opportunities.

Here is the graph data (JSON):
{graph_json}

Your task:
1. Read the SKILL.md files of the top 10 hub skills (highest connection count)
2. For each hub, trace possible multi-step workflows:
   - What task would START with this skill?
   - What skill would RECEIVE its output?
   - Can the chain extend further (3-4 steps)?
3. Score each pipeline by:
   - Practicality (0-10): Would a real user do this?
   - Novelty (0-10): Is this a non-obvious combination?
   - Impact (0-10): How much value does the pipeline create?

Output: Top 5 pipelines as structured recommendations.
Format per pipeline:
- Name: [descriptive name]
- Chain: skill-a → skill-b → skill-c
- Trigger: "User says: [example request]"
- Steps: [1-sentence per step]
- Scores: Practicality X / Novelty Y / Impact Z
```

#### Agent B: Synergy Alchemist

Focus: Discover emergent compositions — skill combos that create capabilities
none has alone. Think creatively. Cross-domain combinations are encouraged.

```
Prompt template:
You are the Synergy Alchemist analyzing a skill knowledge graph.
Your role is to find CREATIVE, NON-OBVIOUS skill combinations.

Here is the graph data (JSON):
{graph_json}

Your task:
1. Look at skills from DIFFERENT domains (cross-domain is the goal)
2. For each combination (2-4 skills), describe the emergent capability:
   - What new thing can the user do that no single skill enables?
   - What's the "aha moment" when these skills combine?
3. Be bold but grounded — each combo must reference actual capabilities
   from the SKILL.md files. Read them to verify.
4. Consider the user's INTENT — what ambitious tasks might they attempt?

Output: Top 5 synergy combos ranked by creativity * feasibility.
Format per combo:
- Name: [catchy emergent capability name]
- Skills: [list]
- Emergent capability: [what becomes possible]
- Example task: [concrete user request that triggers this combo]
- Why it works: [1-2 sentences citing actual skill capabilities]
- Boldness: [how creative is this, 1-10]
- Feasibility: [how practical is this, 1-10]
```

#### Agent C: Gap Cartographer

Focus: Find missing connections and propose new skills that would
dramatically increase the graph's connectivity.

```
Prompt template:
You are the Gap Cartographer analyzing a skill knowledge graph.
Your role is to find MISSING LINKS and propose new connections.

Here is the graph data (JSON):
{graph_json}

Your task:
1. Identify isolated or under-connected skills (< 3 strong edges)
2. For each, ask: "What skill, if it existed, would connect this
   to the rest of the graph?"
3. Look at the domain distribution — which domains are underserved?
4. Propose 3-5 "bridge skills" or "missing links" that would:
   - Connect isolated clusters
   - Enable new pipelines across domains
   - Fill capability gaps in the current inventory

Output:
- Isolated skill analysis: [skill → what it lacks → proposed connection]
- Missing bridge skills: [name, purpose, which skills it would connect]
- Domain gaps: [underserved areas → what skill would fill them]
- Graph health score: [0-100 based on connectivity, coverage, balance]
```

### Step 3: Synthesize Results

After all 3 agents complete, combine their findings:

1. **Merge pipeline and synergy discoveries** — Deduplicate overlapping combos
2. **Cross-reference with gap analysis** — Which proposed combos would also
   fill gaps identified by Agent C?
3. **Rank by composite score**:
   `Score = (Practicality + Novelty + Impact) / 3`
   Bonus +2 if it fills a gap. Bonus +1 if cross-domain.

### Step 4: Generate Visual Graph

Create a Mermaid diagram showing the skill network. Follow diagram-gen conventions.

**Layout rules**:
- Use `flowchart LR` for the overview (horizontal = natural for networks)
- Group skills by domain using subgraphs
- Edge styles:
  - `-->` solid: pipeline edges
  - `-.->` dashed: enhancement edges
  - `~~~` invisible: layout control only
- Highlight recommended combos with thick arrows `==>`
- Color nodes by domain using the semantic palette from diagram-gen
- Keep to top 20-30 most connected skills if inventory is large

**Node styling by domain**:

| Domain | Fill | Stroke |
|--------|------|--------|
| content-creation | `#d3f9d8` | `#2f9e44` |
| document-output | `#fff4e6` | `#e67700` |
| visual-design | `#e5dbff` | `#5f3dc4` |
| dev-tooling | `#dae8fc` | `#6c8ebf` |
| orchestration | `#c5f6fa` | `#0c8599` |
| knowledge-mgmt | `#fff2cc` | `#d6b656` |
| skill-meta | `#f8f9fa` | `#868e96` |
| analysis | `#ffe3e3` | `#c92a2a` |
| ideation | `#fff2cc` | `#d6b656` |

For SVG rendering, use:
```bash
node ~/.claude/skills/diagram-gen/scripts/render.mjs \
  --input graph.mmd --output skill-graph.svg \
  --theme github-light --transparent
```

### Step 5: Present Recommendations

Format output as a structured report:

```markdown
## Skill Graph Report — {date}

### Network Overview
- Total skills: N | Edges: M | Compositions: K
- Hub skills: [top 3 with connection counts]
- Isolated: [list]

### Top Recommended Combos

#### 1. {Combo Name} (Score: X/10)
**Skills**: skill-a + skill-b + skill-c
**What it unlocks**: [1-2 sentences]
**Try it**: "{example user request}"
**Pipeline**: skill-a → skill-b → skill-c

[... repeat for top 5 ...]

### Gap Analysis
- Missing bridges: [proposed new skills]
- Underserved domains: [list]
- Graph health: X/100

### Network Diagram
[Mermaid diagram or link to SVG]
```

**After presenting**, ask the user:
- "Want me to execute one of these combos on a real task?"
- "Should I create a missing bridge skill?"
- "Want to explore a specific cluster in more depth?"

## Quick Reference

### Known High-Value Compositions

| Composition | Skills | Emergent Capability |
|-------------|--------|-------------------|
| Thought Leadership Engine | competitive-intel + content-writer + smart-search | Research → analyze → publish authority content |
| Full Dev Pipeline | spec-kit + maestro + team-tasks | Specify → orchestrate → coordinate |
| Design Workshop | brainstorming + diagram-gen + doc-coauthoring | Ideate → visualize → document |
| Visual Production Suite | image-prompt + image-gen + canvas-design | Craft → generate → compose |
| Campaign Builder | marketing-copy + frontend-design + image-gen | Write → build → illustrate |
| Skill Lifecycle | create-skill + skill-optimizer + skill-curator + skill-publisher | Build → polish → organize → ship |
| Design System | brand-guidelines + theme-factory + frontend-design | Identity → tokens → code |
| Office Suite | pdf + docx + pptx + xlsx | Complete business document coverage |
| NotebookLM Suite | notebookllm-mentor + notebook-bridge + notebookllm-visual | Learn → automate → generate |
| Multi-CLI Arsenal | claude-code-headless + codex-headless + gemini-cli-headless | Three engines for maestro |
| Intelligence Advisor | model-mentor + smart-search | Latest info + optimal tool recommendation |
| Meeting-to-Deck | meeting-insights + content-writer + pptx | Analyze → write → present |

### Sub-Agent Execution Pattern

```
Step 2a: Launch Agent A + Agent B + Agent C in PARALLEL
         (all receive the same graph JSON)
Step 2b: Wait for all three to complete
Step 3:  Synthesize in main context (no sub-agent needed)
```

Use `subagent_type: "general-purpose"` for all three agents.
For large skill inventories (40+), consider splitting Agent A's work
into 2 sub-agents (top 5 hubs each) for faster processing.

## Sandbox Optimization

This skill is **sandbox-optimized**. Batch operations run inside `sandbox_execute`:

- **Skill inventory scan**: Import `scripts/scan_skills.py` in sandbox to build the full graph JSON without spawning a separate process
- **Graph JSON generation**: Run in sandbox so the JSON is returned directly, avoiding shell output buffering issues with large inventories

Principle: **Deterministic batch work → sandbox; reasoning/presentation → LLM.**

## Continuous Improvement

This skill evolves with each use. After every invocation:

1. **Reflect** — Identify what worked, what caused friction, and any unexpected issues
2. **Record** — Append a concise lesson to `lessons.md` in this skill's directory
3. **Refine** — When a pattern recurs (2+ times), update SKILL.md directly

### lessons.md Entry Format

```
### YYYY-MM-DD — Brief title
- **Friction**: What went wrong or was suboptimal
- **Fix**: How it was resolved
- **Rule**: Generalizable takeaway for future invocations
```

Accumulated lessons signal when to run `/skill-optimizer` for a deeper structural review.

## Additional Resources

### Reference Files
- **`references/edge-taxonomy.md`** — Complete edge type definitions with examples,
  scoring criteria, and discovery heuristics

### Scripts
- **`scripts/scan_skills.py`** — Scan all skills and build graph JSON.
  Usage: `python3 scan_skills.py [--skills-dir DIR] [--output FILE] [--json]`
