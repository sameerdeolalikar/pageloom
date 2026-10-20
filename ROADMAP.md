# PageLoom: development plan

Estimated future effort: **74–110 hours**. These milestones are proposed, not implemented or approved paid work. Reassess scope after practical use.

## 1. Text engine and overflow feedback — 18–26 hours

Add measured wrapping, Unicode shaping considerations, paragraph alignment and explicit overflow recovery. Keep print output and editor line breaks consistent.

Definition of done: documented behavior, regression tests, matched before/after UI evidence where visible, valid import/export, and preservation of current undo and storage behavior.

## 2. Selection and composition tools — 14–22 hours

Add multi-selection, snap guides, alignment, grouping and rotation with coherent undo and a keyboard alternative.

Definition of done: documented behavior, regression tests, matched before/after UI evidence where visible, valid import/export, and preservation of current undo and storage behavior.

## 3. Pages and assets — 16–24 hours

Add multi-page documents and original/local image assets with size/type checks and portable exports. Define crop and aspect-ratio behavior and preserve source provenance.

Definition of done: documented behavior, regression tests, matched before/after UI evidence where visible, valid import/export, and preservation of current undo and storage behavior.

## 4. Output fidelity — 14–20 hours

Add PDF output, print margins/bleed controls and font handling. Compare rendered exports with the editor using deterministic fixtures and physical print checks.

Definition of done: documented behavior, regression tests, matched before/after UI evidence where visible, valid import/export, and preservation of current undo and storage behavior.

## 5. Editor resilience and accessibility — 12–18 hours

Add recoverable drafts, revision conflict review, long layer-list navigation, focus restoration and reduced-motion/RTL verification.

Definition of done: documented behavior, regression tests, matched before/after UI evidence where visible, valid import/export, and preservation of current undo and storage behavior.

## Suggested first session

Add measured text wrapping and explicit overflow controls, preserving line breaks and export fidelity after resizing and undo.

## Delivery order

Freeze the user-visible requirement and a passing control before implementation. Finish one bounded feature at a time; do not combine all milestones into one evaluation prompt. Record implemented behavior and remaining limitations in the README after each release.
