# Contributing to RagaNotate

Thank you for your interest in contributing to **RagaNotate**!

This project aims to build the definitive open-source Carnatic music notation engine for both human musicians and AI/ML systems.

---

## Ways to Contribute

- **Notation corrections** — Improvements to swara, gamaka, or tala specifications
- **New compositions** — Annotated examples in the `examples/` folder
- **Bug fixes** — Issues in the TypeScript library or Python package
- **Documentation** — Improve `SPEC.md`, `README.md`, or add examples
- **Dataset annotations** — Add compositions to `dataset/annotated/`
- **Feature development** — See the [roadmap in README.md](README.md#roadmap)

---

## Getting Started

1. Fork the repository: [github.com/jags111/RagaNotate](https://github.com/jags111/RagaNotate)
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/RagaNotate.git
   cd RagaNotate
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes, test them, and commit:
   ```bash
   git commit -m "feat: describe your change"
   ```
5. Push and open a Pull Request to `main`.

---

## Commit Message Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:     New feature or capability
fix:      Bug fix
docs:     Documentation only
spec:     Notation specification update
refactor: Code change (no new feature, no bug fix)
test:     Adding or updating tests
chore:    Build / tooling / CI changes
dataset:  Addition or update to annotated music data
```

Examples:
```
feat: add kampita gamaka pitch contour to renderer
fix: correct Prati Madhyamam frequency ratio (45/32)
spec: add Sankeerna Chapu tala anga breakdown
dataset: annotate Vathapi Ganapathim in Adi tala
```

---

## Code Style

**Python:** Follow PEP 8. Use type hints. Run `ruff` for linting.

**TypeScript:** Strict mode enabled. Use ESLint + Prettier. No `any` types.

---

## Notation Spec Changes

Changes to `SPEC.md` or any file in `spec/` must be discussed in an Issue first, as these affect all downstream consumers (Python package, TypeScript library, dataset format).

---

## Author

**Jags** · [@jags111](https://github.com/jags111)

---

*This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).*
