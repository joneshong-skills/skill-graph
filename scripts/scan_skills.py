#!/usr/bin/env python3
"""Scan all installed skills and build a knowledge graph in JSON.

Usage:
    python3 scan_skills.py [--skills-dir DIR] [--output FILE] [--json]

Output: JSON graph with nodes (skills) and edges (relationships).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

DEFAULT_SKILLS_DIR = os.path.expanduser("~/.claude/skills")

# ── Domain classification keywords ──────────────────────────────────────────
DOMAIN_KEYWORDS = {
    "content-creation": [
        "write", "draft", "article", "blog", "copy", "content", "newsletter",
        "marketing", "email", "ad copy", "social media",
    ],
    "document-output": [
        "pdf", "docx", "pptx", "xlsx", "word", "excel", "powerpoint",
        "spreadsheet", "presentation", "slides", "document",
    ],
    "visual-design": [
        "diagram", "canvas", "poster", "visual", "design", "ui",
        "ux", "frontend", "landing page", "theme", "brand", "color",
    ],
    "image-gen": [
        "image generation", "text-to-image", "ai art", "generate image",
        "image prompt", "midjourney", "dall-e", "flux", "stable diffusion",
        "grok image", "gemini image",
    ],
    "dev-tooling": [
        "headless", "cli", "codex", "gemini", "claude", "mcp", "server",
        "script", "pipeline", "ci/cd", "sdk",
    ],
    "orchestration": [
        "orchestrate", "dispatch", "agent", "multi-agent", "parallel",
        "pipeline", "coordinate", "team", "task", "dag",
    ],
    "knowledge-mgmt": [
        "notebooklm", "notebook", "research", "search", "documentation",
        "wiki", "audio overview", "source",
    ],
    "skill-meta": [
        "lifecycle", "curator", "publisher", "catalog", "optimizer",
        "optimize", "publish", "curate", "organize",
        "merge", "readme", "spec",
    ],
    "analysis": [
        "analyze", "competitor", "meeting", "insights", "audit",
        "communication", "comparison", "review",
    ],
    "ideation": [
        "brainstorm", "ideation", "explore", "decide", "approach",
        "model", "recommend",
    ],
}

# ── Edge heuristic rules ────────────────────────────────────────────────────
# Each rule: (condition_fn, edge_type, description_template)
# condition_fn(a, b) -> bool, where a/b are skill metadata dicts

def _shares_tool(a, b, tool):
    return tool in a.get("tools", []) and tool in b.get("tools", [])

def _in_domain(skill, domain):
    return domain in skill.get("domains", [])

PIPELINE_PAIRS = {
    # (upstream, downstream): description
    ("spec-kit", "maestro"): "Spec defines tasks → Maestro dispatches execution",
    ("spec-kit", "team-tasks"): "Spec defines tasks → Team-tasks coordinates agents",
    ("brainstorming", "spec-kit"): "Brainstorm explores ideas → Spec-kit formalizes",
    ("brainstorming", "frontend-design"): "Brainstorm UI concepts → Frontend implements",
    ("competitive-intel", "content-writer"): "Intel gathers insights → Writer creates content",
    ("competitive-intel", "marketing-copy"): "Intel informs → Marketing crafts messaging",
    ("smart-search", "content-writer"): "Search finds sources → Writer cites them",
    ("smart-search", "competitive-intel"): "Search gathers data → Intel analyzes patterns",
    ("image-prompt", "image-gen"): "Prompt crafts description → Gen produces image",
    ("content-writer", "doc-coauthoring"): "Writer drafts → Co-authoring refines",
    ("create-skill", "skill-optimizer"): "Create builds skill → Optimizer improves it",
    ("skill-optimizer", "skill-publisher"): "Optimizer polishes → Publisher ships it",
    ("create-skill", "skill-publisher"): "Create builds → Publisher ships",
    ("skill-curator", "skill-optimizer"): "Curator identifies issues → Optimizer fixes",
    ("model-mentor", "maestro"): "Mentor recommends CLI → Maestro dispatches to it",
    ("meeting-insights", "doc-coauthoring"): "Insights extracts patterns → Doc records",
    ("meeting-insights", "pptx"): "Insights from meetings → Slides for presentation",
    ("notebookllm-mentor", "notebook-bridge"): "Mentor guides usage → Bridge automates",
    ("notebook-bridge", "notebooklm-visual"): "Bridge uploads data → Visual generates",
}

ENHANCEMENT_PAIRS = {
    # (enhancer, enhanced): description
    ("theme-factory", "pptx"): "Theme styles presentation slides",
    ("theme-factory", "docx"): "Theme styles Word documents",
    ("theme-factory", "frontend-design"): "Theme provides design tokens",
    ("theme-factory", "canvas-design"): "Theme provides color palette",
    ("brand-guidelines", "frontend-design"): "Brand guides design decisions",
    ("brand-guidelines", "marketing-copy"): "Brand ensures voice consistency",
    ("brand-guidelines", "canvas-design"): "Brand guides visual identity",
    ("brand-guidelines", "pptx"): "Brand ensures slide consistency",
    ("diagram-gen", "spec-kit"): "Diagrams visualize spec architecture",
    ("diagram-gen", "doc-coauthoring"): "Diagrams illustrate documentation",
    ("diagram-gen", "readme-gen"): "Diagrams enhance README visuals",
    ("sync-config", "maestro"): "Sync ensures all CLIs configured for dispatch",
}

COMPOSITION_COMBOS = {
    # frozenset of skills: (emergent_name, description)
    frozenset(["competitive-intel", "content-writer", "smart-search"]): (
        "Thought Leadership Engine",
        "Research competitors + find sources + write authoritative articles",
    ),
    frozenset(["spec-kit", "maestro", "team-tasks"]): (
        "Full Dev Pipeline",
        "Specify → orchestrate → coordinate = end-to-end development",
    ),
    frozenset(["brainstorming", "diagram-gen", "doc-coauthoring"]): (
        "Design Workshop",
        "Ideate → visualize → document decisions",
    ),
    frozenset(["image-prompt", "image-gen", "canvas-design"]): (
        "Visual Production Suite",
        "Craft prompts → generate images → compose into designs",
    ),
    frozenset(["meeting-insights", "content-writer", "pptx"]): (
        "Meeting-to-Deck Pipeline",
        "Analyze meeting → write insights → produce presentation",
    ),
    frozenset(["claude-code-headless", "codex-headless", "gemini-cli-headless"]): (
        "Multi-CLI Arsenal",
        "Three headless CLIs ready for maestro orchestration",
    ),
    frozenset(["notebookllm-mentor", "notebook-bridge", "notebooklm-visual"]): (
        "NotebookLM Suite",
        "Learn → automate → generate visual content",
    ),
    frozenset(["create-skill", "skill-optimizer", "skill-curator", "skill-publisher"]): (
        "Skill Lifecycle",
        "Create → optimize → curate → publish = full skill management",
    ),
    frozenset(["frontend-design", "theme-factory", "brand-guidelines"]): (
        "Design System",
        "Brand + theme + code = consistent design language",
    ),
    frozenset(["pdf", "docx", "pptx", "xlsx"]): (
        "Office Suite",
        "Full document format coverage for any business output",
    ),
    frozenset(["smart-search", "model-mentor"]): (
        "Intelligence Advisor",
        "Search latest info + recommend optimal model/tool",
    ),
    frozenset(["marketing-copy", "frontend-design", "image-gen"]): (
        "Campaign Builder",
        "Write copy → design landing page → generate visuals",
    ),
}


def parse_frontmatter(skill_path: Path) -> dict:
    """Parse YAML frontmatter from SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {}

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    raw = match.group(1)

    # Simple YAML parsing (no dependency needed)
    current_key = None
    current_val = []

    for line in raw.split("\n"):
        # Key-value on same line
        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            if current_key and current_val:
                fm[current_key] = " ".join(current_val).strip()
            current_key = kv.group(1)
            val = kv.group(2).strip()
            if val and val != ">-":
                current_val = [val]
            else:
                current_val = []
        elif current_key and line.strip():
            current_val.append(line.strip())

    if current_key and current_val:
        fm[current_key] = " ".join(current_val).strip()

    return fm


def classify_domains(description: str) -> list:
    """Classify a skill into domains based on description keywords."""
    desc_lower = description.lower()
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score >= 2:
            domains.append(domain)
    return domains or ["general"]


def compute_domain_overlap(a_domains: list, b_domains: list) -> float:
    """Jaccard similarity of domain sets."""
    a_set, b_set = set(a_domains), set(b_domains)
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / len(a_set | b_set)


def build_graph(skills_dir: str) -> dict:
    """Build the complete skill knowledge graph."""
    skills_path = Path(skills_dir)
    nodes = []
    edges = []
    skill_map = {}

    # ── Build nodes ──────────────────────────────────────────────────────
    for d in sorted(skills_path.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(d)
        name = fm.get("name", d.name)
        description = fm.get("description", "")
        tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
        version = fm.get("version", "")
        domains = classify_domains(description)

        # Count resources
        scripts = list((d / "scripts").glob("*")) if (d / "scripts").exists() else []
        refs = list((d / "references").glob("*")) if (d / "references").exists() else []
        assets = list((d / "assets").glob("*")) if (d / "assets").exists() else []

        # Estimate body size
        body_lines = len(skill_md.read_text(encoding="utf-8").splitlines())

        node = {
            "id": name,
            "path": str(d),
            "description": description[:200],
            "domains": domains,
            "tools": tools,
            "version": version,
            "resource_count": {
                "scripts": len([s for s in scripts if s.name != ".gitkeep"]),
                "references": len([r for r in refs if r.name not in (".gitkeep", "guide.md")]),
                "assets": len([a for a in assets if a.name != ".gitkeep"]),
            },
            "body_lines": body_lines,
        }
        nodes.append(node)
        skill_map[name] = node

    # ── Build edges ──────────────────────────────────────────────────────
    skill_names = set(skill_map.keys())

    # 1. Pipeline edges (known pairs)
    for (up, down), desc in PIPELINE_PAIRS.items():
        if up in skill_names and down in skill_names:
            edges.append({
                "source": up,
                "target": down,
                "type": "pipeline",
                "description": desc,
                "strength": 0.8,
            })

    # 2. Enhancement edges
    for (enhancer, enhanced), desc in ENHANCEMENT_PAIRS.items():
        if enhancer in skill_names and enhanced in skill_names:
            edges.append({
                "source": enhancer,
                "target": enhanced,
                "type": "enhancement",
                "description": desc,
                "strength": 0.7,
            })

    # 3. Domain overlap edges (auto-discovered)
    names_list = sorted(skill_names)
    for i, a in enumerate(names_list):
        for b in names_list[i + 1:]:
            overlap = compute_domain_overlap(
                skill_map[a]["domains"], skill_map[b]["domains"]
            )
            if overlap >= 0.5:
                # Check it's not already covered by pipeline/enhancement
                existing = {(e["source"], e["target"]) for e in edges}
                existing |= {(e["target"], e["source"]) for e in edges}
                if (a, b) not in existing:
                    edges.append({
                        "source": a,
                        "target": b,
                        "type": "shares-domain",
                        "description": f"Shared domains: {set(skill_map[a]['domains']) & set(skill_map[b]['domains'])}",
                        "strength": round(overlap, 2),
                    })

    # ── Build compositions ───────────────────────────────────────────────
    compositions = []
    for combo_set, (name, desc) in COMPOSITION_COMBOS.items():
        present = combo_set & skill_names
        if len(present) >= 2:  # At least 2 of the combo skills exist
            compositions.append({
                "name": name,
                "skills": sorted(present),
                "missing": sorted(combo_set - skill_names),
                "description": desc,
                "completeness": round(len(present) / len(combo_set), 2),
            })

    # ── Compute graph stats ──────────────────────────────────────────────
    degree = defaultdict(int)
    for e in edges:
        degree[e["source"]] += 1
        degree[e["target"]] += 1

    hub_skills = sorted(degree.items(), key=lambda x: -x[1])[:5]
    isolated = [n["id"] for n in nodes if degree[n["id"]] == 0]

    # Domain distribution
    domain_counts = defaultdict(int)
    for n in nodes:
        for d in n["domains"]:
            domain_counts[d] += 1

    stats = {
        "total_skills": len(nodes),
        "total_edges": len(edges),
        "total_compositions": len(compositions),
        "hub_skills": [{"skill": s, "connections": c} for s, c in hub_skills],
        "isolated_skills": isolated,
        "domain_distribution": dict(sorted(domain_counts.items(), key=lambda x: -x[1])),
        "edge_type_counts": {},
    }
    for e in edges:
        stats["edge_type_counts"][e["type"]] = stats["edge_type_counts"].get(e["type"], 0) + 1

    return {
        "meta": {
            "skills_dir": skills_dir,
            "generated_at": __import__("datetime").datetime.now().isoformat(),
            "version": "1.0.0",
        },
        "nodes": nodes,
        "edges": edges,
        "compositions": compositions,
        "stats": stats,
    }


def main():
    parser = argparse.ArgumentParser(description="Build skill knowledge graph")
    parser.add_argument("--skills-dir", default=DEFAULT_SKILLS_DIR)
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    graph = build_graph(args.skills_dir)

    output = json.dumps(graph, indent=2, ensure_ascii=False) if args.json else json.dumps(graph, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Graph written to {args.output}", file=sys.stderr)
        print(f"  Nodes: {graph['stats']['total_skills']}", file=sys.stderr)
        print(f"  Edges: {graph['stats']['total_edges']}", file=sys.stderr)
        print(f"  Compositions: {graph['stats']['total_compositions']}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
