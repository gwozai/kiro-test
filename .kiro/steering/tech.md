# Technology Stack

## Data Format
- JSON files for storing crawled data
- No build system (data-only repository)

## Data Schema

Each `page_XXXX.json` file follows this structure:
```json
{
  "page": number,
  "url": "string",
  "crawled_at": "ISO 8601 timestamp",
  "articles": [
    {
      "title": "string",
      "url": "string"
    }
  ],
  "content_preview": "string"
}
```

## Summary File
`crawled_data/summary.json` tracks crawl job results:
```json
{
  "total": number,
  "success": number,
  "failed": number,
  "results": [...]
}
```

## Tools Used
- Web crawler (external, likely Playwright-based given timeout errors)
- MCP Server integration for GitHub operations

## Common Tasks
No build/test commands - this is a data repository. Operations involve:
- Reading and analyzing JSON data files
- Processing crawled content
- Validating data integrity
