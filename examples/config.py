from environs import Env

env = Env()
env.read_env()

host = env.str('host')
login = env.str('login')
password = env.str('password')
guest_id = env.str('guest_id')
login_user = env.str('login_user')
password_user = env.str('password_user')
