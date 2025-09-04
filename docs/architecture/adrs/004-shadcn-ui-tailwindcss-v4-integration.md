# ADR-004: shadcn/ui and TailwindCSS v4.0 Integration

## Status
**Accepted** - September 4, 2025

## Context

The tearsheet application previously used basic Tailwind CSS with custom component styling. To improve user experience, accessibility, and design consistency, we needed to integrate a modern component library with proper theme support.

### Previous State
- Basic TailwindCSS v3 configuration with JavaScript config file
- Custom-styled form components without consistent design system
- Limited accessibility features
- No dark/light theme support
- Manual component styling requiring ongoing maintenance

### Requirements
- Modern, accessible UI component library
- Professional black/white theme design
- Dark/light mode theme switching
- TailwindCSS compatibility
- TypeScript support throughout
- Responsive design

## Decision

We decided to integrate **shadcn/ui component library** with **TailwindCSS v4.0** using a CSS-first configuration approach.

### Implementation Strategy

1. **TailwindCSS v4.0 Upgrade**: Migrate to CSS-first configuration
2. **shadcn/ui Integration**: Manual component installation due to CLI compatibility issues
3. **Theme System**: Black/white theme with next-themes for mode switching
4. **Component Transformation**: Convert all UI elements to shadcn/ui patterns

## Rationale

### Benefits of shadcn/ui

1. **Modern Components**: Copy-and-paste components with full customization
2. **Accessibility**: Built-in ARIA attributes and keyboard navigation
3. **TypeScript Native**: Full type safety with proper interfaces
4. **Radix UI Foundation**: Battle-tested component primitives
5. **Customization**: Full control over component styling and behavior
6. **No Runtime Dependencies**: Components copied into codebase

### Benefits of TailwindCSS v4.0

1. **CSS-First Configuration**: Eliminates JavaScript config file complexity
2. **Built-in Features**: Container queries, nesting, and modern CSS features
3. **Performance**: Faster compilation and smaller bundle sizes
4. **Theme Variables**: Native CSS custom property support
5. **Developer Experience**: Better IntelliSense and debugging

## Implementation Details

### TailwindCSS v4.0 Configuration

**PostCSS Configuration (`postcss.config.mjs`):**
```javascript
const config = {
  plugins: ["@tailwindcss/postcss"],
};
export default config;
```

**CSS Theme Configuration (`globals.css`):**
```css
@import "tailwindcss";

@theme {
  --color-background: 0 0% 100%;
  --color-foreground: 0 0% 3.9%;
  --color-primary: 0 0% 9%;
  --color-primary-foreground: 0 0% 98%;
  /* ... complete color system ... */
}

.dark {
  @theme {
    --color-background: 0 0% 3.9%;
    --color-foreground: 0 0% 98%;
    /* ... dark mode overrides ... */
  }
}
```

### shadcn/ui Component Integration

**Manual Installation Process:**
1. Install core dependencies: `@radix-ui/react-label`, `@radix-ui/react-slot`, `class-variance-authority`, `next-themes`, `lucide-react`
2. Create utility functions in `src/lib/utils.ts`
3. Manually create components in `src/components/ui/`
4. Transform existing components to use shadcn/ui patterns

**Key Components Created:**
- `Button` - Primary, secondary, destructive variants
- `Input` - Form input with proper focus states
- `Label` - Accessible form labels
- `Card` - Container components with header/content sections
- `Select` - Form select inputs
- `Table` - Data display components with proper styling
- `Badge` - Status and tag display
- `ThemeToggle` - Dark/light mode switcher

### Component Transformation Examples

**Before (Custom Styling):**
```tsx
<form className="space-y-6 bg-white p-6 rounded-lg shadow">
  <input className="w-full p-3 border rounded" />
  <button className="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
</form>
```

**After (shadcn/ui):**
```tsx
<Card>
  <CardHeader>
    <CardTitle>Form Title</CardTitle>
  </CardHeader>
  <CardContent>
    <form className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="input">Field Label</Label>
        <Input id="input" placeholder="Enter value..." />
      </div>
      <Button type="submit">Submit</Button>
    </form>
  </CardContent>
</Card>
```

### Theme Provider Setup

**Theme Provider (`src/components/theme-provider.tsx`):**
```tsx
import { ThemeProvider as NextThemesProvider } from "next-themes";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      {...props}
    >
      {children}
    </NextThemesProvider>
  );
}
```

## Consequences

### Positive Consequences

1. **Enhanced User Experience**: Professional, consistent design throughout application
2. **Improved Accessibility**: Built-in ARIA support and keyboard navigation
3. **Development Efficiency**: Reusable components reduce development time
4. **Theme Consistency**: Unified black/white theme with seamless dark mode
5. **Type Safety**: Full TypeScript integration prevents runtime errors
6. **Future Maintenance**: Well-documented components easy to maintain and extend

### Challenges Overcome

1. **CLI Compatibility**: shadcn/ui CLI incompatible with TailwindCSS v4.0
   - **Solution**: Manual component installation and configuration
2. **Configuration Conflicts**: TailwindCSS v3/v4 mixed configuration
   - **Solution**: Complete migration to v4.0 CSS-first approach
3. **TypeScript Errors**: Component type definition issues
   - **Solution**: Proper React HTML attribute types for all components

### Technical Debt Resolved

1. **Inconsistent Styling**: Replaced custom styles with design system
2. **Accessibility Gaps**: Added proper ARIA attributes and keyboard support
3. **Theme Management**: Implemented proper theme switching infrastructure
4. **Component Reusability**: Created reusable component library

## Implementation Status

### Completed Components ✅
- ✅ Button (variants: default, secondary, destructive, outline, ghost, link)
- ✅ Input (text, email, password inputs with proper styling)
- ✅ Label (accessible form labels with proper associations)
- ✅ Card (header, content, footer sections)
- ✅ Select (form select inputs with consistent styling)
- ✅ Table (header, body, row, cell components)
- ✅ Badge (variants: default, secondary, destructive, outline)
- ✅ ThemeToggle (sun/moon icon toggle with next-themes)

### Transformed Pages ✅
- ✅ Home page (`/`) - Portfolio analysis form and tearsheet display
- ✅ Ratios page (`/ratios`) - Financial ratios analysis interface
- ✅ Layout - Navigation and theme provider integration

### Configuration ✅
- ✅ TailwindCSS v4.0 CSS-first configuration
- ✅ PostCSS plugin setup
- ✅ Theme variables and dark mode support
- ✅ next-themes provider integration

## Performance Impact

### Bundle Size Improvements
- **TailwindCSS v4.0**: Smaller CSS bundle with better tree-shaking
- **shadcn/ui**: No runtime dependencies, only build-time impact
- **Component Efficiency**: Reduced custom CSS, leveraging utility classes

### Development Performance
- **Faster Compilation**: TailwindCSS v4.0 improved build times
- **Better DX**: IntelliSense support for theme variables
- **Type Safety**: Compile-time error detection vs. runtime issues

## Best Practices Established

### Component Development
1. **Consistent Patterns**: All components follow shadcn/ui conventions
2. **Type Safety**: Proper forwardRef with HTML element types
3. **Accessibility**: ARIA attributes and keyboard navigation built-in
4. **Customization**: className prop for style overrides when needed

### Theme Management
1. **CSS Variables**: Use `--color-*` naming convention
2. **Dark Mode**: `.dark` class selector for next-themes compatibility
3. **Color System**: HSL color space for better manipulation
4. **Responsive Design**: Mobile-first approach with Tailwind utilities

### Development Workflow
1. **Manual Component Creation**: Create shadcn/ui components manually when CLI incompatible
2. **TypeScript First**: Define proper types before implementation
3. **Testing Integration**: Ensure components work across theme modes
4. **Documentation**: Update CLAUDE.md with component patterns and troubleshooting

## Related Decisions

- **ADR-001**: Modular Architecture Adoption (supports component separation)
- **ADR-002**: Stateless Data Architecture (aligns with client-side theme state)
- **ADR-003**: QuantStats Tearsheet Simplification (maintains HTML-based approach)

## Future Considerations

1. **Component Library Expansion**: Add additional shadcn/ui components as needed
2. **Theme Customization**: Extend color palette for specialized use cases
3. **Animation System**: Consider Framer Motion integration for enhanced UX
4. **Component Testing**: Implement comprehensive component testing strategy

## Decision Date
September 4, 2025

## Decision Makers
- Development Team
- UI/UX Design Review

## Review Date
September 4, 2026 (Annual review recommended)