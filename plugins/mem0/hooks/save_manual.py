#!/usr/bin/env python3
"""
mem0 Manual Save Script
Saves provided messages to mem0 memory with optional metadata.

Usage:
    # Simple string (backward compatible)
    python3 save_manual.py "fact to remember"

    # With metadata via stdin
    echo '{"messages": [...], "metadata": {...}}' | python3 save_manual.py

    # JSON with content and metadata via stdin
    echo '{"content": "fact", "metadata": {"type": "engineering", "domain": "backend"}}' | python3 save_manual.py
"""

import json
import os
import sys
from pathlib import Path


def load_env_file():
    """Load .env files as fallback (settings.json env is preferred for global config)."""
    def parse_env_file(env_path: Path):
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())

    # Load project-specific .env first (takes precedence)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        parse_env_file(Path(project_dir) / ".env")

    # Load global .env from ~/.claude/.env as additional fallback
    home_dir = os.environ.get("HOME", "")
    if home_dir:
        parse_env_file(Path(home_dir) / ".claude" / ".env")


def get_config():
    """Get configuration from environment variables."""
    return {
        "api_key": os.environ.get("MEM0_API_KEY", ""),
        "user_id": os.environ.get("MEM0_USER_ID", "claude-code-user"),
    }


def validate_metadata(metadata: dict) -> dict:
    """Validate and clean metadata according to schema."""
    if not metadata:
        return {}

    valid = {}

    # type: required, binary
    mem_type = metadata.get("type", "").lower()
    if mem_type in ("engineering", "eng"):
        valid["type"] = "engineering"
    elif mem_type in ("non-engineering", "non-eng", "other"):
        valid["type"] = "non-engineering"

    # Only include engineering fields if type is engineering
    if valid.get("type") == "engineering":
        # domain
        domain = metadata.get("domain", "").lower()
        valid_domains = ["backend", "frontend", "product", "ai", "devops", "infra", "general"]
        if domain in valid_domains:
            valid["domain"] = domain

        # language
        lang = metadata.get("language", "").lower()
        valid_langs = ["rust", "python", "typescript", "javascript", "go", "java", "c", "cpp", "shell", "sql", "other"]
        if lang in valid_langs:
            valid["language"] = lang

        # repo (string, no validation needed)
        repo = metadata.get("repo", "")
        if repo and isinstance(repo, str):
            valid["repo"] = repo.strip()

        # package (string, no validation needed)
        package = metadata.get("package", "")
        if package and isinstance(package, str):
            valid["package"] = package.strip()

    return valid


def save_memories(messages: list, config: dict, metadata: dict = None) -> dict:
    """Save messages to mem0 with optional metadata.

    Uses infer=False to store pre-extracted insights directly without
    mem0's internal LLM refinement, since extraction is done client-side.
    """
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=config["api_key"])

        # Build kwargs - use infer=False since we do extraction client-side
        kwargs = {"user_id": config["user_id"], "infer": False}
        if metadata:
            validated = validate_metadata(metadata)
            if validated:
                kwargs["metadata"] = validated

        result = client.add(messages, **kwargs)
        return {"success": True, "result": result, "metadata": kwargs.get("metadata")}
    except ImportError:
        return {"success": False, "error": "mem0ai not installed. Run: pip install mem0ai"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    # Load environment from .env file
    load_env_file()

    # Get configuration
    config = get_config()

    # Check for API key
    if not config["api_key"]:
        print(json.dumps({"success": False, "error": "MEM0_API_KEY not configured"}))
        sys.exit(1)

    # Get messages and metadata from stdin or command line
    messages = []
    metadata = {}

    if len(sys.argv) > 1:
        # Message provided as command line argument (backward compatible)
        content = " ".join(sys.argv[1:])
        messages = [{"role": "user", "content": content}]
    else:
        # Try to read from stdin
        try:
            input_data = json.load(sys.stdin)

            if isinstance(input_data, dict):
                # New format: {"content": "...", "metadata": {...}}
                if "content" in input_data:
                    messages = [{"role": "user", "content": input_data["content"]}]
                    metadata = input_data.get("metadata", {})
                # Legacy format: {"messages": [...], "metadata": {...}}
                elif "messages" in input_data:
                    messages = input_data["messages"]
                    metadata = input_data.get("metadata", {})
            elif isinstance(input_data, list):
                # Legacy format: just messages array
                messages = input_data
        except json.JSONDecodeError:
            print(json.dumps({"success": False, "error": "Invalid JSON input"}))
            sys.exit(1)
        except Exception:
            print(json.dumps({"success": False, "error": "No messages provided"}))
            sys.exit(1)

    if not messages:
        print(json.dumps({"success": False, "error": "No messages to save"}))
        sys.exit(1)

    # Save to mem0
    result = save_memories(messages, config, metadata)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
