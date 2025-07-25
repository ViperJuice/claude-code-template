# Project Context for Claude Code

## Project Overview
[Describe your project's purpose, goals, and main features]

## Architecture
[Describe the high-level architecture of your project]

### Key Components
- Component 1: [Description]
- Component 2: [Description]
- Component 3: [Description]

### Technology Stack
- Language: [e.g., TypeScript, Python, Go]
- Framework: [e.g., React, Django, Gin]
- Database: [e.g., PostgreSQL, MongoDB]
- Testing: [e.g., Jest, pytest, go test]

## Development Setup

### Prerequisites
- [List required tools and versions]
- [e.g., Node.js 18+, Python 3.11+, Go 1.21+]

### Installation
```bash
# Clone the repository
git clone [repository-url]
cd [project-name]

# Install dependencies
[package-manager] install
```

### Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Required variables:
# DATABASE_URL=
# API_KEY=
# [other variables]
```

## Key Commands

### Development
```bash
# Start development server
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Build for production
npm run build
```

## Coding Standards

### Code Style
- [Describe code formatting rules]
- [Naming conventions]
- [File organization]

### Git Workflow
- Branch naming: `feature/description`, `fix/description`
- Commit message format: `type(scope): description`
- PR process: [Describe PR requirements]

### Testing Requirements
- All new features must include tests
- Maintain test coverage above [X]%
- Test file naming: `*.test.[ext]` or `*_test.[ext]`

## Important Files and Directories

```
src/
├── components/     # [Description]
├── services/       # [Description]
├── utils/          # [Description]
└── tests/          # [Description]
```

## API Documentation
[Link to API documentation or describe key endpoints]

## Deployment

### Staging
```bash
# Deploy to staging
[deployment command]
```

### Production
```bash
# Deploy to production
[deployment command]
```

## Troubleshooting

### Common Issues
1. **Issue**: [Description]
   **Solution**: [How to fix]

2. **Issue**: [Description]
   **Solution**: [How to fix]

## Additional Notes
[Any other important information for Claude to know about the project]