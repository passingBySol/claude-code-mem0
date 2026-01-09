---
description: Manually save memories from this conversation to mem0
allowed-tools: [Bash]
---

# Save Memories to mem0

Extract and save conceptual insights from this conversation to mem0 for future sessions.

## Instructions

### Step 1: Identify Conceptual Insights

Review the current conversation and identify **conceptual knowledge** worth remembering:

**DO extract:**
- Engineering principles and philosophies
- Architectural patterns and design decisions
- Technical concepts learned
- Problem-solving methodologies
- Best practices and anti-patterns
- Domain-specific knowledge

**DO NOT extract:**
- Procedural facts ("user ran command X")
- Session metadata ("user has N files")
- Temporary state information
- Tool invocations or outputs

### Step 2: Classify Each Insight

For each insight, determine its metadata:

#### 2a. Type Classification (required)
- `engineering` - Technical knowledge: code patterns, architecture, debugging, tooling
- `non-engineering` - Non-technical: product decisions, user preferences, project context

#### 2b. Engineering-only Fields

If type is `engineering`, also classify:

**Domain:**
| Value | Use when |
|-------|----------|
| `backend` | Server-side, APIs, databases, services |
| `frontend` | UI, client-side, UX patterns |
| `product` | Product requirements, feature design |
| `ai` | ML/AI, prompts, LLM patterns |
| `devops` | CI/CD, deployment |
| `infra` | Cloud, networking, system architecture |
| `general` | Cross-cutting, general principles |

**Language:**
`rust`, `python`, `typescript`, `javascript`, `go`, `java`, `c`, `cpp`, `shell`, `sql`, `other`

**Repo** (if applicable):
The repository name this relates to (e.g., `claude-code-mem0`)

**Package** (if applicable):
For monorepos/workspaces, the specific package name (e.g., `enriching-materializer`)

### Step 3: Save Each Insight with Metadata

Save insights using JSON via stdin to include metadata:

```bash
echo '{"content": "YOUR_INSIGHT_HERE", "metadata": {"type": "engineering", "domain": "backend", "language": "rust", "repo": "repo-name"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

### Step 4: Report Results

Tell the user what insights were saved and their classifications.

## Examples

### Engineering Backend Insight (Rust)
```bash
echo '{"content": "In Rust, prefer Result<T, E> with the ? operator for error propagation - it provides type safety and clean control flow without exceptions", "metadata": {"type": "engineering", "domain": "backend", "language": "rust"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

### Engineering General Principle
```bash
echo '{"content": "Modularity principle: things that change together should live together. Each module should have one reason to exist.", "metadata": {"type": "engineering", "domain": "general", "language": "other"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

### Engineering AI Pattern
```bash
echo '{"content": "LLMs exhibit U-shaped attention: strong recall at context beginning and end, with 30%+ performance drop for middle-positioned information", "metadata": {"type": "engineering", "domain": "ai", "language": "other"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

### Project-Specific Insight
```bash
echo '{"content": "The enriching-materializer uses RocksDB for state storage with backward-compatible migration support", "metadata": {"type": "engineering", "domain": "backend", "language": "rust", "repo": "bonkbot-web-terminal", "package": "enriching-materializer"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

### Non-Engineering Insight
```bash
echo '{"content": "User prefers concise responses without excessive praise or emotional validation", "metadata": {"type": "non-engineering"}}' | ${CLAUDE_PYTHON_VENV}/bin/python ${CLAUDE_PLUGIN_ROOT}/hooks/save_manual.py
```

## Context Detection

To help with classification, check the environment:

- `CLAUDE_PROJECT_DIR` - Current project directory (helps detect repo name)
- Look at file paths in conversation for language hints
- Check for Cargo.toml (Rust), package.json (JS/TS), pyproject.toml (Python), etc.

## Metadata Schema Reference

See `METADATA_SCHEMA.md` in the plugin directory for the complete schema definition.
