# Project Structure

```
/
├── .github/           # GitHub workflows and configurations
├── .kiro/             # Kiro IDE settings and steering files
│   └── settings/      # MCP server configurations
├── crawled_data/      # Main data directory
│   ├── page_XXXX.json # Individual crawled page files (455 files)
│   └── summary.json   # Crawl job summary and statistics
├── README.md          # MCP Server configuration guide (Chinese)
└── hello-kiro.md      # Kiro introduction file
```

## Key Directories

### crawled_data/
Contains all crawled web page data:
- Files numbered sequentially: `page_0001.json` to `page_0455.json`
- Each file represents one page from the source website
- `summary.json` provides crawl job metadata

## File Naming Convention
- Page files use zero-padded 4-digit numbering: `page_XXXX.json`
- Allows for up to 9999 pages while maintaining sort order

## Notes
- This is a data-only repository with no source code
- Configuration files are in `.kiro/settings/`
- No test or build directories exist
