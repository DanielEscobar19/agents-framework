import argparse
import json

from agents_framework.retrieval.retrieval_service import RetrievalService
from agents_framework.api.schemas import SearchFilter
from config.config import load_config
from app import App


def main():
    parser = argparse.ArgumentParser(description="agents-framework CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index a repository")
    index_parser.add_argument("root_path", help="Repository path to index")

    retrieve_parser = subparsers.add_parser("retrieve", help="Query the vector index")
    retrieve_parser.add_argument("--query", required=True, help="Search query")
    retrieve_parser.add_argument("--top-k", type=int, help="Override result limit")
    retrieve_parser.add_argument(
        "--min-score",
        type=float,
        help="Override score threshold (e.g. 0.3 to broaden results)",
    )
    retrieve_parser.add_argument(
        "--context",
        action="store_true",
        help="Return assembled context string instead of JSON results",
    )
    retrieve_parser.add_argument(
        "--language", help="Filter by language (e.g. python, csharp, typescript)"
    )
    retrieve_parser.add_argument(
        "--element-type", help="Filter by element type (e.g. method, class, function)"
    )
    retrieve_parser.add_argument("--file-path", help="Filter to an exact file path")
    retrieve_parser.add_argument("--class-name", help="Filter by class name")
    retrieve_parser.add_argument("--namespace", help="Filter by namespace (C# only)")

    args = parser.parse_args()
    config = load_config()

    if args.command == "index":
        app = App(args.root_path, config)
        app.run()

    elif args.command == "retrieve":
        service = RetrievalService(config)

        search_filter = SearchFilter(
            language=args.language,
            element_type=args.element_type,
            file_path=args.file_path,
            class_name=args.class_name,
            namespace=args.namespace,
        )

        if args.context:
            print(service.build_context(args.query, search_filter=search_filter))
        else:
            ctx = service.retrieve(
                args.query,
                limit=args.top_k,
                min_score=args.min_score,
                search_filter=search_filter,
            )
            for r in ctx.results:
                print(
                    json.dumps(
                        {
                            "score": round(r.score, 4),
                            "file": r.file,
                            "lines": f"{r.start_line}-{r.end_line}",
                            "type": r.element_type,
                            "text": r.text[:120].replace("\n", " "),
                        }
                    )
                )


if __name__ == "__main__":
    main()
