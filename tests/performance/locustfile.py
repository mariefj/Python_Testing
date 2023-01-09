from locust import HttpUser, between, task

class ProjectUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def list_competitions(self):
        with self.client.post(
            '/showSummary',
            data={'email': 'john@simplylift.co'},
            catch_response=True
        ) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Getting competitions took too long !")
            else:
                response.success()

    @task
    def book_places(self):
        with self.client.post(
            '/purchasePlaces', 
            data={
                'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': 10
            },
            catch_response=True
        ) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Booking took too long !")
            else:
                response.success()