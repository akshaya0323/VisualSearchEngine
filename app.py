import re
from urllib.parse import urlparse

from flask import Flask, render_template, request
from ddgs import DDGS

app = Flask(__name__)

MAX_WEB = 6
MAX_IMAGES = 8


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def domain(url):
    return urlparse(url).netloc.removeprefix("www.")


def search_web(query):
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=MAX_WEB))
    except Exception as exc:
        return [], f"Web search failed: {clean(exc)}"

    results = []
    for item in raw:
        url = item.get("href") or ""
        title = clean(item.get("title"))
        if url and title:
            results.append({
                "title": title,
                "url": url,
                "domain": domain(url),
                "snippet": clean(item.get("body")),
            })
    return results, None


def search_images(query):
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.images(query, max_results=MAX_IMAGES))
    except Exception as exc:
        return [], f"Image search failed: {clean(exc)}"

    results = []
    for item in raw:
        image = item.get("thumbnail") or item.get("image")
        page = item.get("url") or ""
        if image:
            results.append({
                "title": clean(item.get("title")) or "Untitled image",
                "image": image,
                "page": page or image,
                "domain": domain(page) if page else "",
            })
    return results, None


def summarize(web_results):
    """Use the top snippets as-is. Each line is copied from a source, not generated."""
    lines = []
    for i, r in enumerate(web_results[:3], start=1):
        if r["snippet"]:
            lines.append({"text": r["snippet"], "ref": i})
    return lines


@app.route("/")
def index():
    query = clean(request.args.get("q"))
    web, images, summary, errors = [], [], [], []

    if query:
        web, web_err = search_web(query)
        images, img_err = search_images(query)
        summary = summarize(web)
        errors = [e for e in (web_err, img_err) if e]

    return render_template(
        "index.html",
        query=query,
        web=web,
        images=images,
        summary=summary,
        errors=errors,
    )


if __name__ == "__main__":
    app.run(debug=True)
