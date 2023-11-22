def create_page(content, page: int, page_size: int, total_count: int):
    total_pages = (total_count + page_size - 1) // page_size

    return {
        "content": content,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total": total_count,
    }
