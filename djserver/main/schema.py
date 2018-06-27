import graphene

from graphene_django.types import DjangoObjectType

from main.models import Task, Project


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project


class TaskType(DjangoObjectType):
    class Meta:
        model = Task


class Query(object):
    project = graphene.Field(ProjectType, id=graphene.Int(), name=graphene.String())
    all_projects = graphene.List(ProjectType)
    task = graphene.Field(TaskType, id=graphene.Int(), name=graphene.String())
    all_tasks = graphene.List(TaskType)

    def resolve_all_projects(self, info, **kwargs):
        return Project.objects.all()

    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_project(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Project.objects.get(pk=id)
        if name is not None:
            return Project.objects.get(name=name)

        return None

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Task.objects.get(pk=id)
        if name is not None:
            return Task.objects.get(name=name)

        return None


class CreateProjectMutation(graphene.Mutation):
    class Input:
        name = graphene.String(required=True)
    
    status = graphene.Int()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(self, info, **kwargs):
        name = kwargs.get('name', '').strip()
        try:
            project = Project.objects.create(name=name)
            return CreateProjectMutation(status=200, project=project)
        except:
            return CreateProjectMutation(status=500, project=None)


class Mutation(graphene.ObjectType):
    create_project = CreateProjectMutation.Field()
