# Interactive explanations for personal reflection

Interactivity is optional. Use it only when the reader benefits from exploring a sequence, comparison, decision or state transition.

## Good uses

- reveal the stages of a habit loop;
- compare the user's old and new mental model;
- step through a decision process;
- inspect how an idea moves from a question to an action;
- show the sequence of a learning or feedback cycle.

## Requirements

- Use native button type="button" controls.
- Give every control a clear label and visible selected state such as aria-pressed.
- Use aria-live="polite" when an interaction updates explanatory status text.
- Keep a meaningful default state.
- Ensure the full static explanation remains understandable without JavaScript.
- Do not persist private journal content in browser storage.
- No analytics, remote requests, autoplay, flashing or gamification that pressures the user.
- Test that each control changes a meaningful explanatory state, not just color or decoration.

## Keep the interaction small

One interaction with five clear states is usually better than several unrelated widgets. The purpose is to deepen reflection, not increase screen time.
