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
    message = graphene.String()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(self, info, **kwargs):
        name = kwargs.get('name', '').strip()
        try:
            project = Project.objects.create(name=name)
            return CreateProjectMutation(status=200, message='successful', project=project)
        except:
            return CreateProjectMutation(status=500, message='failed', project=None)


class CreateTaskMutation(graphene.Mutation):
    class Input:
        projectId = graphene.ID(required=True)
        name = graphene.String(required=True)

    status = graphene.Int()
    message = graphene.String()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(self, info, **kwargs):
        project_id = kwargs.get('projectId')
        name = kwargs.get('name', '').strip()
        try:
            project = Project.objects.get(id=project_id)
            task = Task.objects.create(name=name, project=project)
            return CreateTaskMutation(status=200, message='successful', task=task)
        except:
            return CreateTaskMutation(status=500, message='failed', task=None)


class UpdateTaskMutation(graphene.Mutation):
    class Input:
        taskId = graphene.ID(required=True)
        projectId = graphene.ID()
        name = graphene.String()

    status = graphene.Int()
    message = graphene.String()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(self, info, **kwargs):
        project_id = kwargs.get('projectId')
        task_id = kwargs.get('taskId')
        name = kwargs.get('name', '').strip()
        try:
            task = Task.objects.get(id=task_id)
            if project_id is not None:
                task.project_id = project_id
            if name:
                task.name = name
            task.save()
            return UpdateTaskMutation(status=200, message='successful', task=task)
        except Exception as e:
            return UpdateTaskMutation(status=500, message='failed', task=None)


class DeleteTaskMutation(graphene.Mutation):
    class Input:
        taskId = graphene.ID(required=True)

    status = graphene.Int()
    message = graphene.String()

    @staticmethod
    def mutate(self, info, **kwargs):
        taskId = kwargs.get('taskId')
        try:
            task = Task.objects.get(id=taskId)
            Task.delete(task)
            return DeleteTaskMutation(status=200, message='successful')
        except Exception as e:
            return DeleteTaskMutation(status=500, message='failed')


class Mutation(graphene.ObjectType):
    create_project = CreateProjectMutation.Field()
    create_task = CreateTaskMutation.Field()
    update_task = UpdateTaskMutation.Field()
    delete_task = DeleteTaskMutation.Field()
