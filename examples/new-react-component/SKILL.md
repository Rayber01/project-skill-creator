---
name: new-react-component
description: Scaffolds a React component with TypeScript, Tailwind styles, a Jest test and a Storybook story following the project layout. Use when the user asks to create, add or scaffold a UI component. Do not use for editing existing components.
---

# New React component

Create a component bundle that follows the project conventions.

## Steps
1. Ask for the component name (PascalCase) and its props if they were not given.
2. Look in `src/components/ui/` for a component with a similar name; reuse or extend it instead of duplicating.
3. Create `src/components/ui/<Name>/<Name>.tsx` exporting a typed `<Name>Props` interface.
4. Create `<Name>.test.tsx` covering the default render and one interaction.
5. Create `<Name>.stories.tsx` with a default story.
6. Export the component from `src/components/ui/index.ts`.
7. Run the project's test and lint commands and fix any failure.

## Done when
- The three files exist, the index exports the component and tests and lint pass.
