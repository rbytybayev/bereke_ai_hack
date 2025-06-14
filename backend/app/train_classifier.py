#!/usr/bin/env python3
import os
import json
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def main():
    # 1) Загружаем размеченные данные
    dataset_path = "dataset.jsonl"
    if not os.path.exists(dataset_path):
        print(f"Файл {dataset_path} не найден. Сначала создайте dataset.jsonl.")
        return

    texts, labels = [], []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["chunk"])
            labels.append(obj["label"])

    # 2) Загружаем модель эмбеддингов LaBSE
    print("Загружаем SentenceTransformer LaBSE...")
    embedder = SentenceTransformer("sentence-transformers/LaBSE")

    # 3) Считаем эмбеддинги
    print(f"Генерируем эмбеддинги для {len(texts)} фрагментов...")
    embeddings = embedder.encode(texts, show_progress_bar=True)

    # 4) Разбиваем на train и test
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    # 5) Обучаем классификатор
    print("Обучаем LogisticRegression...")
    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    # 6) Оцениваем на тестовой выборке
    print("Оцениваем качество классификации:")
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, zero_division=0)
    print(report)

    # 7) Сохраняем модели
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    emb_model_path = os.path.join(models_dir, "emb_model.pkl")
    clf_path = os.path.join(models_dir, "clf.pkl")
    print(f"Сохраняем embedder в {emb_model_path}")
    with open(emb_model_path, "wb") as f:
        pickle.dump(embedder, f)
    print(f"Сохраняем классификатор в {clf_path}")
    with open(clf_path, "wb") as f:
        pickle.dump(clf, f)

    print("Готово! Модели сохранены в папке 'models'.")


if __name__ == "__main__":
    main()
