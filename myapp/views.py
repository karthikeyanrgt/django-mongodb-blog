from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Blog
from .serializers import BlogSerializer, BlogUpdateSerializer


# ── LIST + CREATE ─────────────────────────────────────────────────────────────
@api_view(['GET', 'POST'])
def blog_list_create(request):
    """
    GET  /api/blogs/       → list all blogs
    POST /api/blogs/       → create a new blog
    """
    if request.method == 'GET':
        blogs = Blog.get_all()
        return Response({'count': len(blogs), 'blogs': blogs})

    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        blog = Blog.create(
            title=serializer.validated_data['title'],
            content=serializer.validated_data['content'],
        )
        return Response(blog, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── RETRIEVE + UPDATE + DELETE ────────────────────────────────────────────────
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def blog_detail(request, blog_id):
    """
    GET    /api/blogs/<id>/  → retrieve one blog
    PUT    /api/blogs/<id>/  → full update
    PATCH  /api/blogs/<id>/  → partial update
    DELETE /api/blogs/<id>/  → delete
    """
    if request.method == 'GET':
        blog = Blog.get_by_id(blog_id)
        if blog is None:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(blog)

    if request.method in ('PUT', 'PATCH'):
        partial = request.method == 'PATCH'
        serializer = BlogUpdateSerializer(data=request.data, partial=partial)
        if serializer.is_valid():
            updated = Blog.update(blog_id, **serializer.validated_data)
            if updated is None:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(updated)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        deleted = Blog.delete(blog_id)
        if not deleted:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_200_OK)