# GitHub Copilot Instructions for Agentic AI BCI Research Assistant

## Project Context

This is an Agentic AI Assistant designed to support Brain-Computer Interface (BCI) research. The system uses LangChain agents powered by Claude to help neuroscience researchers with dataset analysis, experiment planning, and research synthesis.

## Domain-Specific Knowledge

### Neuroscience & BCI Terminology
- Use proper neuroscience terminology (EEG, MEG, fMRI, etc.)
- Understand signal processing concepts (filtering, epoching, artifacts)
- Be familiar with experimental paradigms (P300, SSVEP, motor imagery)
- Know common datasets (OpenNeuro, PhysioNet, BNCI Horizon 2020)

### Research Workflow Understanding
- Literature review and synthesis
- Experiment design and protocol development
- Data collection and preprocessing
- Statistical analysis and interpretation
- Result visualization and reporting

## Technical Guidelines

### LangChain Agent Patterns
- Prefer agent-based architecture with specialized roles
- Use proper tool calling and chain-of-thought reasoning
- Implement memory and context management
- Follow agentic workflow patterns

### Code Organization
- Separate concerns into agents, services, and models
- Use dependency injection for better testing
- Implement proper error handling and logging
- Follow async/await patterns for API calls

### API Integration
- Handle rate limiting gracefully
- Implement proper caching strategies
- Use structured outputs for consistency
- Validate inputs and outputs

## Naming Conventions

### Classes
- Agents: `*Agent` (e.g., `DataQueryAgent`, `AnalysisAgent`)
- Services: `*Service` (e.g., `DatasetService`, `AnalysisService`)
- Models: Domain-specific names (e.g., `Dataset`, `Experiment`, `Signal`)

### Functions
- Use descriptive names for research operations
- Prefix async functions appropriately
- Use verb-noun patterns (e.g., `analyze_signal`, `generate_summary`)

### Variables
- Use domain-specific abbreviations when clear (eeg_data, meg_signal)
- Prefer full words for clarity in research context

## AI Assistant Behavior

### Response Style
- Be scientific and precise in language
- Provide citations and references when relevant
- Explain complex concepts clearly
- Suggest best practices from neuroscience research

### Error Handling
- Provide meaningful error messages for researchers
- Suggest alternative approaches when methods fail
- Include troubleshooting steps for common issues

### Documentation
- Include docstrings with research context
- Provide examples relevant to BCI research
- Reference relevant papers or standards

## Integration Patterns

### Dataset Handling
- Use standardized formats (BIDS, EDF, etc.)
- Implement proper metadata extraction
- Handle large file processing efficiently
- Provide data quality assessments

### Visualization
- Create publication-ready plots
- Use neuroscience-standard color schemes
- Include proper axis labels and legends
- Support interactive exploration

### Analysis Pipeline
- Follow reproducible research practices
- Implement parameter tracking
- Support batch processing
- Enable result comparison

## Security & Privacy

### Data Protection
- Never store sensitive research data
- Implement proper access controls
- Use encryption for data in transit
- Follow research ethics guidelines

### API Security
- Validate all inputs thoroughly
- Implement rate limiting
- Use secure authentication
- Log security events properly

## Testing Guidelines

### Unit Tests
- Test agent logic thoroughly
- Mock external API calls
- Test error conditions
- Validate output formats

### Integration Tests
- Test dataset integration flows
- Validate analysis pipelines
- Test UI interactions
- Check performance benchmarks

Remember: This tool supports critical neuroscience research. Prioritize accuracy, reliability, and scientific rigor in all suggestions.
