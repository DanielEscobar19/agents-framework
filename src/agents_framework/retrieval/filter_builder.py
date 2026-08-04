from __future__ import annotations

from qdrant_client.models import FieldCondition, Filter, MatchValue


def build_filter(f) -> Filter | None:
    """Convert a SearchFilter into a Qdrant Filter; returns None when nothing is set."""
    if f is None:
        return None

    conditions = []

    if f.language is not None:
        conditions.append(
            FieldCondition(key="metadata.language", match=MatchValue(value=f.language))
        )
    if f.element_type is not None:
        conditions.append(
            FieldCondition(key="element_type", match=MatchValue(value=f.element_type))
        )
    if f.file_path is not None:
        conditions.append(
            FieldCondition(key="file", match=MatchValue(value=f.file_path))
        )
    if f.class_name is not None:
        conditions.append(
            FieldCondition(
                key="metadata.class_name", match=MatchValue(value=f.class_name)
            )
        )
    if f.namespace is not None:
        conditions.append(
            FieldCondition(
                key="metadata.namespace", match=MatchValue(value=f.namespace)
            )
        )

    return Filter(must=conditions) if conditions else None
