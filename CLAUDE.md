# Project Context for Claude Code

> 💡 **This is a template file!** Replace the placeholder text below with your actual project information.
> This file helps Claude understand your specific project context and requirements.

## Project Overview
<!-- Replace with 1-2 paragraphs describing your project -->
This is a [type of project] that [main purpose/goal]. It aims to [key objectives].

The project uses [brief technology overview] and is designed for [target audience/use case].

## Architecture
<!-- Describe your project's high-level architecture -->
The system follows a [architecture pattern] with the following main components:

### Key Components
<!-- List and describe your main components/modules -->
- **Component 1**: [Description of what it does]
- **Component 2**: [Description of what it does]
- **Component 3**: [Description of what it does]

### Technology Stack
<!-- Specify the languages and frameworks you're using -->
- **Primary Language(s)**: [e.g., Go, Rust, TypeScript]
- **Secondary Language(s)**: [e.g., Python for scripts, SQL for database]
- **Framework(s)**: [e.g., React, Django, Gin]
- **Database**: [e.g., PostgreSQL, MongoDB]
- **Testing**: [e.g., Jest, pytest, go test]
- **Infrastructure**: [e.g., Docker, Kubernetes, AWS]

## Development Setup

### Prerequisites
<!-- List required tools and minimum versions -->
- [Tool 1] version X.X+ (e.g., Node.js 18+)
- [Tool 2] version X.X+ (e.g., Go 1.21+)
- [Tool 3] version X.X+ (e.g., Docker 20+)

### Installation
```bash
# Clone the repository
git clone [your-repository-url]
cd [your-project-name]

# Install dependencies (adjust for your project)
npm install    # For Node.js projects
go mod download # For Go projects
pip install -r requirements.txt # For Python projects
```

### Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Required variables:
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
API_KEY=your-api-key
PORT=3000
# Add your actual environment variables here
```

## Key Commands
<!-- List the most important commands for your project -->

### Development
```bash
# Start development server
npm run dev         # or: go run . | python manage.py runserver

# Run tests
npm test           # or: go test ./... | pytest

# Lint code
npm run lint       # or: golangci-lint run | pylint src/

# Build for production
npm run build      # or: go build -o app | docker build .
```

### Database
```bash
# Run migrations
npm run migrate    # or your migration command

# Seed database
npm run seed       # or your seed command
```

## Coding Standards

### Code Style
<!-- Describe your project's coding standards -->
- Follow [language] community style guide
- Use [formatter] for automatic formatting
- Maximum line length: [X] characters
- Naming conventions:
  - Functions: [camelCase/snake_case]
  - Classes: [PascalCase]
  - Constants: [UPPER_SNAKE_CASE]

### Git Workflow
- Branch naming: `feature/description`, `fix/description`, `chore/description`
- Commit message format: `type(scope): description`
  - Types: feat, fix, docs, style, refactor, test, chore
- PR process:
  - All PRs require tests
  - Must pass CI/CD checks
  - Squash merge to main

### Testing Requirements
- All new features must include tests
- Maintain test coverage above [80]%
- Test file naming: `*.test.[ext]` or `*_test.[ext]`
- Include unit tests and integration tests

## Important Files and Directories

```
project-root/
├── src/              # Main source code
│   ├── components/   # UI components (if applicable)
│   ├── services/     # Business logic services
│   ├── models/       # Data models
│   └── utils/        # Utility functions
├── tests/            # Test files
├── docs/             # Documentation
├── scripts/          # Build and utility scripts
└── config/           # Configuration files
```

## API Documentation
<!-- Link to or describe your API -->
- API Base URL: `https://api.yourproject.com/v1`
- Authentication: [Bearer token / API key / etc.]
- Main endpoints:
  - `GET /users` - List users
  - `POST /users` - Create user
  - [Add your actual endpoints]

## Deployment

### Staging
```bash
# Deploy to staging
./scripts/deploy-staging.sh
# or: git push staging main
```

### Production
```bash
# Deploy to production
./scripts/deploy-production.sh
# or: git push production main
```

## Troubleshooting

### Common Issues
1. **Issue**: [Common problem]
   **Solution**: [How to fix it]

2. **Issue**: [Another common problem]
   **Solution**: [How to fix it]

## Project-Specific Guidelines

### Performance Considerations
<!-- Any performance-critical aspects Claude should know about -->
- [e.g., This service handles high traffic, optimize for throughput]
- [e.g., Memory usage is critical, avoid large allocations]

### Security Requirements
<!-- Security considerations for the project -->
- [e.g., All user input must be validated]
- [e.g., Use prepared statements for all SQL queries]
- [e.g., Sensitive data must be encrypted at rest]

### Business Rules
<!-- Important business logic Claude should be aware of -->
- [e.g., Users can only access their own data]
- [e.g., Transactions must be idempotent]
- [e.g., Specific calculation formulas or rules]

## Additional Notes
<!-- Any other important information -->
- [Project-specific conventions]
- [Integration points with other systems]
- [Known limitations or technical debt]
- [Future considerations]