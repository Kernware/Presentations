from dockerspawner import DockerSpawner

c = get_config()

# dummy authenticator to allow all usernames
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = "password"
c.Authenticator.allow_all = True

# create docker container for each new user
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# new containers need to join network
c.DockerSpawner.network_name = "jupyterhub-network"
c.DockerSpawner.image = 'jupyterhub-user'
c.DockerSpawner.remove = True  # remove container when user logs out
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': '/home/jovyan/work' }

c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# allow custom login UI
c.JupyterHub.template_paths = ['/srv/jupyterhub/templates']

# Optional: restrict CPU/RAM per user container
# c.DockerSpawner.cpu_limit = 1
# c.DockerSpawner.mem_limit = '1G'
