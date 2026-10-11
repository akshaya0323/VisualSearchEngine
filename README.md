# VisualSearch

A small Flask app that takes a question and shows web sources and related images together, with links back to where each one came from.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

## How it works

1. You type a question.
2. The app runs a text search and an image search (via the `ddgs` package).
3. It shows the top snippets as a short summary, a grid of images, and the source list.

## Limitations

- The summary is made of snippets copied from the search results. It is not a generated or fact-checked answer.
- Images are not re-ranked for relevance; they appear in the order the search provider returns them.
- `ddgs` uses a third-party provider that can rate-limit or change its response format.
- Images may be copyrighted. Check the source page before reusing one.

## Ideas for next steps

- Re-rank images against the query with CLIP.
- Fetch the full pages and generate a cited answer with an LLM.
- Evaluate image relevance with Precision@K over a set of test queries.
