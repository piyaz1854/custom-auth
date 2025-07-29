from rest_framework.views import APIView
from rest_framework.response import Response
from users.permissions import has_permission
from rest_framework import status

DOCUMENTS = [
    {"id": 1,
    "owner_pk": 9,
    "title": "secret document",
    "content":"Джо не входил в сделку."},
    {"id": 2,
    "owner_pk": 9,
    "title": "some document",
    "content":"Special for Effective Mobile."
    }
]
class DocumentsView(APIView):
    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        if has_permission(user, 'read', 'documents', is_owner=False):
            return Response({"documents": DOCUMENTS})

        elif has_permission(user, 'read', 'documents', is_owner=True):
            user_docs = [doc for doc in DOCUMENTS if doc["owner"] == user.id]
            return Response({"documents": user_docs})

        return Response({"detail": "Forbidden"}, status=403)

    def post(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        if not has_permission(user, 'create', 'documents', is_owner=True):
            return Response({"detail": "Forbidden"}, status=403)

        new_doc = {
            "id": len(DOCUMENTS) + 1,
            "title": request.data.get("title", "Untitled"),
            "owner_pk": user.id
        }
        DOCUMENTS.append(new_doc)
        return Response(new_doc, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user
        doc_id = int(request.data.get("id", 0))

        for doc in DOCUMENTS:
            if doc["id"] == doc_id:
                is_owner = doc["owner_pk"] == user.id
                if not has_permission(user, 'update', 'documents', is_owner=is_owner):
                    return Response({"detail": "Forbidden"}, status=403)

                doc["title"] = request.data.get("title", doc["title"])
                return Response(doc)

        return Response({"detail": "Not found"}, status=404)

    def delete(self, request):
        user = request.user
        doc_id = int(request.data.get("id", 0))

        for doc in DOCUMENTS:
            if doc["id"] == doc_id:
                is_owner = doc["owner_pk"] == user.id
                if not has_permission(user, 'delete', 'documents', is_owner=is_owner):
                    return Response({"detail": "Forbidden"}, status=403)

                DOCUMENTS.remove(doc)
                return Response({"detail": "Deleted"})

        return Response({"detail": "Not found"}, status=404)

PROJECTS = [
    {"id": 1, "name": "project 1", "owner": 1},
    {"id": 2, "name": "secure project", "owner": 2}
]

class ProjectsView(APIView):
    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        if has_permission(user, 'read', 'projects', is_owner=False):
            return Response({"projects": PROJECTS})

        elif has_permission(user, 'read', 'projects', is_owner=True):
            own_projects = [p for p in PROJECTS if p["owner"] == user.id]
            return Response({"projects": own_projects})

        return Response({"detail": "Forbidden"}, status=403)

    def post(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        if not has_permission(user, 'create', 'projects', is_owner=True):
            return Response({"detail": "Forbidden"}, status=403)

        name = request.data.get("name", "").strip()
        if not name:
            return Response({"error": "Project name required"}, status=400)

        new_project = {
            "id": len(PROJECTS) + 1,
            "name": name,
            "owner": user.id
        }
        PROJECTS.append(new_project)
        return Response(new_project, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user
        proj_id = int(request.data.get("id", 0))

        project_id = int(request.data.get("id", 0))
        project = next((p for p in PROJECTS if p["id"] == project_id), None)
        if not project:
            return Response({"detail": "Project not found"}, status=404)
        for proj in PROJECTS:
            if proj["id"] == proj_id:
                is_owner = proj["owner_pk"] == user.id
                if not has_permission(user, 'update', 'projects', is_owner=is_owner):
                    return Response({"detail": "Forbidden"}, status=403)
                proj["title"] = request.data.get("title", proj["title"])
                return Response(proj)
        return Response({"detail": "Not found"}, status=404)

    def delete(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        project_id = int(request.data.get("id", 0))
        project = next((p for p in PROJECTS if p["id"] == project_id), None)
        if not project:
            return Response({"detail": "Project not found"}, status=404)

        is_owner = project["owner"] == user.id
        if not has_permission(user, 'delete', 'projects', is_owner=is_owner):
            return Response({"detail": "Forbidden"}, status=403)

        PROJECTS.remove(project)
        return Response({"message": "Project deleted"})