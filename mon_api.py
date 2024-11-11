from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


articles = {
    1: {"nom": "Unité Centrale", "prix": 250},
    2: {"nom": "PC", "prix": 800},
    3: {"nom": "Imprimante", "prix": 1200},
}


class Article(BaseModel):
    nom: str
    prix: float


@app.get("/articles", response_model=list[Article])
def read_articles():
    return list(articles.values())


@app.get("/articles/{article_id}", response_model=Article)
async def read_article(article_id: int):
    if article_id not in articles:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return articles[article_id]


@app.post("/articles", response_model=Article)
async def create_article(article: Article):
    article_id = len(articles) + 1
    articles[article_id] = article
    return article

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    if article_id not in articles:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    articles[article_id] = article
    return article

@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    if article_id not in articles:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    del articles[article_id]
    return {"message": "Article supprimé avec succès"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)