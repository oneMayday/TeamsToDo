from todo.models import TeamList


def create_task_api_view(obj, request, *args, **kwargs):
	user = request.user
	if validate_user_membership(user, request):
		data = request.data
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
	if validate_user_membership(user, request):
		partial = kwargs.pop('partial', False)
		instance = obj.get_object()
		data = request.data
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


def validate_user_membership(user, request):
	target_teamlist_members = TeamList.objects.get(pk=request.data['teamlist_relation']).members.all()
	return user in target_teamlist_members


def validate_is_user_take_task(user, data):
	if data['who_takes'] in [user.pk, None]:
		return True
