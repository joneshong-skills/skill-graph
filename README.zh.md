[English](README.md) | [繁體中文](README.zh.md)

# skill-graph

Discover skill synergies and map relationships across your entire skill inventory.

## 說明

Skill Graph maps installed skills as a knowledge network, discovers pipelines and synergies, and outputs actionable recommendations with a visual network diagram showing how skills can be combined.

## 功能特色

- Maps all installed skills as a knowledge graph
- Identifies direct pipelines (e.g., blueprint → executor)
- Discovers unexpected synergies between unrelated skills
- Generates visual ASCII or Mermaid network diagrams
- Recommends creative skill combinations for complex tasks
- Parallel sub-agent analysis for comprehensive coverage

## 使用方式

透過以下觸發語句呼叫 Claude Code 來使用此技能：

- "show skill synergies"
- "skill graph"
- "which skills work together"
- "技能圖譜"
- "skill 協作"

## 相關技能

- [`skill-catalog`](https://github.com/joneshong-skills/skill-catalog)
- [`skill-curator`](https://github.com/joneshong-skills/skill-curator)
- [`diagram-gen`](https://github.com/joneshong-skills/diagram-gen)

## 安裝

將技能目錄複製到 Claude Code 技能資料夾：

```
cp -r skill-graph ~/.claude/skills/
```

放置在 `~/.claude/skills/` 的技能會被 Claude Code 自動發現，無需額外註冊。
