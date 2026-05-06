from datetime import datetime, timezone
from bson import ObjectId
from .db import get_collection


class Blog:
    COLLECTION = 'blogs'

    @classmethod
    def _col(cls):
        return get_collection(cls.COLLECTION)

    # ── CREATE ────────────────────────────────────────────────────────────────
    @classmethod
    def create(cls, title: str, content: str) -> dict:
        doc = {
            'title': title,
            'content': content,
            'created_at': datetime.now(timezone.utc),
        }
        result = cls._col().insert_one(doc)
        doc['_id'] = str(result.inserted_id)
        doc['created_at'] = doc['created_at'].isoformat()
        return doc

    # ── READ ALL ──────────────────────────────────────────────────────────────
    @classmethod
    def get_all(cls) -> list:
        blogs = cls._col().find().sort('created_at', -1)
        return [cls._serialize(b) for b in blogs]

    # ── READ ONE ──────────────────────────────────────────────────────────────
    @classmethod
    def get_by_id(cls, blog_id: str) -> dict | None:
        try:
            doc = cls._col().find_one({'_id': ObjectId(blog_id)})
        except Exception:
            return None
        return cls._serialize(doc) if doc else None

    # ── UPDATE ────────────────────────────────────────────────────────────────
    @classmethod
    def update(cls, blog_id: str, title: str = None, content: str = None) -> dict | None:
        updates = {}
        if title is not None:
            updates['title'] = title
        if content is not None:
            updates['content'] = content
        if not updates:
            return cls.get_by_id(blog_id)

        try:
            result = cls._col().find_one_and_update(
                {'_id': ObjectId(blog_id)},
                {'$set': updates},
                return_document=True,  # returns the updated doc
            )
        except Exception:
            return None
        return cls._serialize(result) if result else None

    # ── DELETE ────────────────────────────────────────────────────────────────
    @classmethod
    def delete(cls, blog_id: str) -> bool:
        try:
            result = cls._col().delete_one({'_id': ObjectId(blog_id)})
        except Exception:
            return False
        return result.deleted_count == 1

    # ── HELPER ────────────────────────────────────────────────────────────────
    @staticmethod
    def _serialize(doc: dict) -> dict:
        """Convert MongoDB doc to JSON-safe dict."""
        return {
            'id': str(doc['_id']),
            'title': doc.get('title', ''),
            'content': doc.get('content', ''),
            'created_at': doc['created_at'].isoformat()
                          if hasattr(doc.get('created_at'), 'isoformat')
                          else str(doc.get('created_at', '')),
        }