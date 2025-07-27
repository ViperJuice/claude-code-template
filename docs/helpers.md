# Helper Scripts

Claude Code Template provides several helper scripts to streamline development.

## Quick Setup

```bash
./scripts/setup.sh
```

Sets up the Claude Code template by:
- Creating required directories
- Installing Python dependencies
- Configuring git worktree
- Creating example project structures
- Running template validation

## Validation

```bash
./scripts/validate.sh
```

Validates your template setup by checking:
- Required directories and files
- Python dependencies
- Integration tests
- Example project structure
- Inventory check

## Example Projects

```bash
# Run all examples
./scripts/run-examples.sh

# Run specific example
./scripts/run-examples.sh python-ml-typescript-api
```

Runs the example projects with language-specific commands:

### rust-go-microservices
- Builds both services
- Starts services in background
- Runs integration tests

### python-ml-typescript-api
- Installs dependencies
- Starts ML service and API gateway
- Tests sentiment predictions

### cpp-java-python-engine
- Builds C++ engine
- Compiles Java wrapper
- Builds Python bindings
- Runs performance benchmarks

## Best Practices

1. **Always validate after setup**
   ```bash
   ./scripts/validate.sh
   ```

2. **Test with examples first**
   ```bash
   ./scripts/run-examples.sh
   ```

3. **Use examples as templates**
   ```bash
   cp examples/rust-go-microservices my-project
   ```

4. **Regular validation**
   ```bash
   # After making changes
   ./scripts/validate.sh
   ```

## Common Issues

### Setup Script Fails
- Check Python version (3.8+ required)
- Verify pip installation
- Check for required system packages

### Example Project Fails
- Ensure all dependencies are installed
- Check language-specific requirements
- Verify port availability

### Validation Fails
- Check directory structure
- Verify file permissions
- Install missing dependencies
- Fix test failures