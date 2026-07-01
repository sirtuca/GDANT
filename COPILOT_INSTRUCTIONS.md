# GDANT Development Instructions

## Project Objective

GDANT is a desktop application whose only objective is to transform Administrative Process PDFs into Debt Registration Terms (DOCX and PDF).

The application must always prioritize:

- Simplicity
- Speed
- Stability
- Maintainability

Never add features that were not explicitly requested.

---

## Architecture

Business rules must NEVER be hardcoded inside the application.

The software is only responsible for:

- Reading PDFs
- Organizing extracted information
- Applying the selected Template
- Generating DOCX
- Exporting PDF

Business logic evolves outside the software through the Manual Técnico and Template Mestre.

---

## Development Rules

- Never commit directly to main.
- Develop only on develop branch.
- Keep modules small.
- One responsibility per file whenever possible.
- Prefer readability over abstraction.
- Avoid unnecessary frameworks.
- Keep dependencies to a minimum.
- Always preserve backward compatibility.

---

## UI Philosophy

The application must remain extremely simple.

Main window:

- Template Mestre
- Manual Técnico
- Input Folder
- Output Folder
- Generate DOCX
- Generate PDF
- GERAR TERMOS

Nothing else unless explicitly requested.

---

## Performance

Optimize for processing dozens of PDFs.

The application should be able to process large batches efficiently.

---

## Code Style

- Pythonic
- Typed whenever reasonable
- Well documented
- Modular
- Clean
- Easy to read

---

## Golden Rule

If there is any doubt about implementing a feature, stop and ask instead of making assumptions.
