# Contributing to AI Proposal Writer

First off, thank you for considering contributing to AI Proposal Writer! It's people like you that make open-source software such a great community.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](../../issues) page to see if someone else has already created a ticket. If not, go ahead and make one!

## Fork & create a branch

If this is something you think you can fix, then fork AI Proposal Writer and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-stripe-integration
```

## Local Development

Please refer to the `README.md` for local setup instructions for the Python backend and HTML/JS frontend.

1. Ensure the backend runs locally via `uvicorn`.
2. Ensure you have tested your frontend changes across different screen sizes.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Styleguides

### Code Style
- **Python:** We follow PEP 8. Please run your code through `flake8` or `black` before submitting.
- **JavaScript/CSS:** Standard ES6+ conventions. Keep DOM manipulations modular. Avoid inline styles where possible; use `style.css`.
- **Commits:** We prefer Conventional Commits (e.g., `feat: add new scope generator`, `fix: resolve pdf alignment issue`).
