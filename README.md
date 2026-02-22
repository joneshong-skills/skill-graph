[English](README.md) | [繁體中文](README.zh.md)

# skill-graph

Discover skill synergies and map relationships across your entire skill inventory.

## Description

Skill Graph maps installed skills as a knowledge network, discovers pipelines and synergies, and outputs actionable recommendations with a visual network diagram showing how skills can be combined.

## Features

- Maps all installed skills as a knowledge graph
- Identifies direct pipelines (e.g., blueprint → executor)
- Discovers unexpected synergies between unrelated skills
- Generates visual ASCII or Mermaid network diagrams
- Recommends creative skill combinations for complex tasks
- Parallel sub-agent analysis for comprehensive coverage

## Usage

Invoke by asking Claude Code with trigger phrases such as:

- "show skill synergies"
- "skill graph"
- "which skills work together"
- "技能圖譜"
- "skill 協作"

## Related Skills

- [`skill-catalog`](https://github.com/joneshong-skills/skill-catalog)
- [`skill-curator`](https://github.com/joneshong-skills/skill-curator)
- [`diagram-gen`](https://github.com/joneshong-skills/diagram-gen)

## Install

Copy the skill directory into your Claude Code skills folder:

```
cp -r skill-graph ~/.claude/skills/
```

Skills placed in `~/.claude/skills/` are auto-discovered by Claude Code. No additional registration is needed.
