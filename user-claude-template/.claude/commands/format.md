# Format Command

Format code according to personal preferences across different languages.

## Steps

1. Detect file type
   - Check file extension
   - Identify appropriate formatter

2. Apply formatting
   - JavaScript/TypeScript: Use prettier or eslint
   - Python: Use black or autopep8
   - Go: Use gofmt
   - Rust: Use rustfmt
   - Other: Apply language-specific formatter

3. Verify formatting
   - Check for syntax errors
   - Ensure consistent style

## Usage

```
/format [file-path]
```

If no file path is provided, format all modified files.