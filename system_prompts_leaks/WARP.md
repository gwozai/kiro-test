# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a community-maintained collection of system prompts, system messages, and developer messages from various AI systems. It's a **documentation-only repository** with no build system, tests, or dependencies.

## Directory Structure

Organized by company/provider:

- **Anthropic/** - Claude system prompts, tool definitions, and feature-specific prompts
- **Google/** - Gemini system prompts (webapp, CLI, guided learning modes)
- **OpenAI/** - ChatGPT/GPT system prompts
  - **OpenAI/API/** - API-specific system messages and configuration docs
  - **OpenAI/Old/** - Archived/historical prompts
- **Perplexity/** - Perplexity AI system prompts
- **Proton/** - Luma AI system prompts
- **xAI/** - Grok system prompts and persona definitions
- **Misc/** - Other AI systems (Warp, Kagi, Raycast, Le Chat, Sesame AI, Fellou)

## File Naming Conventions

When adding new system prompts, follow these patterns:

- **Model version**: `claude-4.5-sonnet.md`, `gpt-5-thinking.md`, `grok-4.md`
- **Feature/mode specific**: `claude-code-plan-mode.md`, `gemini-2.5-pro-guided-learning.md`
- **Tool definitions**: `tool-file_search.md`, `tool-python.md`, `tool-deep-research.md`
- **Use descriptive names** that make the content immediately clear

## File Formats

- **Primary format**: Markdown (`.md`)
- **Alternative formats**: `.txt`, `.xml`, `.js` for structured data
- Some prompts include JSON/XML artifacts when that's how they're transmitted

## Contributing

This repository welcomes pull requests. When adding new prompts:

1. Place in appropriate company/provider directory (or `Misc/` if unclear)
2. Use descriptive filenames following existing conventions
3. Include metadata context where helpful (date extracted, model version, access method)
4. No special formatting or linting requirements

## Important Notes

- **No build/test commands** - this is pure documentation
- Check `Anthropic/readme.md` for details on character encoding in Claude prompts
- Check `OpenAI/API/readme.md` for API-specific system message details
- The repository includes Warp's own agent prompt in `Misc/Warp-2.0-agent.md`

## Common Tasks

**View all files in a directory:**
```bash
ls Anthropic/
```

**Find prompts matching a pattern:**
```bash
fd -e md -e txt "claude-code" Anthropic/
```

**Search for specific content:**
```bash
rg "artifacts" Anthropic/
```

**Check recent additions:**
```bash
git --no-pager log --oneline -10
```
