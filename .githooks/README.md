# Git Hooks

This repo uses a custom hooks directory.

Setup:
- Run: git config core.hooksPath .githooks

Behavior:
- pre-commit updates main.css cache-busting params when styles/main.css is staged.
