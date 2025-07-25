# Test Command

Run the project's test suite and analyze results.

## Steps

1. Pre-test checks
   - Ensure environment is set up
   - Check for test configuration
   - Clear test cache if needed

2. Run tests
   - Execute the project's test command
   - Run unit tests
   - Run integration tests if available
   - Check code coverage

3. Analyze results
   - Report passed/failed tests
   - Show coverage metrics
   - Identify failing tests

4. Handle failures
   - For failing tests:
     - Show error details
     - Analyze failure reasons
     - Suggest fixes if possible

5. Coverage analysis
   - Identify uncovered code
   - Suggest areas needing tests
   - Compare with coverage thresholds

6. Performance
   - Report slow tests
   - Suggest optimizations

## Options

- Run specific test file: Include file path
- Run tests in watch mode for development
- Generate coverage report

## Usage

```
/test
```

Run regularly during development and before commits.