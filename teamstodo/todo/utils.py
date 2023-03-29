from todo.models import TeamList


def create_task_api_view(obj, request, *args, **kwargs):
	user = request.user
	data = request.data
	if validate_user_membership(user, data):
		serializer = obj.get_serializer(data=data)
		if validate_is_user_take_task(user, data):
			serializer.is_valid(raise_exception=True)
			obj.perform_create(serializer)
			response_data = serializer.data
			access_status = 'accepted'
		else:
			response_data = 'Вы не можете назначить исполнителем другого пользователя.'
			access_status = 'locked'
	else:
		response_data = 'У вас не прав для добавления задачи в этот список'
		access_status = 'locked'
	return response_data, access_status


def update_task_api_view(obj, request, *args, **kwargs):
	user = request.user
	data = request.data
	if validate_user_membership(user, data):
		partial = kwargs.pop('partial', False)
		instance = obj.get_object()

		if validate_is_user_take_task(user, data):
			serializer = obj.get_serializer(instance, data=data, partial=partial)
			serializer.is_valid(raise_exception=True)
			obj.perform_update(serializer)

			response_data = serializer.data
			access_status = 'accepted'
		else:
			response_data = 'Вы не можете назначить исполнителем другого пользователя.'
			access_status = 'locked'
	else:
		response_data = 'У вас не прав для добавления задачи в этот список'
		access_status = 'locked'
	return response_data, access_status


def validate_user_membership(user, data):
	"""The user can only add(update) tasks to teamlists, where he is a membership."""
	print(data)
	target_teamlist_members = TeamList.objects.get(pk=data['teamlist_relation']).members.all()
	return user in target_teamlist_members


def validate_is_user_take_task(user, data):
	"""The user can take the task only for himself (or set None)."""
	return data['who_takes'] in [user.pk, None]
