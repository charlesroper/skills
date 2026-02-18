---
name: maintainable-css
description: Apply the MaintainableCSS methodology to plan, refactor, and review CSS and markup. Use when a user asks for scalable CSS architecture, semantic class naming, module/component/state/modifier conventions, lower-regression refactors, or migration away from utility/visual class patterns.
license: CC BY-NC-SA 4.0 concepts from maintainablecss.com, adapted for project use
metadata:
  author: Charles Roper
  based_on: Adam Silver’s MaintainableCSS
  source: https://maintainablecss.com/
  version: "1.0"
---

# Maintainable CSS Skill

Use this skill to implement the MaintainableCSS approach from Adam Silver in real codebases.

## Outcomes

- Make CSS easier to change without unexpected side effects.
- Keep selectors low-specificity and intention-revealing.
- Model UI as modules with clear components, states, and modifiers.

## When To Use

Activate this skill when tasks involve:

- CSS architecture or naming conventions
- refactoring legacy CSS with regression risk
- converting utility/visual classes to semantic classes
- introducing reusable UI modules
- adding stateful styling for JS-driven interfaces
- deciding what to duplicate vs abstract

## Canonical Convention

Use this naming pattern:

```css
.module {}
.module-component {}
.module-isState {}
.module--modifier {}
```

Conventions:

- Classes are semantic (what it is), not visual (what it looks like).
- Prefix components and states with module name.
- Modifiers are for small, well-understood differences only.
- Do not style with IDs.

## Working Rules (Do / Avoid)

Do:

- Build independent modules that can be added/removed safely.
- Keep selectors simple and predictable.
- Prefer explicit classes over deep descendant chains.
- Encapsulate module behavior and styles together.
- Duplicate when abstraction would introduce coupling.

Avoid:

- Utility/atomic class dependence as primary architecture.
- Premature DRY abstractions and large shared mixins.
- Intertwined modules that require override chains.
- ID selectors for styling.

## Standard Refactor Workflow

1. **Inventory**
   - List existing classes and selectors.
   - Identify candidate modules and components.

2. **Define names**
   - Create a rename map to semantic module-first classes.
   - Lock module/component/state/modifier names before editing.

3. **Refactor markup hooks first**
   - Update template/HTML classes to the new names.
   - Add explicit component classes where selectors rely on structure.

4. **Refactor CSS**
   - Rename selectors to match markup.
   - Reduce specificity and remove unnecessary chaining.
   - Keep global rules minimal and truly global.

5. **Handle state/modifiers**
   - Represent state with `module-isState`.
   - Use modifiers only for slight, controlled deltas.

6. **Prune and verify**
   - Remove dead selectors and obsolete hooks.
   - Run formatter/linter/build and perform visual spot checks.

## Reuse Decision Guide

When deciding whether to share CSS:

- If two pieces are conceptually different, keep separate modules even if they look similar.
- If styles are identical and stable, share with comma-delimited selectors or narrow shared primitives.
- If behavior is shared but visuals differ, share JS behavior and keep CSS module-specific.
- If both behavior and visuals are truly identical across modules, consider a global state class.

## Versioning / Experiments

For A/B tests or redesigns, create a parallel module name (for example `basket2`) instead of layering risky overrides into the original module.

## Organization Guidance

Choose one of:

- one CSS area with clear module sections, or
- module-oriented folders with module-local CSS.

In either case, keep code easy to find and easy to delete.

## Accessibility + Semantics

- Use IDs where required for semantics/accessibility wiring (labels, anchors, ARIA relationships), not as style hooks.
- Keep HTML semantic and readable; class names should aid both humans and tooling.

## Review Checklist

Before finishing, confirm:

- Class names are semantic and module-first.
- No ID selectors are used for styling.
- Components/states are module-prefixed.
- Modifiers are small and bounded.
- Selector specificity is low and predictable.
- Similar-looking but distinct features are not over-abstracted.

## References

- Chapter-by-chapter condensed guidance: `references/maintainable-css-manual.md`
