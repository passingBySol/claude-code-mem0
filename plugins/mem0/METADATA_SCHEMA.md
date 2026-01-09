# Memory Metadata Schema

This document defines the metadata schema used for categorizing memories to improve retrieval.

## Schema Definition

```json
{
  "type": "engineering" | "non-engineering",

  // Only present if type == "engineering"
  "domain": "backend" | "frontend" | "product" | "ai" | "devops" | "infra" | "general",
  "language": "rust" | "python" | "typescript" | "javascript" | "go" | "java" | "c" | "cpp" | "shell" | "sql" | "other",
  "repo": "repository-name",           // Optional: name of the repository
  "package": "crate-or-module-name"    // Optional: specific package in a workspace/monorepo
}
```

## Field Definitions

### `type` (required)
Binary classification of the memory content.

| Value | Description |
|-------|-------------|
| `engineering` | Technical knowledge: code patterns, architecture, debugging, tooling |
| `non-engineering` | Non-technical: product decisions, user preferences, project context |

### `domain` (engineering only)
The technical domain this knowledge applies to.

| Value | Description |
|-------|-------------|
| `backend` | Server-side logic, APIs, databases, services |
| `frontend` | UI, client-side code, UX patterns |
| `product` | Product requirements, feature design, user stories |
| `ai` | ML/AI systems, prompts, model behavior, LLM patterns |
| `devops` | CI/CD, deployment, infrastructure-as-code |
| `infra` | Cloud, networking, system architecture |
| `general` | Cross-cutting concerns, general engineering principles |

### `language` (engineering only)
Primary programming language context.

| Value | Examples |
|-------|----------|
| `rust` | Rust patterns, cargo, crates |
| `python` | Python idioms, pip, Django/FastAPI |
| `typescript` | TypeScript, Node.js, React |
| `javascript` | Vanilla JS, browser APIs |
| `go` | Go patterns, modules |
| `java` | JVM ecosystem |
| `c` | C patterns, memory management |
| `cpp` | C++ patterns, templates |
| `shell` | Bash, scripting |
| `sql` | Database queries, schema design |
| `other` | Other or language-agnostic |

### `repo` (engineering only, optional)
Name of the repository this knowledge relates to. Use the repo name without org prefix.

Examples: `claude-code-mem0`, `bonkbot-web-terminal`, `my-app`

### `package` (engineering only, optional)
For monorepos or workspaces, the specific package/crate/module name.

Examples:
- Rust workspace: `enriching-materializer` (a binary in the workspace)
- Node monorepo: `@myorg/api-client` (a package in the monorepo)
- Python: `myproject.utils` (a submodule)

## Examples

### Engineering - Backend Rust pattern
```json
{
  "type": "engineering",
  "domain": "backend",
  "language": "rust",
  "repo": "bonkbot-web-terminal",
  "package": "enriching-materializer"
}
```

### Engineering - Frontend React pattern
```json
{
  "type": "engineering",
  "domain": "frontend",
  "language": "typescript",
  "repo": "my-dashboard"
}
```

### Engineering - General principle
```json
{
  "type": "engineering",
  "domain": "general",
  "language": "other"
}
```

### Non-engineering - Product decision
```json
{
  "type": "non-engineering"
}
```

## Usage in mem0

Metadata is passed to `client.add()`:

```python
client.add(
    messages=[{"role": "user", "content": "insight content"}],
    user_id="claude-code-user",
    metadata={
        "type": "engineering",
        "domain": "backend",
        "language": "rust",
        "repo": "my-project"
    }
)
```

Metadata improves retrieval by allowing filtered searches and contextual ranking.
