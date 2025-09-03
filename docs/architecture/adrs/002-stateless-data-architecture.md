# ADR-002: Stateless Data Architecture

## Status

Accepted

## Context

The tearsheet portfolio analyzer needs to handle financial data for analysis and reporting. Key considerations include:

- **Data Sensitivity**: Financial portfolio data is sensitive and should not be permanently stored
- **Regulatory Compliance**: Potential data privacy regulations require careful data handling
- **Performance**: Real-time analysis requires efficient data processing
- **Scalability**: System should support multiple concurrent users
- **Reliability**: External API dependencies (VNStock) require robust error handling

Initial options considered:
1. Database-backed persistent storage for user portfolios and analysis history
2. File-based storage for caching and user data
3. Stateless, in-memory processing with no permanent storage

## Decision

We will implement a **stateless, in-memory data architecture** with the following characteristics:

- **No Persistent Storage**: No databases or permanent file storage of user data
- **Real-time Data Retrieval**: All data fetched on-demand from external APIs
- **In-Memory Processing**: Data exists only during request lifecycle
- **Temporary File Generation**: Reports generated as temporary files, cleaned up regularly
- **Session-based State**: Minimal session data for user experience, not business data

### Architecture Components:
1. **External API Integration**: VNStock API for market data and financial ratios
2. **In-Memory Data Models**: Pandas DataFrames and Python objects for processing
3. **Stateless Services**: Services that don't maintain internal state between requests
4. **Temporary Report Generation**: HTML/Excel files generated on-demand

## Consequences

### Positive Consequences

- **Enhanced Privacy**: No permanent storage of sensitive financial data
- **Simplified Architecture**: No database management, backup, or data migration concerns
- **Better Security**: Reduced attack surface, no persistent data to compromise
- **Regulatory Compliance**: Easier to comply with data privacy regulations
- **Scalability**: Stateless services easier to scale horizontally
- **Fresh Data**: Always uses latest market data from authoritative sources
- **Simplified Deployment**: No database setup or migration scripts required

### Negative Consequences

- **Performance Impact**: No caching of historical data, repeated API calls
- **External Dependencies**: Heavy reliance on VNStock API availability
- **Limited Offline Capability**: Cannot function without internet connectivity
- **No Analysis History**: Users cannot review previous analyses
- **API Rate Limits**: Potential throttling from external data providers

### Risk Mitigation

- **Error Handling**: Comprehensive error handling for API failures
- **Caching Strategy**: Short-term, in-memory caching during request processing
- **API Monitoring**: Monitor external API health and response times
- **Graceful Degradation**: Provide meaningful error messages when data unavailable
- **Performance Optimization**: Efficient data processing algorithms

## Implementation

### Timeline

- **Phase 1 (Completed)**: Remove any persistent storage mechanisms
- **Phase 2 (Completed)**: Implement stateless service architecture
- **Phase 3 (Completed)**: Add comprehensive error handling for external dependencies
- **Phase 4 (Completed)**: Optimize data processing performance

### Resources Required

- Development time for stateless service implementation
- Testing infrastructure for external API integration
- Monitoring setup for external dependency health

### Dependencies

- VNStock API reliability and performance
- Network connectivity requirements
- External API rate limits and terms of service

## Alternatives Considered

1. **PostgreSQL Database**: Relational database for portfolio and analysis storage
   - **Rejected**: Adds complexity, data privacy concerns, regulatory compliance overhead

2. **SQLite Local Storage**: Lightweight local database
   - **Rejected**: Still involves persistent storage of sensitive data

3. **Redis Caching**: In-memory database for session and temporary data storage
   - **Considered**: Could be future enhancement for performance optimization

4. **File-based Caching**: Local file system caching of API responses
   - **Rejected**: Data persistence concerns, cleanup complexity

5. **Hybrid Approach**: Cache non-sensitive reference data, process portfolios in-memory
   - **Future Consideration**: Could optimize performance while maintaining privacy

## References

- [Twelve-Factor App Methodology - Stateless Processes](https://12factor.net/processes)
- [GDPR Data Protection Principles](https://gdpr-info.eu/art-5-gdpr/)
- [Stateless vs Stateful Architecture](https://docs.microsoft.com/en-us/azure/architecture/guide/architecture-styles/)
- [Financial Data Privacy Best Practices](https://www.sec.gov/files/data-privacy-framework.pdf)