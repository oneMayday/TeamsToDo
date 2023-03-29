from todo.tests.test_settings import Settings


class TestPermissions(Settings):
	# Permissions test for guest user
	def test_permissions_guest_user_get_tasks_access_denied(self):
		list_response = self.guest_user.get('/api/v1/tasks/')
		detail_response = self.guest_user.get(f'/api/v1/tasks/{self.task1_user1.pk}/')
		self.assertEqual(list_response.status_code, 403, self.error())
		self.assertEqual(detail_response.status_code, 403, self.error())

	def test_permissions_guest_user_get_teamlist_access_denied(self):
		list_response = self.guest_user.get('/api/v1/teamlist/')
		detail_response = self.guest_user.get(f'/api/v1/teamlist/{self.team_list1.pk}/')
		self.assertEqual(list_response.status_code, 403, self.error())
		self.assertEqual(detail_response.status_code, 403, self.error())

	def test_permissions_guest_user_create_tasks_access_denied(self):
		post_response = self.guest_user.post('/api/v1/tasks/')
		self.assertEqual(post_response.status_code, 403, self.error())

	def test_permissions_guest_user_create_teamlist_access_denied(self):
		post_response = self.guest_user.post('/api/v1/teamlist/')
		self.assertEqual(post_response.status_code, 403, self.error())

	# Permissiom test for authenticated user.
	def test_permissions_authorized_user_tasks_get_access_allowed(self):
		list_response = self.authorized_user1.get('/api/v1/tasks/')
		detail_response = self.authorized_user1.get(f'/api/v1/teamlist/{self.task1_user1.pk}/')
		self.assertEqual(list_response.status_code, 200, self.error())
		self.assertEqual(detail_response.status_code, 200, self.error())

	def test_permissions_authorized_user_teamlist_get_access_allowed(self):
		list_response = self.authorized_user1.get('/api/v1/teamlist/')
		detail_response = self.authorized_user1.get(f'/api/v1/teamlist/{self.team_list1.pk}/')
		self.assertEqual(list_response.status_code, 200, self.error())
		self.assertEqual(detail_response.status_code, 200, self.error())

	def test_permissions_authorized_user_teamlist_patch_access_allowed(self):
		patch_response = self.authorized_user1.patch(f'/api/v1/teamlist/{self.team_list1.pk}/')
		self.assertEqual(patch_response.status_code, 200, self.error())

	def test_permissions_authorized_user_teamlist_patch_access_denied(self):
		patch_response = self.authorized_user1.patch(f'/api/v1/teamlist/{self.team_list2.pk}/')
		self.assertEqual(patch_response.status_code, 403, self.error())

	def test_permissions_authorized_user_teamlist_delete_access_allowed(self):
		delete_response = self.authorized_user1.delete(f'/api/v1/teamlist/{self.team_list1.pk}/')
		self.assertEqual(delete_response.status_code, 204, self.error())

	def test_permissions_authorized_user_teamlist_delete_access_denied(self):
		delete_response = self.authorized_user1.delete(f'/api/v1/teamlist/{self.team_list2.pk}/')
		self.assertEqual(delete_response.status_code, 403, self.error())



	# def test_permissions_authorized_user_member_tasks_create_access_allowed(self):
	# 	response = self.authorized_user1.post('/api/v1/tasks/')
	# 	self.assertEqual(response.status_code, 200, self.error())
	#
	# def test_permissions_authorized_user_member_teamlist_create_access_allowed(self):
	# 	response = self.authorized_user1.post('/api/v1/teamlist/')
	# 	self.assertEqual(response.status_code, 200, self.error())

	# def test_permissions_authorized_user_tasks_patch_access_allowed(self):
	# 	patch_response = self.authorized_user1.patch(f'/api/v1/tasks/{self.task1_user1.pk}/')
	# 	self.assertEqual(patch_response.status_code, 200, self.error())
	#
	# def test_permissions_authorized_user_tasks_patch_access_denied(self):
	# 	patch_response = self.authorized_user1.patch(f'/api/v1/tasks/{self.task1_user2.pk}/')
	# 	self.assertEqual(patch_response.status_code, 403, self.error())


