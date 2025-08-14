from .base import *
import environ

env_file = ROOT_DIR.path('.envs').path(f'.env.{ENVIRONMENT}')
environ.Env.read_env(env_file)

DEBUG = True
