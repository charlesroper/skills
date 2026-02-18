# MaintainableCSS Manual (Condensed)

Source: https://maintainablecss.com/

## 1) Introduction

- MaintainableCSS is about modular, scalable, maintainable CSS.
- Goal: make changes safely as codebase size grows.

## 2) Semantics

- Prefer semantic class names over visual/utility naming.
- Semantic names improve readability, searchability, debugging, JS hooks, and test hooks.
- They reduce accidental global regressions.

## 3) Reuse

- Avoid forced DRY.
- Prefer clarity over clever abstraction.
- Duplication is often safer than brittle shared abstractions.
- Reuse carefully when patterns are truly stable.

## 4) IDs

- Do not use IDs as style hooks due to specificity issues.
- IDs remain valid for semantics/accessibility needs.

## 5) Conventions

Core pattern:

```css
.module {}
.module-component {}
.module-isState {}
```

- Prefix component/state with module name.
- Keep naming consistent and predictable.

## 6) Modules

- A module is an independent unit.
- Components are required parts inside a module.
- Similar visuals do not guarantee same module.
- Prefer separate modules to avoid entanglement.

## 7) State

- Model visual state with explicit classes (for example `module-isEmpty`).
- Keep state local to module unless state and visuals are truly shared.
- Do not rely on ARIA attributes alone for styling.

## 8) Modifiers

- Use modifiers for small, well-understood differences.
- Pattern: `module--variant`.
- If differences become large, split into a separate module.

## 9) Versioning

- For A/B tests or migrations, duplicate module with a new name (`module2`).
- Remove old version after rollout decision.

## 10) JavaScript

- JS can share behavior across modules while CSS remains module-specific.
- Global state class is acceptable only when both behavior and style are identical.

## 11) Organisation

- Organize so code is easy to find.
- Either central CSS with clear structure or feature/module-local CSS.
- Avoid over-fragmentation that harms maintainability.

## 12) FAQs

- Global element styles are acceptable when truly universal.
- Otherwise prefer module encapsulation.
- Keep breakpoints and state near the module they affect.

## Practical Refactor Heuristics

- Rename by meaning, not appearance.
- Replace deep selector chains with explicit component classes.
- Keep specificity low.
- Prefer maintainable duplication over risky shared abstractions.
- Ensure deletability: code should be easy to remove when no longer needed.
