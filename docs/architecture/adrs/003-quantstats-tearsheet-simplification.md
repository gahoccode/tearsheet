# ADR-003: QuantStats Tearsheet Simplification

## Status
**Accepted** - January 4, 2025

## Context

During the development of the Next.js + Flask API architecture (v2.0), we initially implemented complex custom chart visualizations using Plotly.js. This approach involved:

- Custom chart data services generating Plotly configurations
- Complex React components for chart rendering
- Heavy client-side JavaScript bundles
- Custom chart layouts and interactions
- Multiple API endpoints for different chart types

However, this approach introduced unnecessary complexity and reinvented functionality already provided by the proven QuantStats library.

## Decision

We decided to **simplify the visualization approach** by returning to QuantStats-generated HTML tearsheets instead of custom chart implementations.

### Implementation Approach

1. **Backend**: Use `qs.reports.html()` to generate complete HTML tearsheets
2. **Frontend**: Display HTML content using React's `dangerouslySetInnerHTML`
3. **API Design**: Single `/api/tearsheet` endpoint returning HTML content
4. **Cleanup**: Remove all custom chart components and Plotly.js dependencies

## Rationale

### Benefits of QuantStats HTML Tearsheets

1. **Proven Solution**: QuantStats is a battle-tested library used by financial professionals
2. **Comprehensive Reports**: Complete tearsheets with all necessary visualizations
3. **Simplicity**: Single API endpoint vs. multiple chart data endpoints
4. **Performance**: No heavy client-side chart libraries required
5. **Reliability**: Stable, well-documented library with consistent output
6. **Professional Quality**: Industry-standard tearsheet formatting

### Problems with Custom Plotly.js Implementation

1. **Complexity**: Multiple chart components, data services, and configurations
2. **Maintenance Burden**: Custom chart logic requires ongoing maintenance
3. **Bundle Size**: Heavy Plotly.js library increased frontend bundle size
4. **Reinvention**: Duplicating functionality already provided by QuantStats
5. **Development Time**: Significant effort to recreate proven tearsheet features

## Implementation Details

### Backend Implementation
```python
@app.route("/api/tearsheet", methods=["POST"])
def generate_tearsheet():
    # ... validation and data processing ...
    
    # Generate QuantStats HTML tearsheet
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    qs.reports.html(
        portfolio_returns,
        title=portfolio_name,
        output=temp_file_path,
        # ... configuration parameters ...
    )
    
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    os.unlink(temp_file_path)  # Cleanup
    
    return jsonify({"html": html_content, ...})
```

### Frontend Implementation
```typescript
function QuantStatsTearsheet({ htmlContent }: { htmlContent: string }) {
  return (
    <div 
      className="quantstats-tearsheet"
      dangerouslySetInnerHTML={{ __html: htmlContent }}
    />
  );
}
```

### Cleanup Actions
1. ✅ Removed `frontend/src/components/charts/` directory
2. ✅ Uninstalled Plotly.js dependencies from package.json
3. ✅ Cleaned up TypeScript interfaces for chart data
4. ✅ Updated API client to use tearsheet endpoint
5. ✅ Updated React components to use tearsheet display

## Consequences

### Positive Consequences

1. **Reduced Complexity**: Significant reduction in codebase size and complexity
2. **Improved Performance**: Faster frontend bundle, no heavy chart libraries
3. **Enhanced Reliability**: Using proven QuantStats library instead of custom implementations
4. **Faster Development**: Less custom code to maintain and debug
5. **Professional Output**: Industry-standard tearsheet formatting and visualizations
6. **Better User Experience**: Consistent, professional reports

### Potential Limitations

1. **HTML Rendering**: Using `dangerouslySetInnerHTML` requires trust in QuantStats output
2. **Customization**: Limited ability to customize tearsheet appearance
3. **Interactivity**: HTML tearsheets may be less interactive than custom charts
4. **Styling Integration**: QuantStats styling may not match application theme

### Mitigation Strategies

1. **Security**: QuantStats is a trusted library with safe HTML output
2. **Customization**: QuantStats provides sufficient configuration options
3. **CSS Override**: Custom CSS can be applied to tearsheet container
4. **Future Enhancement**: Custom charts can be added alongside tearsheets if needed

## Related Decisions

- **ADR-001**: Modular Architecture Adoption (supports microservices separation)
- **ADR-002**: Stateless Data Architecture (aligns with temporary file approach)

## Implementation Status

- ✅ Backend tearsheet endpoint implemented
- ✅ Frontend tearsheet component created
- ✅ Plotly.js cleanup completed
- ✅ Full stack integration tested
- ✅ Documentation updated

## Lessons Learned

1. **Simplicity Over Complexity**: Choose proven solutions over custom implementations
2. **Library Evaluation**: Thoroughly evaluate existing solutions before building custom
3. **Incremental Adoption**: Consider phased approaches for major architectural changes
4. **User Feedback**: Early user feedback helps identify over-engineering
5. **Technical Debt**: Custom implementations create maintenance burden

## Decision Date
January 4, 2025

## Decision Makers
- Development Team
- Technical Architecture Review

## Review Date
January 4, 2026 (Annual review recommended)