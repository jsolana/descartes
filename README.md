# Descartes

`Descartes` agent is a powerful tool designed to enhance and refine project documentation by leveraging the [Diataxis framework](https://diataxis.fr/).

## ✅ Running locally

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `make run` or just `make`

Also take into account that you will need to se these environment variables to be able to run the whole project:

- `OPENAI_API_KEY`
- `OPENAI_MODEL_NAME`
- Optionally:
  - `OPENAI_ORG`
  - `SERPER_API_KEY` to use [serper service](https://serper.dev/)

## Instructions

We are using Diátaxis framework for focusing the documentation. That means we are creating essentially 4 classes of documents:

- Tutorials: Lessons that provide a learning experience, taking users step-by-step through hands-on exercises to build skills and familiarity.
- How-to's: Practical guides focused on providing the steps to solve real-world problems.
- Explanation: Background information and conceptual discussions that provide context and illuminate topics more broadly.
- Reference: Technical descriptions and factual information about the system, APIs, parameters, etc.

Those categories fit better with the user needs, focusing the docs on two axis: action-knowledge and acquisition-application.

You can read more on Diátaxis main site ([link](https://diataxis.fr/)).
