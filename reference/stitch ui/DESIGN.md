# Design System Strategy: The Clinical Ethereal

## 1. Overview & Creative North Star
The "Clinical Ethereal" is our North Star. In the high-stakes, high-cognitive-load environment of medical professionals, traditional "boxy" software adds unnecessary mental friction. This design system rejects the rigid, spreadsheet-like interfaces common in healthcare. Instead, we embrace a **Digital Sanctuary** approach—a high-fidelity, editorial experience that feels as calm as it is efficient.

We break the "standard template" look through **Intentional Asymmetry** and **Tonal Depth**. By moving away from 1px borders and hard lines, we create an interface that feels less like a database and more like a curated workspace. We prioritize breathing room (white space) to ensure that critical patient data is never lost in visual noise.

## 2. Colors & Surface Philosophy
The palette is a sophisticated mix of deep oceanic blues (`primary`), organic teals (`secondary`), and slate-toned neutrals. 

### The "No-Line" Rule
Standard 1px borders are strictly prohibited for sectioning or containment. Boundaries must be defined through **Background Color Shifts**. For example, a sidebar should use `surface-container-low` while the main workspace sits on `surface`. This creates a cleaner, more modern "app-as-a-canvas" feel.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of frosted glass.
*   **Base:** `surface` (#f8f9fa)
*   **Sectioning:** `surface-container-low` (#f3f4f5) for large organizational blocks.
*   **High-Priority Focus:** `surface-container-lowest` (#ffffff) for active cards or data entry points to make them pop against the background.
*   **Overlays:** Use `surface-bright` for hover states or temporary focus areas.

### The "Glass & Gradient" Rule
To elevate the "JR Journal" beyond a generic tool, use Glassmorphism for floating elements (modals, popovers). Apply a semi-transparent `surface` color with a `20px` backdrop-blur. 
*   **Signature Gradients:** For primary CTAs, do not use flat hex codes. Apply a subtle linear gradient from `primary` (#005e96) to `primary_container` (#0277bd) at a 135-degree angle. This adds a "jewel-like" depth that signals professional premium quality.

## 3. Typography: The Editorial Scale
We use a dual-font strategy to balance authority with readability.

*   **The Authority (Manrope):** Used for `display` and `headline` tiers. Its geometric yet friendly curves provide a modern, high-end editorial feel. Use `display-lg` (3.5rem) sparingly for dashboard welcomes to establish a sense of calm.
*   **The Precision (Inter):** Used for `title`, `body`, and `label` tiers. Inter is the industry standard for legibility in data-dense environments.
    *   **Scale Contrast:** Use `title-lg` (Inter, 1.375rem) for section headers to create a clear "anchor" for the eye, contrasting sharply with `label-sm` (Inter, 0.6875rem) for metadata.

## 4. Elevation & Depth
Depth is a functional tool, not a decoration. We convey hierarchy through **Tonal Layering** rather than structural lines.

*   **Ambient Shadows:** For floating elements like modals or tooltips, use "Ambient Shadows." These are extra-diffused. 
    *   *Spec:* `0px 12px 32px rgba(25, 28, 29, 0.06)`. The shadow color is a low-opacity version of `on_surface` to mimic natural light.
*   **The Ghost Border Fallback:** If a border is required for accessibility (e.g., in high-contrast modes), use a "Ghost Border": `outline_variant` at 15% opacity. Never use 100% opaque borders.
*   **Interactive Glow:** When an element is focused or active (like a selected journal entry), apply a subtle outer glow using the `primary_fixed` color (#cfe5ff) with a `10px` blur. This simulates a "lit-from-within" medical monitor effect.

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary_container`), `xl` roundedness (0.75rem). Subtle glow on hover.
*   **Secondary:** No fill. `ghost-border` (15% `outline`). Text in `primary`.
*   **Tertiary:** No border, no fill. High-contrast `on_surface_variant` text.

### Cards & Lists
*   **The "No-Divider" Rule:** Forbid 1px dividers between list items. Instead, use a `12px` vertical gap and a subtle background shift to `surface-container-highest` on hover. 
*   **Layout:** Use `xl` (0.75rem) rounded corners for cards to soften the medical aesthetic.

### Input Fields
*   **State:** Background should be `surface-container-highest`. Upon focus, the background shifts to `surface-container-lowest` (#ffffff) with a 2px `primary` bottom-border and the "Interactive Glow" effect.
*   **Labels:** Always use `label-md` in `on_surface_variant` for maximum clarity.

### Context-Specific Components
*   **The "Clinical Pulse" Chip:** Use for status indicators (e.g., "Active," "Pending"). Instead of solid blocks, use a light `secondary_container` background with `on_secondary_container` text and a small, pulsing dot to indicate live data.
*   **Timeline Scrubber:** A custom component for journaling. A thin `outline_variant` horizontal line with `primary` nodes, using `xl` rounding for the handle.

## 6. Do's and Don'ts

### Do
*   **DO** use whitespace as a separator. If in doubt, add 8px more padding.
*   **DO** use "Surface-Container" tiers to nest information (e.g., a white card on a light gray section).
*   **DO** use `secondary` (Teal/Green) for positive clinical outcomes or "success" states to create a calming psychological effect.

### Don't
*   **DON'T** use black (#000000) for text. Always use `on_surface` (#191c1d) to reduce eye strain for doctors working long shifts.
*   **DON'T** use traditional drop shadows that look "muddy." Stick to the Ambient Shadow spec.
*   **DON'T** use 1px solid dividers to separate patient data. It creates "visual bars" that make the user feel trapped. Use tonal shifts.